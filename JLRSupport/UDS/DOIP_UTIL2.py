# for XML
from xml.etree import ElementTree as ET
# socket
import socket
import threading
import time # 접속 정보 설정

# 1. UDP broadcasting with VEH message (OK)
# 2. UDP broadcasting with Routine message (OK)
# 3. UDP Reading DID is faield ( payload error  TT TT TT )

xmlName = "Config.xml"

#precondition : ba is valuable array
def BaToVal( ba ) :
    value = 0
    if( type(ba) == int ) : return True , ba
    if( len(ba) > 4 ) :
         return False, 0
    for elem in ba :
        value = (value << 8) | elem
    return True, value

def LoadConfigXML( filename ) :
    config = {}
    xmltree = ET.parse( filename )
    xmlroot = xmltree.getroot()
    if (xmlroot == None):
        print("[Error] LoadConfigXML :: root error ")
        return 1
    for node in xmlroot:
        print(node)
        config["IP"] = node.attrib['IP']
        config["PORT"] = node.attrib['PORT']
    return config

if False :
    config = LoadConfigXML( xmlName )
    print( config )

class Doip_Util :
    def __init__(self):
        self.debug = 1  # flag for function of some debug
        self.status = 0 # status flagging
        self.packet_len = 4096 # unit of transmission
        self.client_status = 0 #
        self.makeMessageList()

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
            self.config["IP"] = node.attrib['IP']
            self.config["PORT"] = int( node.attrib['PORT'] )
            self.targetAddr = ( self.config["IP"], self.config["PORT"] )
            if( self.debug and 1 ) : print( self.config )
            self.status = 1

    # Create Socket to broadcast
        #Broad Casting Socket
            # UDP
            # PORT 13400
            # bind to : device
    def CreateSendBrSocket(self):
        self.BroadCastSendSokcet = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.BroadCastSendSokcet.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.BroadCastSendSokcet.bind(( self.config["IP_ETH"], 13400))


    def LoopSendRequestVehId(self):
        self.status = 1
        while True:
            if( self.status == 0 ) :
                # Send Vehicle Request
                print("Send Loop : Send Vehicle Identification")
                msg = b'\x02\xfd\x00\x01\x00\x00\x00\x00' # request vhehcile identification
                self.BroadCastSendSokcet.sendto(msg, ("255.255.255.255", 13400))
            elif( self.status == 1 ) :
                # request Routine Activation
                print("Send Loop : Send Routine Acitvation")
                msg = b'\x02\xfd\x00\x05\x00\x00\x00\x07\x0e\x80\x00\x00\x00\x00\x00'
                #self.BroadCastSendSokcet.sendto(msg, (self.PIVI_Addr[0], self.PIVI_Addr[1]))
                self.sockTCP.sendto( msg , self.PIVI_Addr )
            elif( self.status == 2 ) :
                print("Send Loop : Loop ")
                # read F111
                msg = b'\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4\x22\xf1\x11'
                self.sockTCP.sendto( msg, self.PIVI_Addr )
                time.sleep(4)
            time.sleep(3)

    def LoopPollRecv_TCP(self):
        while True :
            rcvdata = self.sockTCP.recv(self.packet_len)
            print( "[LoopPollRecv_TCP] data={}".format( rcvdata ) )
            time.sleep(1)
            if (self.status == 1 ):
                print("LoopPollRecv_TCP >> status 1 ")
                data = self.Handle_RoutingActivation_Message(0, rcvdata )
                print(data)
            # {'type': 6, 'len': 13, 'la_testor': bytearray(b'\x0e\x80'), 'sa': 5300, 'routing_rescode': bytearray(b'\x10'), 'revISO': bytearray(b'\x00\x00\x00\x00'), 'revOEM': bytearray(b'\x00\x00\x00\x00'), 'VSS': bytearray(b'')}
                if ((data['type'] == 0x6) and (data['sa'] == 0x14b4) and (data['routing_rescode'] == 0x10)):
                    print(">> >> Routing Activation ")
                    self.status = 2
                else:
                    print("why ? type:{0} sa:{1} rescode:{2}".format(data['type'], data['sa'], data['routing_rescode']))


    def LoopPollRecv(self):
        while True :
            msg, addr = self.BroadCastSendSokcet.recvfrom(self.packet_len)
            print("msg:{0} , msglen:{2} , addr:{1}".format(msg, addr, len(msg)))
            if( addr[0] == self.config["IP_ETH"] ) : print(">> from me")
            else :
                if( self.status == 0 ) :
                    print("LoopPollRecv >> status 0 ")
                    data = self.Handle_VEH_Message( addr , msg )
                    print( data )
                    if( ( data['type'] == 0x4 ) and ( data['la'] == 0x14b4) ) :
                        # Vehicle Identification Message is received
                        print(">> >> VEH Response is receieved from PIVI ")
                        self.PIVI_Addr = addr
                        self.PIVI_VEH = data
                            # create TCP Socket
                        self.Create_PIVI_Socket()
                        self.status = 1; # to send routine activation
                    else :
                        print(">> I don't know this message")

                elif( self.status == (1 + 100) ) :
                    print("LoopPollRecv >> status 1 ")
                    data = self.Handle_RoutingActivation_Message(addr,msg)
                    print(data)
                    #{'type': 6, 'len': 13, 'la_testor': bytearray(b'\x0e\x80'), 'sa': 5300, 'routing_rescode': bytearray(b'\x10'), 'revISO': bytearray(b'\x00\x00\x00\x00'), 'revOEM': bytearray(b'\x00\x00\x00\x00'), 'VSS': bytearray(b'')}

                    if( (data['type'] == 0x6) and (data['sa'] == 0x14b4) and (data['routing_rescode'] == 0x10 )) :
                        print(">> >> Routing Activation ")
                        self.status = 2
                    else : print( "why ? type:{0} sa:{1} rescode:{2}".format( data['type'] , data['sa'] , data['routing_rescode']) )
                elif( self.status == (2 + 100) ) :
                    print("LoopPollRecv >> status 2 ")
            time.sleep(0)

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
        dict_ret['len'] = BaToVal(dict_ret['len'])[1]
        dict_ret['type'] = BaToVal(dict_ret['type'])[1]
        dict_ret['la'] = BaToVal(dict_ret['la'])[1]
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

    def LoopPollRecv(self):
        while True :
            msg, addr = self.BroadCastSendSokcet.recvfrom(self.packet_len)
            print("msg:{0} , msglen:{2} , addr:{1}".format(msg, addr, len(msg)))
            if( addr[0] == self.config["IP_ETH"] ) : print(">> from me")
            else :
                if( self.status == 0 ) :
                    print("LoopPollRecv >> status 0 ")
                    data = self.Handle_VEH_Message( addr , msg )
                    print( data )
                    if( ( data['type'] == 0x4 ) and ( data['la'] == 0x14b4) ) :
                        print(">> >> VEH Response is receieved from PIVI ")
                        self.PIVI_Addr = addr
                        self.PIVI_VEH = data
                        self.Create_PIVI_Socket()
                        self.status = 1; # to send routine activation
                        return (0)
                    else :
                        print(">> I don't know this message")
                elif( self.status == 1 ) :
                    print("LoopPollRecv >> status 1 ")
                    data = self.Handle_RoutingActivation_Message(addr,msg)
                    print(data)
                    #{'type': 6, 'len': 13, 'la_testor': bytearray(b'\x0e\x80'), 'sa': 5300, 'routing_rescode': bytearray(b'\x10'), 'revISO': bytearray(b'\x00\x00\x00\x00'), 'revOEM': bytearray(b'\x00\x00\x00\x00'), 'VSS': bytearray(b'')}

                    if( (data['type'] == 0x6) and (data['sa'] == 0x14b4) and (data['routing_rescode'] == 0x10 )) :
                        print(">> >> Routing Activation ")
                        self.status = 2
                    else : print( "why ? type:{0} sa:{1} rescode:{2}".format( data['type'] , data['sa'] , data['routing_rescode']) )
                elif( self.status == 2 ) :
                    print("LoopPollRecv >> status 2 ")
            time.sleep(0)

    def LoopTCPRecv(self):
        while True :
            msg , addr = self.sock.recv( self.packet_len )

    # Create Client Socket
    def Create_PIVI_Socket(self):
        self.PIVI_Addr = ( '169.254.115.144',13400)
        self.sockTCP = socket.socket(socket.AF_INET , socket.SOCK_STREAM )
        self.sockTCP.connect( self.PIVI_Addr )

        self.threadSendBroadCast = threading.Thread(target=self.LoopSendRequestVehId)
        self.threadSendBroadCast.start()

        print( "[Create_PIVI_Socket] {}".format( self.PIVI_Addr ))
        self.threadTCPRecv = threading.Thread( target = self.LoopPollRecv_TCP )
        self.threadTCPRecv.start()

    # Listening VEH  - Socket and Threading
    def CreatePollBrSocket(self):
        self.BroadCastPollSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.BroadCastPollSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.BroadCastPollSocket.bind((self.config["IP_ETH"], 13400))

    def LoopPollVeh(self):
        while True:
            msg, addr = self.BroadCastPollSocket.recvfrom( self.packet_len )
            print("msg:{0} , msglen:{2} , addr:{1}".format(msg, addr, len(msg)))
            msg, addr = self.BroadCastPollSocket.recvfrom(self.packet_len)
            print("msg:{0} , msglen:{2} , addr:{1}".format(msg, addr, len(msg)))
            time.sleep(0)

    def RunVeh(self):
        if True :
            # Sending Thread
            self.CreateSendBrSocket()
            self.threadSendBroadCast = threading.Thread( target = self.LoopSendRequestVehId )
            self.threadSendBroadCast.start()

            # Polling to receive Thread
            self.threadRecvBroadCast = threading.Thread(target = self.LoopPollRecv)
            self.threadRecvBroadCast.start()

        if False :
            self.CreatePollBrSocket()
            self.threadPollRecvBroadCast = threading.Thread( target = self.LoopPollVeh )
            self.threadPollRecvBroadCast.start()

    def RunVeh2(self):
        self.Create_PIVI_Socket()

    def SendUDS_ReadDID_F111(self):
        while True :
            msg_send = b'\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4\x22\xf1\x11'
            ret = self.clientSocket.send(msg_send)
            msg, addr = self.clientSocket.recvfrom(1024)
            print( ret , msg, addr )
            time.sleep(1)

doip = Doip_Util()
doip.LoadConfigXML( xmlName )

doip.RunVeh2()



