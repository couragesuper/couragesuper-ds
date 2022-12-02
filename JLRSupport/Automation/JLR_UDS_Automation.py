from xml.etree import ElementTree as ET
import socket
import threading
import time
from datetime import datetime
import sys
import os

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


# class : Packet Parser
class UDS_Packet_Parser:
    def __init__( self , loglevel ):
        self.loglevel = loglevel
        self.debugTag = "UDS_Packet_Parser"
        self.log( "Init", "I", "initalization" )
        self.dictParseRule = {}

    def log(self, subTag, level, msg):
        try :
            if( level in self.loglevel ) :
                print("[{}][{}][{}][{}] {}".format(datetime.now(),self.debugTag, subTag, level, msg))
            else: {

            }
        except Exception as e:
            print("\n[Exception]{}\n".format(e))

    # RULE XML
        # L1 : DOIP or UDS (Protocols)
        # L2 : Packets
        # L3 : Fields
    def LoadRuleXML(self, xmlfile):
        # Debugging Data
        subTag = "LoadRuleXML"
        self.log(subTag, "D", "[Parsing] Rule the XML")

        # Element Tree
        xmltree = ET.parse(xmlfile)
        xmlroot = xmltree.getroot()
        if (xmlroot == None):
            self.log(subTag, "E", "LoadRuleXML .. Root")
            return False
            # L1
        for node in xmlroot:
            tag = node.tag
            if (tag=="CONFIG") :
                isDbg = True if str(node.attrib["DEBUG"]).upper() == "TRUE" else False
            elif (tag == "DOIP"):
                self.log(subTag, "D", "\tnode L1 DOIP")
                offset = 0
                for node_l1 in node:
                    arrayHdrInfo = {}
                    if (node_l1.attrib["name"] == "Header"):
                        if( isDbg == True ) : self.log(subTag, "I", "\t\tnode L1:{}-> attr:{}".format(node_l1, node_l1.attrib))
                            # L2
                        for node_l2 in node_l1:
                            if( isDbg == True ) : self.log(subTag, "I", "\t\t\tnode L2:{} -> attr:{}".format(node_l2, node_l2.attrib))
                            name = node_l2.attrib["name"]
                            len = node_l2.attrib["len"]
                            arrayHdrInfo[name] = {"len": int(len), "offset": offset}
                            offset = int(offset) + int(len)
                    self.dictParseRule["DOIPHDR"] = arrayHdrInfo
            elif (tag == "UDS"):
                self.log(subTag, "D", "\tnode L1 UDS")
                    #L1
                for node_l1 in node:
                    arrayUDSInfo = self.dictParseRule["DOIPHDR"].copy()
                    if( isDbg == True ) : self.log(subTag, "I", "\t\tnode L1:{} -> attr:{}".format(node_l1, node_l1.attrib))
                    packet_name = node_l1.attrib["name"]
                    packet_type = node_l1.attrib["doiptype"]
                    arrayUDSInfo["doiptype"] = packet_type
                    offset = 8
                        #L2
                    for node_l2 in node_l1:
                        if (node_l2.tag != "DOIPHEADER"):
                            if( isDbg == True ) : self.log(subTag, "I", "\t\t\tnode L2:{} -> attr:{}".format(node_l2, node_l2.attrib))
                            name = node_l2.attrib["name"]
                            len = node_l2.attrib["len"]
                            arrayUDSInfo[name] = {"len": int(len), "offset": offset}
                            offset = int(offset) + int(len)
                        self.dictParseRule[packet_name] = arrayUDSInfo
            else:
                self.log(subTag, "E", " Invalid Node ")

        # Result of Parsed Rule
        self.log(subTag, "D", "[Display Nodes] ")
        for k, v in self.dictParseRule.items():
            self.log(subTag, "D", "\t{} = {} ".format(k, v))

        self.log(subTag, "I", "[Parsing] Completed.")
        return True
    def getRuleData(self):
        return self.dictParseRule

# test of packet parser
if False:
    parser = UDS_Packet_Parser(self.isDebug)
    parser.LoadRuleXML("PacketParseRule.xml")
    print(parser.getRuleData())
    exit(0)

class stopWatch :
    def reset(self) :
        self.start_time = time.time()
    def diff(self):
        return time.time() - self.start_time

