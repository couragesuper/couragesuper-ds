# for XML
from xml.etree import ElementTree as ET
# socket
import socket
import threading
import time
# for timestamp
from datetime import datetime

# Goal : Connection through OBD connector
# Protocol for communication between GWM and ICCM

# Connection
    # GWM
        #UDP -> VEH_REQ
        #UDP <- VEH_RES (1716)
        #TCP -> Connecting to GWM
        #TCP -> Send Rou_REQ
        #TCP <- Recv Rou_RES
    # PIVI
        #UDP -> VEH_REQ
        #UDP <- VEH_RES
        #TCP -> Connecting to pIVI
        #TCP -> Send Rou_REQ
        #TCP <- Recv Rou_RES

# Step of Test
    # 1. Send Testor Present
    # 2. Send Reading DID F111
    # 3. Send Reading DID F113
    # 4. Send Reading DID F188
    # 5. Send Reading DID F18C
    # 6. Send Reading DID F1BE
    # 7. Send Reading DID F1BF
    # 8. Change Session to Extend
    # 9. Run ODST Routine
    # 10. Run Result of ODST Routine

# SubStep of Test
    # 1. 0 : Ready
    # 2. 1 : Send Command is done ( Wait )
    # 3. 100 : Fail ( Stop )

networkConfig = "Config.xml"

# Byte to Array
# Precondition : ba is valuable Array
def BaToVal(ba):
    value = 0
    if (type(ba) == int): return True, ba
    if (len(ba) > 4):
        return False, ba
    for elem in ba:
        value = (value << 8) | elem
    return True, value

if False:
    config = LoadConfigXML( networkConfig )
    print(config)

# class : Packet Parser
class UDS_Packet_Parser:
    def __init__(self, isDebug):
        self.debugTag = "UDS_Packet_Parser"
        self.log( "Init" , "I" ,  "initalization")
        self.isDebug = True
        self.dictParseRule = {}

    def log(self, subTag, level, msg):
        print("[{}][{}][{}][{}] {}".format(datetime.now(),self.debugTag, subTag, level, msg))

    # RULE XML
        # L1 : DOIP or UDS (Protocols)
        # L2 : Packets
        # L3 : Fields
    def LoadRuleXML(self, xmlfile):
        # Debugging Data
        subTag = "LoadRuleXML"
        self.log(subTag, "I", "[Parsing] Rule the XML")
            # parsing xml
        xmltree = ET.parse(xmlfile)
        xmlroot = xmltree.getroot()
        if (xmlroot == None):
            self.log(subTag, "E", "LoadRuleXML .. Root")
            return False
            # L1
        for node_protocol in xmlroot:
            tag = node_protocol.tag
            self.log(subTag, "I", "\tnode L1 : {}".format(tag))
            if (tag == "DOIP"):
                offset = 0
                for node_l1 in node_protocol:
                    arrayHdrInfo = {}
                    if (node_l1.attrib["name"] == "Header"):
                        self.log(subTag, "I", "\t\tnode L1:{}-> attr:{}".format(node_l1, node_l1.attrib))
                            # L2
                        for node_l2 in node_l1:
                            self.log(subTag, "I", "\t\t\tnode L2:{} -> attr:{}".format(node_l2, node_l2.attrib))
                            name = node_l2.attrib["name"]
                            len = node_l2.attrib["len"]
                            arrayHdrInfo[name] = {"len": int(len), "offset": offset}
                            offset = int(offset) + int(len)
                    self.dictParseRule["DOIPHDR"] = arrayHdrInfo
            elif (tag == "UDS"):
                    #L1
                for node_l1 in node_protocol:
                    arrayUDSInfo = self.dictParseRule["DOIPHDR"].copy()
                    self.log(subTag, "I", "\t\tnode L1:{} -> attr:{}".format(node_l1, node_l1.attrib))
                    packet_name = node_l1.attrib["name"]
                    packet_type = node_l1.attrib["doiptype"]
                    arrayUDSInfo["doiptype"] = packet_type
                    offset = 8
                        #L2
                    for node_l2 in node_l1:
                        if (node_l2.tag != "DOIPHEADER"):
                            self.log(subTag, "I", "\t\t\tnode L2:{} -> attr:{}".format(node_l2, node_l2.attrib))
                            name = node_l2.attrib["name"]
                            len = node_l2.attrib["len"]
                            arrayUDSInfo[name] = {"len": int(len), "offset": offset}
                            offset = int(offset) + int(len)
                        self.dictParseRule[packet_name] = arrayUDSInfo
            else:
                self.log(subTag, "E", " Invalid Node ")

        if (self.isDebug == True):
            self.log(subTag, "I", "[Display Nodes] ")
            for k, v in self.dictParseRule.items():
                self.log(subTag, "D", "\t{} = {} ".format(k, v))
        return True
    def getRuleData(self):
        return self.dictParseRule

