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
         return False, 0
    for elem in ba :
        value = (value << 8) | elem
    return True, value


def ShowTs() :
    print( datetime.now() )

if False :
    config = LoadConfigXML( xmlName )
    print( config )

class DID_Parser :
    def __init__(self):
        print( "DID Parser")

    def makePNList(self):
        self.aPN = []
        self.aPN.append(b'\xf1\x11')
        self.aPN.append(b'\xf1\x12')
        self.aPN.append(b'\xf1\x13')
        self.aPN.append(b'\xf1\x88')
        self.aPN.append(b'\xf1\x90')
        self.aPN.append(b'\xf1\xA0')
        self.aPN.append(b'\xf1\xBE')
        self.aPN.append(b'\x41\xAE')
        self.aPN.append(b'\x48\x84')




class Doip_Util :
    def __init__(self):
        self.debug = 1         # flag for function of some debug
        self.status = 0        # status flagging
        self.packet_len = 4096 # unit of transmission
        self.makeMessageList()

        # list of  dids.
        self.makePartNumberLists()
        # delay whenever perfoming operation of socket.
        self.udsDelay = 0.03

    def makePartNumberLists(self):
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

    def makeUDSCommand(self):
        self.arrUDSs = []
        self.arrUDSs.append( b'\x14\xff\xff\xff')
        self.arrUDSs.append( b'\x3E\x00') # testor present
        print( self.arrUDSs )

    def makeUDSRouinte(self):
        self.arrUDSs.append( b'\x31\x01\x02\x02')
        print( self.arrUDSs )

    def makeMessageList(self):
        self.message = {}
        self.message["VEH_REQ"] = b'\x02\xfd\x00\x01\x00\x00\x00\x00'

    def LoadConfigXML( self , filename ):
        self.config = {}
        xmltree = ET.parse(filename)
        xmlroot = xmltree.getroot()
        if (xmlroot == None):
            print("[Error] LoadConfigXML :: root error ")
            return 1
        for node in xmlroot:
            print(node)
            print(node.tag)
            self.config["IP_ETH"] = node.attrib['IP_ETH']
            #self.config["IP"] = node.attrib['IP']
            self.config["PORT"] = int( node.attrib['PORT'] )
            #self.targetAddr = ( self.config["IP"], self.config["PORT"] )
            if( self.debug and 1 ) : print( self.config )
            self.status = 1
        print( self.config )

    def Handle_VEH_Message(self , addr , msg ):
        isDebug = False
        ba = bytearray ( msg )
        dict_data = {}
        dict_ret = {}
        if( isDebug ) : print( "[Handle_VEH_Message] Handle DOIP Message \n ")

        # for 4 VEH Reqponse
            #1. names of field
        arr_Field = ['type', 'len' , 'vin' , 'la' , 'eid' ,'gid' ,'rev1' ,'rev2']
            #2. datas of offset and length
        dict_data['type_off'] = 2
        dict_data['type_len'] = 2
        dict_data['len_off'] = 4
        dict_data['len_len'] = 4
        dict_data['vin_off'] = 8
        dict_data['vin_len'] = 17
        dict_data['la_off'] = 25
        dict_data['la_len'] = 2
        dict_data['eid_off'] = 27
        dict_data['eid_len'] = 6
        dict_data['gid_off'] = 33
        dict_data['gid_len'] = 6
        dict_data['rev1_off'] = 39
        dict_data['rev1_len'] = 1
        dict_data['rev2_off'] = 40
        dict_data['rev2_len'] = 1

        if( ( ba[0] == 0x2 ) and ( ba[1] == 0xfd ) ) :
            # 1. preprocessing data
            for elem in arr_Field :
                off = dict_data[ elem + "_off" ]
                len = dict_data[ elem + "_len" ]
                dict_ret[ elem ] = ba[off : off + len]
                if( isDebug ) : print( "off:{0} len:{1} data:{2}".format(off,len,ba[ off : off+ len ]))
            if( isDebug ) : print( dict_ret )
        # post processing
        dict_ret['len']  = BaToVal(dict_ret['len'] )[1]
        dict_ret['type'] = BaToVal(dict_ret['type'])[1]
        dict_ret['la']   = BaToVal(dict_ret['la']  )[1]
        return dict_ret

    def Handle_RoutingActivation_Message(self , addr , msg ):
        isDebug = True
        ba = bytearray ( msg )
        dict_data = {}
        dict_ret = {}
        if( isDebug ) : print( "[Handle_VEH_Message] Handle DOIP Message \n ")

        # for 4 VEH Reqponse
            #1. names of field
        arr_Field = ['type', 'len' , 'la_testor' , 'sa' , 'routing_rescode' ,'revISO' ,'revOEM' ,'VSS']

            #2. datas of offset and length
        dict_data['type_off'] = 2
        dict_data['type_len'] = 2
        dict_data['len_off'] = 4
        dict_data['len_len'] = 4

        dict_data['la_testor_off'] = 8
        dict_data['la_testor_len'] = 2
        dict_data['sa_off'] = 10
        dict_data['sa_len'] = 2
        dict_data['routing_rescode_off'] = 12
        dict_data['routing_rescode_len'] = 1

        dict_data['revISO_off'] = 13
        dict_data['revISO_len'] = 4
        dict_data['revOEM_off'] = 17
        dict_data['revOEM_len'] = 4
        dict_data['VSS_off'] = 21
        dict_data['VSS_len'] = 1

        if( ( ba[0] == 0x2 ) and ( ba[1] == 0xfd ) ) :
            # 1. preprocessing data
            for elem in arr_Field :
                off = dict_data[ elem + "_off" ]
                len = dict_data[ elem + "_len" ]
                dict_ret[ elem ] = ba[off : off + len]
                if( isDebug ) : print( "off:{0} len:{1} data:{2}".format(off,len,ba[ off : off+ len ]))

            # 2. some field to integer.
            if( isDebug ) : print( dict_ret )

        dict_ret['len'] = BaToVal(dict_ret['len'])[1]
        dict_ret['type'] = BaToVal(dict_ret['type'])[1]
        dict_ret['sa'] = BaToVal(dict_ret['sa'])[1]
        dict_ret['routing_rescode'] = BaToVal(dict_ret['routing_rescode'])[1]
        return dict_ret

    def parseUDSDID ( self , packet ) :
        dict_Data = {}
        print( "[parseUDSDID] packet:{}\n\tdid:{}".format( packet , packet[12:] ) )
        dict_Data ['did_ret'] = packet[12:]
        return dict_Data

    def FoundPIVI(self):
        # 1.unset flag whether PIVI is founded
        self.isFoundPIVI = False;
        ShowTs()
        # 2.Create UDP Socket to broadcast to found PIVI
        self.Create_UDP_Socket()
        # 3.Create Sending Thread and Receiving Thread
        self.threadFoundPIVI_Send = threading.Thread( target = self.loopFoundPIVI_Send )
        self.threadFoundPIVI_Recv = threading.Thread( target = self.loopFoundPIVI_Recv )
        self.threadFoundPIVI_Send.start()
        self.threadFoundPIVI_Recv.start()

    def Create_UDP_Socket(self):
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.sockUDP.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # config UDP Socket with Configuration of XML
            # IP_ETH : IP address of ethernet device has vlan configuration
        self.sockUDP.bind(( self.config["IP_ETH"], self.config["PORT"]))

    def loopFoundPIVI_Send(self):
        # send vehicle identification message until pivi is answered.
        while self.isFoundPIVI == False :
            ShowTs()
            print("loopFoundPIVI_Send] Request Vehicle Identification {}".format( self.config ) )
            msg = b'\x02\xfd\x00\x01\x00\x00\x00\x00'
            self.sockUDP.sendto(msg, ("255.255.255.255", self.config["PORT"]))
            time.sleep(self.udsDelay)

    def loopFoundPIVI_Recv(self):
        while self.isFoundPIVI == False :
            ShowTs()
            msg, addr = self.sockUDP.recvfrom(self.packet_len)
            print("[loopFoundPIVI_Recv] msg:{0}, msglen:{2}, addr:{1}".format(msg, addr, len(msg)))
            if( addr[0] == self.config["IP_ETH"] ) : print("    [ignore] packet from self ")
            else :
                data = self.Handle_VEH_Message( addr , msg )
                # From PIVI
                if( ( data['type'] == 0x4 ) and ( data['la'] == 0x14b4) ) :
                    self.PIVI_Addr = addr
                    self.SavePIVIAddress();
                    self.PIVI_VEH  = data
                    #self.Create_PIVI_Socket()
                    self.sockUDP.close()
                    time.sleep(self.udsDelay)
                    self.isFoundPIVI = True
                else :
                    print(">> I don't know this message")

        self.CreateTCPSock()
        self.runLoopTCP()

    def SavePIVIAddress(self):
        print(" SavePIVIAddress = Found PIVI addr:{} port:{}".format( self.PIVI_Addr[0] , self.PIVI_Addr[1] ) )

    def CreateTCPSock(self):
        #Create TCP Coskcet
        self.sockTCP = socket.socket(socket.AF_INET , socket.SOCK_STREAM )
        self.sockTCP.connect( self.PIVI_Addr )

    def runLoopTCP(self):
        print( "runLoopTCP" )
        self.isRecvRoutineActivation = False;
        self.threadTCP_Send = threading.Thread(target = self.loopUDS_Send )
        self.threadTCP_Send.start()
        self.threadTCPRecv = threading.Thread( target = self.loopUDS_Recv )
        self.threadTCPRecv.start()

    def loopUDS_Send(self):
        while self.isRecvRoutineActivation == False :
            ShowTs()
            print("Send Loop : Send Routine Acitvation")
            msg = b'\x02\xfd\x00\x05\x00\x00\x00\x07\x0e\x80\x00\x00\x00\x00\x00'
            self.sockTCP.sendto(msg, self.PIVI_Addr)
            time.sleep(self.udsDelay)
            self.cnt = 0
        while True :
            ShowTs()
            if False :
                print("Send Loop : Reading DID F111 ... ")
                #msg = b'\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4\x22\xf1\x11'
                self.udsReadingDID( b'\xf1\x11' )
                #self.sockTCP.sendto(msg, self.PIVI_Addr)
                time.sleep(self.udsDelay)
            else :
                if self.cnt < len(self.arrDIDPartNumbers) :
                    self.udsReadingDID( self.arrDIDPartNumbers[self.cnt] )
                    self.cnt = self.cnt + 1
                elif self.cnt == len(self.arrDIDPartNumbers) :
                    self.cnt = 0

    def loopUDS_Recv(self):
        while self.isRecvRoutineActivation == False:
            rcvdata = self.sockTCP.recv(self.packet_len)
            ShowTs()
            print("[loopUDS_Recv] data={}".format(rcvdata))
            data = self.Handle_RoutingActivation_Message(0, rcvdata)
            if ((data['type'] == 0x6) and (data['sa'] == 0x14b4) and (data['routing_rescode'] == 0x10)):
                ShowTs()
                print(">> >> Routing Activation ")
                self.isRecvRoutineActivation = True
            else:
                print("----")
            time.sleep(self.udsDelay)
        while True:
            rcvdata = self.sockTCP.recv(self.packet_len)
            print("[loopUDS_Recv] data={}".format(rcvdata))
            self.parseUDSDID( rcvdata )
            time.sleep( self.udsDelay )

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

    def udsClearDTCAll(self):
        udsClearDtcAll =  b'\x14\xff\xff\xff'
        self.sockTCP.sendto( msg, self.PIVI_Addr )
        time.sleep(self.udsDelay)

    def udsTestorPresent(self):
        msg = b'\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4\x0E\x00'
        self.sockTCP.sendto( msg, self.PIVIV_Addr )
        time.sleep(self.udsDelay)

    def udsStartRoutnie ( self , cmd ):
        msg = b'\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4'
        msg_send = msg + cmd
        self.sockTCP.sendto( msg_send , self.PIVI_Addr )
        time.sleep(self.udsDelay)

    def readDTCs (self ):
        print( "readDTCs : read all result of dtcs ")
        msg = b'\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4\x22'
        self.sockTCP.sendto( msg , self.PIVI_Addr )

doip = Doip_Util()
doip.LoadConfigXML( xmlName )

doip.FoundPIVI()

#work to do
    # uds command is received