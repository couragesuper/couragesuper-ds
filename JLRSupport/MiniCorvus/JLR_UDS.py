    # for XML
from xml.etree import ElementTree as ET
    # socket
import socket
import threading
import time
    # for timestamp
from datetime import datetime

# Process List
    # 1. UDP broadcasting with VEH message (OK)
    # 2. UDP broadcasting with Routine message (OK)
    # 3. UDP Reading DID is failed ( error of payload )

# Goal : Direct Connection.
    # timeout of sending Vehicle identification
    # timeout of routing activation
    # timeout of reading did
    # error reading specified did

# Configuration : XML

xmlName = "Config.xml"

#Precondition : ba is valuable Array
def BaToVal( ba ) :
    value = 0
    if( type( ba ) == int ) : return True , ba
    if( len( ba ) > 4 ) :
         return False, ba
    for elem in ba :
        value = (value << 8) | elem
    return True, value

def ShowTs() :
    print( datetime.now() )

if False :
    config = LoadConfigXML( xmlName )
    print( config )

class UDS_Packet_Parser :
    def __init__( self , isDebug ):
        print( "[UDS_Packet_Parser] Init .. ")
        self.isDebug = True
        self.dictParseRule = {}
        self.debugTag = "UDS_Packet_Parser"

    def log(self, subTag, level, msg):
        print( "[{}][{}][{}] {}".format( self.debugTag, subTag, level,  msg ) )

    # RULE XML
        # L1 : DOIP or UDS (Protocols)
        # L2 : Packets
        # L3 : Fields
    def LoadRuleXML( self , xmlfile):
        # Debugging Data
        subTag = "LoadRuleXML"

        self.log(subTag, "I" , "[Parsing] Rule the XML")
        # parsing xml
        xmltree = ET.parse(xmlfile)
        xmlroot = xmltree.getroot()
        if (xmlroot == None):
            self.log( subTag , "E" , "LoadRuleXML .. Root")
            return False

        #L1
        for node_protocol in xmlroot:
            tag = node_protocol.tag
            self.log(subTag, "I", "\tnode L1 : {}".format(tag) )
            if( tag == "DOIP" ) :
                offset = 0
                for node_l1 in node_protocol :
                    arrayHdrInfo = {}
                    if( node_l1.attrib["name"] == "Header" ) :
                        self.log(subTag, "I", "\t\tnode L1:{}-> attr:{}".format(node_l1 , node_l1.attrib))
                        #L2
                        for node_l2 in node_l1 :
                            self.log(subTag, "I", "\t\t\tnode L2:{} -> attr:{}".format(node_l2, node_l2.attrib))
                            name = node_l2.attrib["name"]
                            len  = node_l2.attrib["len"]
                            arrayHdrInfo[ name ] = { "len" : int(len),  "offset": offset }
                            offset = int(offset) + int(len)
                    self.dictParseRule["DOIPHDR"] = arrayHdrInfo
            elif( tag == "UDS") :
                for node_l1 in node_protocol:
                    arrayUDSInfo = self.dictParseRule["DOIPHDR"].copy()
                    self.log(subTag, "I", "\t\tnode L1:{} -> attr:{}".format(node_l1 , node_l1.attrib))
                    packet_name = node_l1.attrib["name"]
                    packet_type = node_l1.attrib["doiptype"]
                    arrayUDSInfo["doiptype"] = packet_type
                    offset = 8
                    for node_l2 in node_l1 :
                        if( node_l2.tag != "DOIPHEADER" ) :
                            self.log(subTag, "I", "\t\t\tnode L2:{} -> attr:{}".format(node_l2, node_l2.attrib))
                            name = node_l2.attrib["name"]
                            len  = node_l2.attrib["len"]
                            arrayUDSInfo[name] = { "len" : int(len),  "offset": offset }
                            offset = int(offset) + int (len)
                        self.dictParseRule[packet_name] = arrayUDSInfo
            else:
                self.log( subTag , "E" , " Invalid Node ")

        if( self.isDebug == True ) :
            self.log(subTag, "I",  "[Display Nodes] ")
            for k , v  in self.dictParseRule.items() :
                self.log(subTag, "D" , "\t{} = {} ".format( k ,v ) )
        return True

    def getRuleData(self):
        return self.dictParseRule

if False :
    parser = UDS_Packet_Parser( self.isDebug )
    parser.LoadRuleXML("PacketParseRule.xml" )
    print( parser.getRuleData() )
    exit(0)