# test of packet parser
if False:
    parser = UDS_Packet_Parser(self.isDebug)
    parser.LoadRuleXML("PacketParseRule.xml")
    print(parser.getRuleData())
    exit(0)

class JLR_UDS:
    def __init__(self):
            # 1. Information
        self.debug = 1  # flag for function of some debug
        self.isDebug = True
        self.status = 0  # status flagging
        self.packet_len = 4096  # unit of transmission
            # 2. JLR_UDS
        self.debugTag = "JLR_UDS"
            # 3. XML Config
        self.config = {}
            # 4. Status Flag
        self.resetFlag()
        self.InitPackets()
            # 5. Delay
        self.udsDelay = 0.02
        self.useGWM = False

        # 1. log function
    def log(self, subTag, level, msg):
        print("[{}][{}][{}][{}] {}".format(datetime.now(), self.debugTag, subTag, level, msg))

    def resetFlag(self):
        self.isFoundGWM = False
        self.isFoundPIVI = False

    def InitPackets(self):
        subTag = "InitPackets"

        parser = UDS_Packet_Parser(self.isDebug)
        if (True == parser.LoadRuleXML("PacketParseRule.xml")):
            self.dict_udsRule = parser.getRuleData().copy()

        self.log(subTag, "I", "[Lists of packet data]")
        self.UDSPackets = {}
        self.UDSPackets["VEH_REQ"] = b'\x02\xfd\x00\x01\x00\x00\x00\x00'
        self.UDSPackets["ROUTINE_REQ"] = b'\x02\xfd\x00\x05\x00\x00\x00\x07\x0e\x80\x00\x00\x00\x00\x00'

        self.log(subTag, "I", "[Lists of doip types]")
        self.DOIPType = {}
        self.DOIPType["VEH_REQ"] = 1
        self.DOIPType["VEH_RES"] = 4
        self.DOIPType["ROU_REQ"] = 5
        self.DOIPType["ROU_RES"] = 6

        # Test Step
        self.UDSCommands = {}
        self.UDSCommands["TESTORPRESENT"] = b"\x02\xfd\x80\x01\x00\x00\x00\x08\x0e\x80\x14\xb4\x3e\x00"
        self.UDSCommands["F111"] = b"\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4\x22\xf1\x11"
        self.UDSCommands["F113"] = b"\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4\x22\xf1\x13"
        self.UDSCommands["F188"] = b"\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4\x22\xf1\x88"
        self.UDSCommands["F18C"] = b"\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4\x22\xf1\x8c"
        self.UDSCommands["F1BE"] = b"\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4\x22\xf1\xbe"
        self.UDSCommands["F1BF"] = b"\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4\x22\xf1\xbf"
        self.UDSCommands["EXTSESSION"] = b"\x02\xfd\x80\x01\x00\x00\x00\x06\x0e\x80\x14\xb4\x10\x03"
        self.UDSCommands["ODST"] = b"\x02\xfd\x80\x01\x00\x00\x00\x08\x0e\x80\x14\xb4\x31\x01\x02\x02"
        self.UDSCommands["ODST_RET"] = b"\x02\xfd\x80\x01\x00\x00\x00\x08\x0e\x80\x14\xb4\x31\x03\x02\x02"

        self.TestList = ["TESTORPRESENT" ,  "F111" , "F113", "F188" , "F18C" , "F1BE" , "F1BF", "EXTSESSION" , "ODST", "ODST_RET"]

        self.TestStep = 1
        self.TestSubStep = 100 ; #Ready  0(Ready) 1(Send) 2(Recv) , 100(Wait) ,200(Invalid)

        # TEST STEP
            # 1. Send Testor Present
            # 2. Send Reading DID F111
            # 3. Send Reading DID F113
            # 4. Send Reading DID F188
            # 5. Send Reading DID F18C
            # 6. Send Reading DID F1BE
            # 7. Send Reading DID F1BF
            # 8. Change Session to Extend
            # 9. Run ODST Routine
            # 10. Run Result of ODST Routine

        self.arrDIDPartNumbers = []
        self.arrDIDPartNumbers.append(b'\xf1\x11')
        self.arrDIDPartNumbers.append(b'\xf1\x12')
        self.arrDIDPartNumbers.append(b'\xf1\x13')
        self.arrDIDPartNumbers.append(b'\xf1\x88')
        self.arrDIDPartNumbers.append(b'\xf1\x90')
        self.arrDIDPartNumbers.append(b'\xf1\xA0')
        self.arrDIDPartNumbers.append(b'\xf1\xBE')
        self.arrDIDPartNumbers.append(b'\x41\xAE')
        self.arrDIDPartNumbers.append(b'\x48\x84')

    # Load Network Information from XML
    def LoadConfigXML(self, xml_file):
        xmltree = ET.parse(xml_file)
        xmlroot = xmltree.getroot()
        if (xmlroot == None):
            print("[JLR_UDS][Error] LoadConfigXML .. Root ")
            return False
        for node in xmlroot:
            self.config["IP_ETH"] = node.attrib['IP_ETH']
            # self.config["IP"] = node.attrib['IP']
            self.config["PORT"] = int(node.attrib['PORT'])
            # self.targetAddr = ( self.config["IP"], self.config["PORT"] )
            if (self.debug and 1):
                print("[JLR_UDS] LoadConfigXML .. Ret:{} ".format(self.config))

    # Utility to delay
    def delayUDS(self):
        time.sleep( self.udsDelay )

    def makeUDSPacket(self , msgByteArr ):
        doiphdr = b"\x02\xfd\x80\x01\x00\x00\x00\x08\x0e\x80\x14\xb4" + msgByteArr
        self.log( "makeUDSCommand" , "I" , doiphdr )
        return doiphdr

    # parsing byte through BaToVal ( 2 param )
        # msg is string (need to convert byte array)
    def parseUDSPacket(self, addr, msg):
        subTag = "parseUDSPacket"
        ba_pkt = bytearray(msg)
        data = {"ret":True}
        if (len(ba_pkt) >= 8):
            # found rule
            Ret, doipType = BaToVal(ba_pkt[2: 2 + 2])
            if (Ret != True):
                self.log(subTag, "E", "DoipType")
            RetFound, rule = self.foundRule(doipType)
            if (RetFound == True):
                for rule_k, rule_v in rule.items():
                    if (rule_k != "doiptype"):
                        # print("{} = {}".format(rule_k, rule_v))
                        off = int(rule_v["offset"])
                        length = int(rule_v["len"])
                        data[rule_k] = BaToVal(ba_pkt[off:off + length])[1]
            else:
                self.log(subTag, "E", "Found Rule Error -> Type : {}".format(doipType))
                data["ret"] = False
        else:
            self.log(subTag, "E", "Packet Error(short packet) -> len : {}".format(len(packet)))
            data["ret"] = False
        self.log(subTag, "I", "Parsed Data = {}".format(data))
        return data

    def foundRule(self, doiptype):
        for key, rule in self.dict_udsRule.items():
            #self.log("foundRule", "D" , "{} vs {}:{}".format( key, doiptype , rule["doiptype"] ) )
            if (key != "DOIPHDR"):
                type = int(rule["doiptype"])
                if (doiptype == type): return True, rule
        return False, None

    # found PIVI and Connect PIVI
    def foundPIVI(self , useGWM ):
        self.useGWM = useGWM
            # 1.unset flag whether PIVI is found
            # 2.Create UDP Socket to broadcast to found PIVI
        self.createUDPSocket()
            # 3.Create Sending Thread and Receiving Thread
        self.threadFoundDOIP_Send = threading.Thread(target=self.loopFoundDOIP_Send)
        self.threadFoundDOIP_Recv = threading.Thread(target=self.loopFoundDOIP_Recv)
            # 4 run Threads
        self.threadFoundDOIP_Send.start()
        self.threadFoundDOIP_Recv.start()

    # network
    # UDP socket : broad cast VEH message to all network .
    # pivi answers VEH response.
    def createUDPSocket(self):
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sockUDP.bind((self.config["IP_ETH"], self.config["PORT"]))

    # Protocol DOIP
    # make UDP socket
    # send VEH req : -> "VEH_REQ" (Doip 1)
    # recv VEH res : -> "VEH_RES" (Doip 4) -> set isFoundPIVI to True
    # close UDP socket

    def loopFoundDOIP_Send(self):
        # send vehicle identification message until pivi is answered.
        if( self.useGWM == True ) :
            while self.isFoundGWM == False:
                # self.log( "loopFoundDOIP_Send" , "I" , "Request Vehicle Identification" )
                self.sockUDP.sendto(self.UDSPackets["VEH_REQ"], ("255.255.255.255", self.config["PORT"]))
                self.delayUDS()

        while self.isFoundPIVI == False:
            self.sockUDP.sendto(self.UDSPackets["VEH_REQ"], ("255.255.255.255", self.config["PORT"]))
            self.delayUDS()
        self.sockUDP.close()
        self.delayUDS()

    def loopFoundDOIP_Recv(self):
        subTag = "loopFoundDOIP_Recv"

        if( self.useGWM == True ) :
            while self.isFoundGWM == False:
                msg, addr = self.sockUDP.recvfrom(self.packet_len)
                # print("[loopFoundPIVI_Recv] msg:{0}, msglen:{2}, addr:{1}".format(msg, addr, len(msg)))
                if (addr[0] == self.config["IP_ETH"]):
                    self.log( subTag , "I" , "[Ignore :: Skipping] Packet is received from self")
                else:
                    data = self.parseUDSPacket(addr, msg)
                    # From PIVI
                    if ((data['type'] == self.DOIPType["VEH_RES"]) and (data['LogAddr'] == 0x1716)):
                        #self.PIVI_Addr = addr
                        self.GWM_Addr = addr
                        self.GWM_VEH = data
                        self.delayUDS()
                        self.isFoundGWM = True
                    else:
                        print(">> I don't know this message")
            self.CreateTCPSockGWM()
            self.runLoopUDS_GWM()

            while self.isRecvRoutineActivation_GWM == False :
                self.delayUDS()

        while self.isFoundPIVI == False:
            msg, addr = self.sockUDP.recvfrom(self.packet_len)
            # print("[loopFoundPIVI_Recv] msg:{0}, msglen:{2}, addr:{1}".format(msg, addr, len(msg)))
            if (addr[0] == self.config["IP_ETH"]):
                print("    [ignore] packet from self ")
            else:
                data = self.parseUDSPacket(addr, msg)
                if ((data['type'] == self.DOIPType["VEH_RES"]) and (data['LogAddr'] == 0x14B4)):
                    self.PIVI_Addr = addr
                    self.PIVI_VEH = data
                    self.isFoundPIVI = True
                else:
                    print(">> I don't know this message")

        self.CreateTCPSock()
        self.runLoopUDS()

    def CreateTCPSock(self):
        # Create TCP Coskcet
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockTCP.connect(self.PIVI_Addr)

    def CreateTCPSockGWM(self):
        # Create TCP Coskcet
        self.sockTCP_GWM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockTCP_GWM.connect(self.GWM_Addr)

    def runLoopUDS_GWM(self):
        subTag = "runLoopUDS_GWM"
        self.log( subTag, "I" , "reset flags and starting GWM's Thread.")
        self.isRecvRoutineActivation_GWM = False;
        self.isUDSLoopRunning_GWM = True
        self.threadTCP_Send_GWM = threading.Thread(target=self.loopUDS_Send_GWM)
        self.threadTCP_Send_GWM.start()
        self.threadTCPRecv_GWM = threading.Thread(target=self.loopUDS_Recv_GWM)
        self.threadTCPRecv_GWM.start()

    def runLoopUDS_GWM(self):
        subTag = "runLoopUDS_GWM"
        self.log( subTag , "I" , "reset flags and starting GWM's threads")
        self.isRecvRoutingActivation_GWM = False
        self.isUDSLoopRunning_GWM = True
        self.threadTCP_Send_GWM = threading.Thread( target=self.loopUDS_Send_GWM)
        self.threadTCP_Send_GWM.start()

    def loopUDS_Send_GWM(self):
        subTag = "loopUDS_Send_GWM"
        while self.isRecvRoutineActivation_GWM == False:
            self.log(subTag, "I", " [Send] Routing Acitivation Reqeust (GWM)");
            self.sockTCP_GWM.sendto(self.UDSPackets["ROUTINE_REQ"], self.GWM_Addr)
            self.delayUDS()

    def loopUDS_Recv_GWM(self):
        subTag = "loopUDS_Recv_GWM"
        while self.isRecvRoutineActivation_GWM == False:
            msg = self.sockTCP_GWM.recv(self.packet_len)
            self.log(subTag, "I", " Data is received=len:{} data:{}".format(len(msg), msg))
            data = self.parseUDSPacket(0, msg)
            if( (data['type'] == self.DOIPType["ROU_RES"]) and
                    (data['SourceAddr'] == 0x1716) and
                    (data['ResponseCode'] == 0x10) ):
                self.log(subTag, "I", " Routing is activated " )
                self.isRecvRoutineActivation_GWM = True
            else:
                self.log(subTag, "E", " Parsed Packet is unknown." )
            time.sleep(self.udsDelay)
            self.sockTCP_GWM.close()

    # UDS Command
    def udsReadingDID( self, did ):
        print( "sendReadingDID : did{} :type:{}".format(did , type(did)))
        if( type(did) == bytes ) :
            msg = b'\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4\x22'
            msg = msg + did
            print( "message:{}".format( msg )  )
            self.sockTCP.sendto( msg, self.PIVI_Addr )
            time.sleep(self.udsDelay)
        else :
            print( "sendReadingDID is failed with illegal param:{}".format( did ) )

    # Protocol UDS
        # send Routing Acitivation : -> "ROU_REQ" (Doip 5)
        # recv Routing Response : -> "ROU_RES" (Doip 6)
    def runLoopUDS(self):
        print("runLoopUDS")
        self.isRecvRoutineActivation = False;

        self.isUDSLoopRunning = True
        self.threadTCP_Send = threading.Thread(target=self.loopUDS_Send)
        self.threadTCP_Send.start()
        self.threadTCPRecv = threading.Thread(target=self.loopUDS_Recv)
        self.threadTCPRecv.start()

    def loopUDS_Send(self):
        subTag = "loopUDS_Send"
        self.log(subTag, "I" , "Start Loop")

        while self.isRecvRoutineActivation == False:
            self.log(subTag, "I", " [Send] Routing Acitivation Reqeust [PIVI]");
            self.sockTCP.sendto(self.UDSPackets["ROUTINE_REQ"], self.PIVI_Addr)
            self.delayUDS()

        self.log(subTag, "I", "Routing Activation in Sending Loop [PIVI]" )

        self.isUDSTestSending = True
        while self.isUDSTestSending :
            if( self.TestSubStep == 0 ):
                if( self.TestStep < len( self.TestList ) ) :
                    test = self.TestList[  self.TestStep ]
                    test_packet = self.UDSCommands[ test ]
                    self.log(subTag, "I", "Sending = {}:{} ".format(test , test_packet) )
                    self.sockTCP.sendto( test_packet , self.PIVI_Addr)
                    self.TestSubStep = 1 # Send
                else :
                    self.log(subTag, "I", "Sending Commands is done\n")
                    self.isUDSTestSending = False

            self.delayUDS()

        self.log(subTag, "I", "End Loop")
        self.isUDSTestRecving = False

    def loopUDS_Recv(self):
        subTag = "loopUDS_Recv"
        self.log(subTag, "I", "Start of Loop")
        while self.isRecvRoutineActivation == False:
            msg = self.sockTCP.recv(self.packet_len)
            self.log(subTag, "I", " Data is received=len:{} data:{}".format(len(msg), msg))
            data = self.parseUDSPacket(0, msg)
            if ((data['type'] == self.DOIPType["ROU_RES"]) and (data['SourceAddr'] == 0x14b4) and (
                    data['ResponseCode'] == 0x10)):
                print(">> >> Routing Activation ")
                self.isRecvRoutineActivation = True
                self.TestSubStep = 0
            else:
                self.log(subTag, "E" , "Parsed Packet is unknown type.")
            time.sleep(self.udsDelay)

        self.log(subTag, "I", "Ready to receive UDS Commands")

        # Test step
        self.isUDSTestRecving = True
        while self.isUDSTestRecving:
            #sub step
            #self.log(subTag, "I", "loop : {}".format( self.TestSubStep) )
            if( (self.TestSubStep == 1) or  (self.TestSubStep == 2) ) :
                #self.log(subTag, "I", "loop Recv")
                rcvdata = self.sockTCP.recv(self.packet_len)
                # buffering
                Data = self.parseUDSPacket( 0, rcvdata )
                self.log( subTag, "I" , "Rcv Data={} -> Parsed Data:{} ".format( rcvdata, Data ))
                if( Data["ret"] == True) :
                    # Diagnostics Ack (ACK in doip . i think)
                    if( ( Data["type"] == 0x8002 )  ) :
                        self.log(subTag, "I" , "Diag Ack : {}".format( Data["AckCode"]) )
                        # if packet is over 13
                        if( len(rcvdata) > 13 ) :
                            rcvdata2 = rcvdata[13:]
                            Data = self.parseUDSPacket( 0, rcvdata2 )
                        else :
                            self.TestSubStep = 2

                    # UDS Command is received
                    if ( ( Data["type"] == 0x8001 ) ) :
                        udscode = hex(Data["UDSCode"]).upper()
                        udssubcode = hex(Data["UDSSubCode"]).upper()
                        self.log(subTag, "I" , "UDS-Cmd:{} SubCmd:{} ".format( udscode , udssubcode ) )
                        if( (udscode == "0X7F") and ( udssubcode == "0X3178" )) :
                            self.log(subTag, "I" , " UDS is pending "  )
                        elif ( udscode == "0x7F" ) :
                            self.log(subTag, "I", " UDS is Failed ")
                            self.TestStep = self.TestStep + 1
                            self.TestSubStep = 0
                        else :
                            if udscode == "0X62" :
                                if udssubcode == "0XF111" :
                                    self.log( subTag, "I", "Reading DID Result : Data:{} Len:".format(rcvdata[-24:]))
                                elif udssubcode == "0XF113" :
                                    self.log( subTag, "I", "Reading DID Result : Data:{}".format(rcvdata[-24:]))
                                elif udssubcode == "0XF188" :
                                    self.log( subTag, "I", "Reading DID Result : Data:{}".format(rcvdata[-24:]))
                                elif udssubcode == "0XF18C" :
                                    self.log( subTag, "I", "Reading DID Result : Data:{}".format(rcvdata[-16:]))
                                elif udssubcode == "0XF1BE" :
                                    self.log( subTag, "I", "Reading DID Result : Data:{}".format(rcvdata[-64:]))
                                elif udssubcode == "0XF1BF" :
                                    self.log( subTag, "I", "Reading DID Result : Data:{}".format(rcvdata[-64:]))
                            self.TestStep = self.TestStep + 1
                            self.TestSubStep = 0
            self.delayUDS()
        self.log(subTag, "I", "End of Loop")
        self.sockTCP.close()

# Module Test
if True:
    jlruds = JLR_UDS()
    jlruds.LoadConfigXML( networkConfig )
    jlruds.foundPIVI( False )