class JLR_UDS:
    def __init__( self , xmlConfig ):

        self.loglevel = ['I','E']

        self.stopwatch = stopWatch()
        self.debugTag = "JLR_UDS"
        self.config={}
        self.LoadConfigXML( xmlConfig )
        self.resetFlag()
        self.InitPackets()
        self.udsDelay = self.config["UDSDELAY"]
        self.useGWM = self.config["USEGWM"]
        self.packet_len = self.config["PACKETLEN"]

        self.loglevel = ['I','E']
        if( self.config["ISDEBUG"] ) : self.loglevel = ['I' , 'E' , 'D']

        self.testStatus = {
            "id": 0 ,
            "name" : "DEFAULT" ,
            "status" : "READY" , # READY, RUNNING , FAIL, SUCCEED
            "param" : True ,
            "info" : {}
        }
        self.isAutomationTest = self.config["AUTOMATION"]

    # UTIL : log
    def log(self, subTag, level, msg):
        try :
            if( level in self.loglevel ) : print("[{}][{}][{}][{}] {}".format(datetime.now(), self.debugTag, subTag, level, msg))
            else : {}
        except Exception as e :
            print("\n[exception]{}\n".format(e))

    # Relase
    def Close(self):
        subTag ="Close"
        self.isUDSTestRecving = False
        #self.threadTCP_Send = threading.Thread(target=self.loopUDS_Send)
        #self.threadTCPRecv = threading.Thread(target=self.loopUDS_Recv)
        #self.log(subTag, "D", "JOIN...1");
        self.threadTCP_Send.join(2)
        #self.log(subTag, "D", "JOIN...2");
        self.threadTCPRecv.join(2)
        #self.log(subTag, "D", "JOIN...2");


    # STATE
    def resetFlag(self):
        self.isFoundGWM = False
        self.isFoundPIVI = False

    # Initalize Packet Data
    def InitPackets(self):
        subTag = "InitPackets"

        # Copy from Parser
        parser = UDS_Packet_Parser(self.loglevel)
        if (True == parser.LoadRuleXML("PacketParseRule.xml")):
            self.dict_udsRule = parser.getRuleData().copy()

        # for Connecting ECUs (GWM,PIVI)
        # self.log(subTag, "I", "[Lists of packet data]")
        self.UDSPackets = {}
        self.UDSPackets["VEH_REQ"] = b'\x02\xfd\x00\x01\x00\x00\x00\x00'
        self.UDSPackets["ROUTINE_REQ"] = b'\x02\xfd\x00\x05\x00\x00\x00\x07\x0e\x80\x00\x00\x00\x00\x00'

        #[Lists of doip types]
        #self.log(subTag, "I", "[Lists of doip types]")
        self.DOIPType = {}
        self.DOIPType["VEH_REQ"] = 1
        self.DOIPType["VEH_RES"] = 4
        self.DOIPType["ROU_REQ"] = 5
        self.DOIPType["ROU_RES"] = 6

        # One Shot Test
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
        self.TestSubStep = 100

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
        subtag = "LoadConfigXML"
        xmltree = ET.parse(xml_file)
        xmlroot = xmltree.getroot()
        if (xmlroot == None):
            self.log(subtag, "E", "Root isn't found.")
            return False
        for node in xmlroot:
            if( node.tag == "Network") :
                self.config["IP_ETH"] = node.attrib['IP_ETH']
                self.config["PORT"] = int(node.attrib['PORT'])
            elif( node.tag == "Config" ) :
                self.config["USEGWM"] = True if str(node.attrib['USEGWM']).upper() == "TRUE" else False
                self.config["AUTOMATION"] = True if str(node.attrib['AUTOMATION']).upper() == "TRUE" else False
                self.config["UDSDELAY"] = float(node.attrib['UDSDELAY'])
                self.config["PACKETLEN"] = int(node.attrib['PACKETLEN'])
                self.config["DID_TIMEOUT_SEC"] = int(node.attrib['DID_TIMEOUT_SEC'])
                self.config["ISDEBUG"] = True if str(node.attrib['ISDEBUG']) == "TRUE" else False
            else :
                self.log(subtag, "E", "Invalid node is founded")
        self.log(subtag, "I" , "Config is loaded with IP:{} , PORT:{} , USEGWM:{}, Automation:{} ".format( self.config["IP_ETH"] , self.config["PORT"] , self.config["USEGWM"] , self.config["AUTOMATION"]) )

    # Utility to delay
    def delayUDS(self):
        time.sleep( self.udsDelay )
    def delayUDS1S(self):
        time.sleep( 1 )
    def delayUDS_self(self , delay):
        time.sleep( delay )

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
            self.log(subTag, "E", "Packet Error(short packet) -> len : {}".format(len(ba_pkt)))
            data["ret"] = False
        self.log(subTag, "D", "Parsed Data = {}".format(data))
        return data

    def foundRule(self, doiptype):
        for key, rule in self.dict_udsRule.items():
            #self.log("foundRule", "D" , "{} vs {}:{}".format( key, doiptype , rule["doiptype"] ) )
            if (key != "DOIPHDR"):
                type = int(rule["doiptype"])
                if (doiptype == type): return True, rule
        return False, None

    # found PIVI and Connect PIVI
    def foundPIVI(self ):
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
        subTag = "loopFoundDOIP_Send"
        if( self.useGWM == True ) :
            self.isRecvRoutineActivation_GWM = False
            while self.isFoundGWM == False:
                self.log( subTag , "D" , "[Send] VEH_ID_REQ by GWM" )
                self.sockUDP.sendto(self.UDSPackets["VEH_REQ"], ("255.255.255.255", self.config["PORT"]))
                self.delayUDS()
            while self.isRecvRoutineActivation_GWM == False:
                self.log( subTag , "I" , "UDP Step GWM to PIVI (GWM Done)  " )
                self.delayUDS()

        # PIVI Sequence
        while self.isFoundPIVI == False:
            self.log(subTag, "D", "[Send] VEH_ID_REQ by PIVI ")
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
                    self.log( subTag , "D" , "[Ignore :: Skipping] Packet is received from self")
                else:
                    data = self.parseUDSPacket(addr, msg)
                    # From PIVI
                    if ((data['type'] == self.DOIPType["VEH_RES"]) and (data['LogAddr'] == 0x1716)):
                        self.log( subTag , "D" , "VEH ID Response in GWM" )
                        #self.PIVI_Addr = addr
                        self.GWM_Addr = addr
                        self.GWM_VEH = data
                        self.delayUDS()
                        self.isFoundGWM = True
                    else:
                        self.log(subTag, "E", "unknown packet is received.")

            self.CreateTCPSockGWM()
            self.runLoopUDS_GWM()
            while self.isRecvRoutineActivation_GWM == False :
                self.delayUDS()

        while self.isFoundPIVI == False:
            msg, addr = self.sockUDP.recvfrom(self.packet_len)
            # print("[loopFoundPIVI_Recv] msg:{0}, msglen:{2}, addr:{1}".format(msg, addr, len(msg)))
            if (addr[0] == self.config["IP_ETH"]):
                self.log( subTag, "D" , "[Skipping] self packet is passed \n.")
            else:
                data = self.parseUDSPacket(addr, msg)
                if ((data['type'] == self.DOIPType["VEH_RES"]) and (data['LogAddr'] == 0x14B4)):
                    self.log( subTag, "I" , "[Recv] VEH ID Response in PIVI")
                    self.PIVI_Addr = addr
                    self.PIVI_VEH = data
                    self.isFoundPIVI = True
                else:
                    self.log( subTag, "E" , "[Exception] packet is unexpected type.")
        self.CreateTCPSock()
        self.runLoopUDS()

    def CreateTCPSock(self):
        # Create TCP Coskcet
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockTCP.connect(self.PIVI_Addr)
        self.sockTCP.settimeout(1)

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
                self.log(subTag, "I", " Routing is activated [GWM]." )
                self.isRecvRoutineActivation_GWM = True
            else:
                self.log(subTag, "E", " Recv Unknown Packet is received." )
            time.sleep(self.udsDelay)
            #self.sockTCP_GWM.close() #

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
        subTag = "runLoopUDS"
        self.log(subTag, "I", "Start of Loop")
        self.isRecvRoutineActivation = False;

        self.isUDSLoopRunning = True
        self.threadTCP_Send = threading.Thread(target=self.loopUDS_Send)
        self.threadTCP_Send.start()
        self.threadTCPRecv = threading.Thread(target=self.loopUDS_Recv)
        self.threadTCPRecv.start()
        self.log(subTag, "I", "End of Loop")

    def loopUDS_Send(self):
        subTag = "loopUDS_Send"
        self.log(subTag, "I" , "Start Loop")

        while self.isRecvRoutineActivation == False:
            self.log(subTag, "I", " [Send] Routing Acitivation Reqeust");
            self.sockTCP.sendto(self.UDSPackets["ROUTINE_REQ"], self.PIVI_Addr)
            #self.delayUDS()
            time.sleep(0.5) # too many sending makes problem in test suite

        self.log(subTag, "I", "Routing Activation in Sending Loop")

        if self.isAutomationTest == False :
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
            self.isUDSTestRecving = False # Work to do (change this)

    def isAllZero(self , data):
        cnt_zero = 0
        for idx in range(0,len(data)) :
            if  data[idx] == '\0' : cnt_zero = cnt_zero + 1
        if( cnt_zero == len(data) ) : return True
        return False

    def testcase_snapshot(self , data ):
        if( self.isAllZero( data ) ) : self.testStatus["status"] = "FAIL"
        else: self.testStatus["status"] = "OK"
        self.testStatus["info"] = {}
        self.testStatus["info"]["time"] = self.stopwatch.diff()
        self.testStatus["info"]["data"] = data

    def testcase_snapshot_ret(self , ret ):
        if  ret  : self.testStatus["status"] = "OK"
        else: self.testStatus["status"] = "FAIL"
        self.testStatus["info"] = {}
        self.testStatus["info"]["time"] = self.stopwatch.diff()

    def testcase_resend(self):
        subtag = "testcase_resend"
        test_packet = self.UDSCommands[ self.testStatus["name"] ]
        self.log(subtag, "I", "Sending = {}:{} ".format( self.testStatus["name"] , test_packet))
        self.sockTCP.sendto(test_packet, self.PIVI_Addr)

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
                # for AutomateTest
                if( self.isAutomationTest == True ) :
                    if ( (self.testStatus["name"] == "CONNECT") and (self.testStatus["status"] == "RUNNING") ) :
                        self.testStatus["status"] = "OK"
            else:
                self.log(subTag, "E" , "Parsed Packet is unknown type.")
            time.sleep(self.udsDelay)
        self.log(subTag, "I", "Ready to receive UDS Commands")

        if self.isAutomationTest == False:
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
                    self.log( subTag, "D" , "Rcv Data={} -> Parsed Data:{} ".format( rcvdata, Data ))
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
                            self.log(subTag, "D" , "UDS-Cmd:{} SubCmd:{} ".format( udscode , udssubcode ) )
                            if( (udscode == "0X7F") and ( udssubcode == "0X3178" )) :
                                self.log(subTag, "I" , " UDS is pending "  )
                            elif ( udscode == "0x7F" ) :
                                self.log(subTag, "E", " UDS is Failed ")
                                self.TestStep = self.TestStep + 1
                                self.TestSubStep = 0
                            else :
                                if udscode == "0X62" :
                                    if udssubcode == "0XF111" :
                                        self.log( subTag, "I" , "Reading DID:{} Result:{}".format(rcvdata[-24:]))
                                    elif udssubcode == "0XF113" :
                                        self.log(subTag, "I", "Reading DID:{} Result:{}".format(rcvdata[-24:]))
                                    elif udssubcode == "0XF188" :
                                        self.log(subTag, "I", "Reading DID:{} Result:{}".format(rcvdata[-24:]))
                                    elif udssubcode == "0XF18C" :
                                        self.log(subTag, "I", "Reading DID:{} Result:{}".format(rcvdata[-16:]))
                                    elif udssubcode == "0XF1BE" :
                                        self.log(subTag, "I", "Reading DID:{} Result:{}".format(rcvdata[-64:]))
                                    elif udssubcode == "0XF1BF" :
                                        self.log(subTag, "I", "Reading DID:{} Result{}".format(rcvdata[-64:]))
                                self.TestStep = self.TestStep + 1
                                self.TestSubStep = 0
                self.delayUDS()
            self.log(subTag, "I", "End of Loop")
            self.sockTCP.close()
        elif self.isAutomationTest == True:
        # Test step
            self.isUDSTestRecving = True
            while self.isUDSTestRecving:

                try :
                    self.log(subTag, "D", "loop rcv ..1 ")
                    rcvdata = self.sockTCP.recv(self.packet_len)
                    self.log(subTag, "D", "loop rcv ..2 ")
                    # buffering
                    Data = self.parseUDSPacket( 0, rcvdata )
                    self.log(subTag, "D", "loop rcv ..3 ")
                    self.log(subTag, "D", "Rcv Data={} -> Parsed Data:{} ".format(rcvdata, Data))
                except Exception as e :
                    self.log(subTag, "D" , "Recv Loop Exception : {}".format(e))
                    continue
                if( Data["ret"] == True) :
                    # Handle Diag Ack
                    # Diagnostics Ack (ACK in doip . i think)
                    if( ( Data["type"] == 0x8002 )  ) :
                        self.log(subTag, "D" , "Diag Ack : {}".format( Data["AckCode"]) )
                        # DiagAck Pakcet is over 13 (chained packet)
                        if( len(rcvdata) > 13 ) :
                            rcvdata2 = rcvdata[13:]
                            Data = self.parseUDSPacket( 0, rcvdata2 )
                    # UDS Command is received
                    if ( ( Data["type"] == 0x8001 ) ) :
                        udscode = hex(Data["UDSCode"]).upper()
                        udssubcode = hex(Data["UDSSubCode"]).upper()
                        self.log(subTag, "D" , "UDS-Cmd:{} SubCmd:{} ".format( udscode , udssubcode ) )
                        if( (udscode == "0X7F") and ( udssubcode == "0X3178" )) :
                            self.log(subTag, "D" , " UDS is pending "  )
                        elif ((udscode == "0X7F") and (udssubcode == "0X2221")):
                            self.log(subTag, "E" , " Busy Repeat "  )
                            self.delayUDS_self(0.2)
                            self.testcase_resend()
                        elif ( udscode == "0X7F" ) :
                            self.log(subTag, "E", " UDS is Failed ")
                            self.testStatus["status"] = "FAIL"
                            self.testStatus["info"] = {}
                            self.testStatus["info"]["time"] = self.stopwatch.diff()
                        else :
                            if udscode == "0X62" :
                                if udssubcode == "0XF111" :
                                    self.log(subTag, "I", "Reading DID Result : {}".format(rcvdata[-24:]))
                                    if self.isAutomationTest == True:
                                        if ((self.testStatus["name"] == "F111") and (
                                                self.testStatus["status"] == "RUNNING")):
                                            self.testcase_snapshot( rcvdata[-24:-24 + 16] )
                                elif udssubcode == "0XF113" :
                                    self.log(subTag, "I", "Reading DID Result : {}".format(rcvdata[-24:]))
                                    if (self.isAutomationTest == True):
                                        if ((self.testStatus["name"] == "F113") and (
                                                self.testStatus["status"] == "RUNNING")):
                                            self.testcase_snapshot( rcvdata[-24:-24 + 16] )
                                elif udssubcode == "0XF188" :
                                    self.log(subTag, "I", "Reading DID Result : {}".format(rcvdata[-24:]))
                                    if (self.isAutomationTest == True):
                                        if ((self.testStatus["name"] == "F188") and (
                                                self.testStatus["status"] == "RUNNING")):
                                            self.testcase_snapshot(rcvdata[-24:-24 + 16+1])
                                elif udssubcode == "0XF18C" :
                                    self.log(subTag, "I", "Reading DID Result : {}".format(rcvdata[-16:]))
                                    if (self.isAutomationTest == True):
                                        if ((self.testStatus["name"] == "F18C") and (
                                                self.testStatus["status"] == "RUNNING")):
                                            self.testcase_snapshot(rcvdata[-16:-16+13])
                                elif udssubcode == "0XF1BE" :
                                    self.log(subTag, "I", "Reading DID Result : {}".format(rcvdata[-64:]))
                                    if (self.isAutomationTest == True):
                                        if ((self.testStatus["name"] == "F1BE") and (self.testStatus["status"] == "RUNNING")):
                                            if (self.isAllZero(rcvdata[-64:])) :
                                                if (self.stopwatch.diff() > self.config["DID_TIMEOUT_SEC"] ):
                                                    self.testcase_snapshot( rcvdata[-64:-64 + 8] )
                                                else:
                                                    self.delayUDS1S()
                                                    self.testcase_resend()
                                            else:
                                                self.testcase_snapshot( rcvdata[-64:-64 + 8] )
                                elif udssubcode == "0XF1BF" :
                                    self.log(subTag, "I", "Reading DID Result : {}".format(rcvdata[-64:]))
                                    if (self.isAutomationTest == True):
                                        if ((self.testStatus["name"] == "F1BF") and (self.testStatus["status"] == "RUNNING")):
                                            if (self.isAllZero(rcvdata[-64:])):
                                                if (self.stopwatch.diff() > self.config["DID_TIMEOUT_SEC"] ):
                                                    self.testcase_snapshot(rcvdata[-64:-64 + 8])
                                                else:
                                                    self.delayUDS1S()
                                                    self.testcase_resend()
                                            else:
                                                self.testcase_snapshot(rcvdata[-64:-64 + 7])
                            elif udscode == "0X50" :
                                self.testcase_snapshot_ret( True )
                            elif udscode == "0X71":
                                self.testcase_snapshot_ret( True )
                            else :
                                self.log(subTag, "E", "Invalid Packet :: udscode:{}".format( udscode ))
                #self.log(subTag, "D", "loop rcv ..4 ")
                self.delayUDS()

            self.log(subTag, "D", "Close Socket 1")
            self.sockTCP.close()
            self.log(subTag, "D", "Close Socket 2")
            if( self.useGWM == True ) :
                self.sockTCP_GWM.close()
        self.log(subTag, "D", "End of Loop (Rcv)")

    # Information for test suite
        # interface
        # test style : step
    # function action :
        # command :
            # 1.CONNECT (useGWM : True, False )
            # 2.DID F111
                # Push Event To SendQueue
                # 3.DID F113
            # 4.DID F188
            # 5.DID F18C
            # 6.DID F1BE
            # 7.DID F1BF
            # 8.EXT SESSION
            # 9.RUN ODST
            # 10. Result Of ODST
        # param1
        # param2
    # function assertion :
        # READY, RUNNNIIG , DONE_FAIL, DONE_OK
        # status of test
            # ready : not running in command , can start new test casae
            # running : running in command
            # done : Fail
            # done : Succeed

    def Action( self , id , testcase , param ):
        subTag = "Action"
        # Run Testcase when ready
        if( self.testStatus["status"] == "READY" ) :
            # Update TestStatus
            self.log(subTag, "D", "READY")
            self.testStatus["id"] = id
            self.testStatus["name"] = testcase
            self.testStatus["status"] = "RUNNING"
            self.testStatus["param"] = param
            self.testStatus["info"] = {}
            self.log(subTag, "D" , "update action : {}".format(self.testStatus) )
            self.stopwatch.reset()
            # Run TestCase
            self.RunTestCase()
        else :
            self.log( subTag, "E" , "TestSuie : not ready : cur status {}".format( self.testStatus["status"] ))

    def Assertion( self  ):
        subTag = "Assertion"
        #self.log( subTag, "I" , "[Assertion--] is : Before{}".format( self.testStatus ) )
        while self.testStatus["status"] == "RUNNING":
            self.delayUDS()
        ret = self.testStatus.copy()
        jlruds.ReadyAction()
        self.log(subTag, "I", "[Assertion--] is : Ret{}".format(ret))
        return ret

    def RunTestCase( self ):
        subTag = "RunTestCase"
        self.log(subTag, "D", "TestStatus is :{}".format(self.testStatus))

        testname = self.testStatus["name"]
        param = self.testStatus["param"]

        # Change Statud to Running
        if( testname == "CONNECT" ) :
            self.testStatus["status"] = "RUNNING"
            self.foundPIVI()
        elif ( testname in self.TestList ) :
            self.testStatus["status"] = "RUNNING"
            test_packet = self.UDSCommands[ testname ]
            self.sockTCP.sendto(test_packet, self.PIVI_Addr)
        else :
            self.log(subTag, "I" , "RunTestCase" )

    def ReadyAction( self ) :
        self.testStatus["status"] = "READY"

    print("[JLR UDS Automation] v1.0")
    print("created by couragesuper.kim@lgepartner.com")
    # validataon parameters