class JLR_UDS :
    def __init__(self):
        #1. Information
        self.debug = 1         # flag for function of some debug
        self.isDebug = True
        self.status = 0        # status flagging
        self.packet_len = 4096 # unit of transmission

        #2. JLR_UDS
        self.debugTag = "JLR_UDS"

        #3. XML Config
        self.config = {}

        #4. Status Flag
        self.resetFlag()
        self.InitPackets()

    def log(self, subTag, level, msg):
        print( "[{}][{}][{}] {}".format( self.debugTag, subTag, level,  msg ) )

    def resetFlag(self) :
        self.isFoundPIVI = False

    def InitPackets(self):
        subTag = "InitPackets"

        parser = UDS_Packet_Parser(self.isDebug)
        if( True == parser.LoadRuleXML("PacketParseRule.xml" ) ) :
            self.dict_udsRule = parser.getRuleData().copy()

        self.log( subTag, "I", "[Lists of packet data]" )
        self.UDSPackets = {}
        self.UDSPackets[ "VEH_REQ" ] = b'\x02\xfd\x00\x01\x00\x00\x00\x00'
        self.UDSPackets[ "ROUTINE_REQ"] = b'\x02\xfd\x00\x05\x00\x00\x00\x07\x0e\x80\x00\x00\x00\x00\x00'

        self.log(subTag, "I", "[Lists of doip types]")
        self.DOIPType = {}
        self.DOIPType["VEH_REQ"] = 1
        self.DOIPType["VEH_RES"] = 4
        self.DOIPType["ROU_REQ"] = 5
        self.DOIPType["ROU_RES"] = 6

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

    def LoadConfigXML( self , xml_file ):
        xmltree = ET.parse( xml_file )
        xmlroot = xmltree.getroot()
        if (xmlroot == None):
            print("[JLR_UDS][Error] LoadConfigXML .. Root ")
            return False
        for node in xmlroot:
            print( node.attrib )
            self.config["IP_ETH"] = node.attrib['IP_ETH']
            #self.config["IP"] = node.attrib['IP']
            self.config["PORT"] = int( node.attrib['PORT'] )
            #self.targetAddr = ( self.config["IP"], self.config["PORT"] )
            if( self.debug and 1 ) :
                print( "[JLR_UDS] LoadConfigXML .. Ret:{} ".format( self.config ) )

    def delayUDS(self) :
        time.sleep( 0.02 )

    # parsing byte through BaToVal ( 2 param )
        # msg is string (need to convert byte array)
    def parseUDSPacket(self , addr , msg):
        subTag = "parseUDSPacket"
        ba_pkt = bytearray( msg )
        data = {}
        if( len(ba_pkt) >= 8 ) :
            # found rule
            Ret, doipType = BaToVal(ba_pkt[2: 2 + 2])
            if( Ret == True ) :
                self.log( subTag, "I" , "DoipType = {}".format( doipType ) )
            else :
                self.log(subTag, "E", "DoipType")
            RetFound , rule = self.foundRule( doipType )
            if( RetFound == True ) :
                for rule_k, rule_v in rule.items() :
                    if( rule_k != "doiptype" ) :
                        #print("{} = {}".format(rule_k, rule_v))
                        off = int(rule_v["offset"])
                        length = int(rule_v["len"])
                        data[ rule_k ] = BaToVal( ba_pkt[off:off+length] )[1]
            else:
                self.log(subTag , "E" , "Found Rule Error -> Type : {}".format( doiptype ) )
        else :
            self.log(subTag , "E" , "Packet Error(short packet) -> len : {}".format( len( packet ) ) )
        self.log(subTag, "I", "\tParsed Data = {}".format( data ) )
        return data

    def foundRule(self ,doiptype):
        for key, rule in self.dict_udsRule.items() :
            if( key != "DOIPHDR" ) :
                type = int( rule["doiptype"] )
                if( doiptype == type ) : return True , rule
        return False , None


    # found PIVI and Connect PIVI
    def foundPIVI(self):
        # 1.unset flag whether PIVI is found

        # 2.Create UDP Socket to broadcast to found PIVI
        self.createUDPSocket()
        # 3.Create Sending Thread and Receiving Thread
        self.threadFoundPIVI_Send = threading.Thread( target = self.loopFoundPIVI_Send )
        self.threadFoundPIVI_Recv = threading.Thread( target = self.loopFoundPIVI_Recv )
        # 4 run Threads
        self.threadFoundPIVI_Send.start()
        self.threadFoundPIVI_Recv.start()

    # network
        # UDP socket : broad cast VEH message to all network .
            # pivi answers VEH response.
    def createUDPSocket(self):
        self.sockUDP = socket.socket( socket.AF_INET , socket.SOCK_DGRAM , socket.IPPROTO_UDP )
        self.sockUDP.setsockopt( socket.SOL_SOCKET , socket.SO_BROADCAST, 1 )
        self.sockUDP.bind( ( self.config["IP_ETH"], self.config["PORT"]) )

    # Protocol DOIP
            # make UDP socket
            # send VEH req : -> "VEH_REQ" (Doip 1)
            # recv VEH res : -> "VEH_RES" (Doip 4) -> set isFoundPIVI to True
            # close UDP socket
    def loopFoundPIVI_Send(self):
        # send vehicle identification message until pivi is answered.
        while self.isFoundPIVI == False :
            #self.log( "loopFoundPIVI_Send" , "I" , "Request Vehicle Identification" )
            self.sockUDP.sendto( self.UDSPackets[ "VEH_REQ" ], ("255.255.255.255", self.config["PORT"]) )
            self.delayUDS()

    def loopFoundPIVI_Recv(self):
        while self.isFoundPIVI == False :
            ShowTs()
            msg, addr = self.sockUDP.recvfrom(self.packet_len)
            #print("[loopFoundPIVI_Recv] msg:{0}, msglen:{2}, addr:{1}".format(msg, addr, len(msg)))
            if( addr[0] == self.config["IP_ETH"] ) :
                print("    [ignore] packet from self ")
            else :
                data = self.parseUDSPacket( addr , msg )
                # From PIVI
                if( ( data['type'] == self.DOIPType["VEH_RES"] ) and ( data['LogAddr'] == 0x14b4 )  ) :
                    self.PIVI_Addr = addr
                    #self.SavePIVIAddress();
                    self.PIVI_VEH  = data

                    self.sockUDP.close()
                    self.delayUDS()
                    self.isFoundPIVI = True
                else :
                    print(">> I don't know this message")
        self.CreateTCPSock()
        self.runLoopUDS()

    def CreateTCPSock(self):
        # Create TCP Coskcet
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockTCP.connect(self.PIVI_Addr)
 
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
        while self.isRecvRoutineActivation == False:
            ShowTs()
            self.log( subTag , "I" , " [Send] Routing Acitivation Reqeust" );
            self.sockTCP.sendto( self.UDSPackets["ROUTINE_REQ"], self.PIVI_Addr)
            self.delayUDS()

        cnt = 0
        # This is task after Activation
            # packets is required to send.
        while self.isUDSLoopRunning :
            ShowTs()
            if cnt < len(self.arrDIDPartNumbers):
                self.udsReadingDID(self.arrDIDPartNumbers[ cnt ])
                cnt = cnt + 1
            elif cnt == len(self.arrDIDPartNumbers):
                cnt = 0

    def udsReadingDID( self, did ):
        print( "sendReadingDID : did{} :type:{}".format(did , type(did)))
        if( type(did) == bytes ) :
            msg = b'\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4\x22'
            msg = msg + did
            print( "message:{}".format( msg )  )
            self.sockTCP.sendto( msg, self.PIVI_Addr )
            self.delayUDS()
        else :
            print( "sendReadingDID is failed with illegal param:{}".format( did ) )

    def loopUDS_Recv(self):
        subTag = "loopUDS_Recv"
        while self.isRecvRoutineActivation == False:
            msg = self.sockTCP.recv(self.packet_len)
            ShowTs()
            self.log( subTag  , "I" , " Data is received=len:{} data:{}".format(len(msg) ,  msg) )
            data = self.parseUDSPacket(0, msg)
            if ((data['type'] == self.DOIPType["ROU_RES"]) and (data['SourceAddr'] == 0x14b4) and (data['ResponseCode'] == 0x10)):
                ShowTs()
                print(">> >> Routing Activation ")
                self.isRecvRoutineActivation = True
            else:
                print("----")
            time.sleep(self.udsDelay)
        while True:
            rcvdata = self.sockTCP.recv(self.packet_len)
            print("[loopUDS_Recv] data={}".format(rcvdata))
            self.parseUDSDID(rcvdata)
            time.sleep(self.udsDelay)

# Module Test
if True :
    print("JLR_UDS ...")
    jlruds = JLR_UDS()
    jlruds.LoadConfigXML( xmlName )
    jlruds.foundPIVI()