if __name__ == '__main__' :
    if len(sys.argv) != 3:
        print("[Error] Usage> JLR_UDS_Automation [Config.xml] [TestCase.xml] ")
        exit(0)
    else:
        print("JLR_UDS_Automation : Config XML : {}".format(sys.argv[1]))
        print("JLR_UDS_Automation : TestCase XML : {}".format(sys.argv[2]))

        # check whether xml and file is existconnect

        lparam1 = sys.argv[1].lower()
        if (".xml" not in lparam1):
            print("xml-config isn't xml.")
            exit(0)
        elif os.path.exists(os.getcwd() + "/{}".format(lparam1)) == False:
            print("xml-config doesn't exist.")
            exit(0)

        lparam2 = sys.argv[2].lower()
        if (".xml" not in lparam2):
            print("testcase-config isn't xml.")
            exit(0)
        elif os.path.exists(os.getcwd() + "/{}".format(lparam2)) == False:
            print("testcase-config doesn't exist.")
            exit(0)

        # loading test case items
        test_cases = []
        xmltree = ET.parse(sys.argv[2])
        xmlroot = xmltree.getroot()
        if (xmlroot == None):
            print(subTag, "E", "Root node error.")
            exit(0)
            # L1
        for node in xmlroot:
            dict = {}
            dict["id"] = node.attrib["id"]
            dict["cmd"] = node.attrib["cmd"]
            dict["param"] = True if node.attrib["param"] else False
            test_cases.append(dict)

    if False:
        # make test case
        test_cases = [{"id": 1, "cmd": "CONNECT", "param": False},
                      {"id": 2, "cmd": "F111", "param": True},
                      {"id": 3, "cmd": "F113", "param": True},
                      {"id": 4, "cmd": "F188", "param": True},
                      {"id": 5, "cmd": "F18C", "param": True},
                      {"id": 6, "cmd": "F1BE", "param": True},
                      {"id": 7, "cmd": "F1BF", "param": True},
                      {"id": 8, "cmd": "EXTSESSION", "param": True},
                      {"id": 9, "cmd": "ODST", "param": True},
                      {"id": 10, "cmd": "ODST_RET", "param": True}]
        # running test cases
        # and asserting result of uds commands

    jlruds = JLR_UDS(sys.argv[1])

    for test_case in test_cases :
        jlruds.Action( test_case["id"], test_case["cmd"], test_case["param"])
        ret = jlruds.Assertion()
        print("assertion result : {}".format( ret ))

    jlruds.Close()
    time.sleep(2)
    print("==============\nEnd of Script\n")
else :
    print("this is import library")
    jlruds = JLR_UDS("Config.xml")

def ACTION_CONNECT() :
    jlruds.Action( 1,  "CONNECT", False )

def ACTION_F111() :
    jlruds.Action(2, "F111", True)

def ACTION_F113() :
    jlruds.Action(3, "F113", True)

def ACTION_F188() :
    jlruds.Action(4, "F188", True)

def ACTION_F18C() :
    jlruds.Action(5, "F18C", True)

def ACTION_F1BE() :
    jlruds.Action(6, "F1BE", True)

def ACTION_F1BF() :
    jlruds.Action(7, "F1BF", True)

def ACTION_EXTSESSION() :
    jlruds.Action(8, "EXTSESSION", True)

def ACTION_ODST() :
    jlruds.Action(9, "ODST", True)

def ACTION_ODST_RET() :
    jlruds.Action(10, "ODST_RET", True)

def ASSERTION() :
    ret = jlruds.Assertion()
    if( ('data' in ret['info'].keys()) and ('time' in ret['info'].keys()) ) : return ret['status'],ret['name'],ret['info']['time'],ret['info']['data']
    elif ('time' in ret['info'].keys()): return ret['status'], ret['name'], ret['info']['time']
    else : return ret['status'],ret['name'];

def CLOSE() :
    jlruds.Close()