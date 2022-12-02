
#tcp conneciton

import socket
import time # 접속 정보 설정

eth_ip = '169.254.221.6'
ip = "169.254.115.144"
port = 13400
addr_tuple = ( ip , port )

pkt_len = 1024
index = 0


# 클라이언트 소켓 설정
sock = socket.socket( socket.AF_INET , socket.SOCK_STREAM )
sock.connect( addr_tuple )  # 서버에 접속

print("connection is succeed")

pkt = {}
pkt["veh_id_req"] = b'\x02\xfd\x00\x01\x00\x00\x00\x00'
pkt["routine_req"] = b'\x02\xfd\x00\x05\x00\x00\x00\x07\x0e\x80\x00\x00\x00\x00\x00'
pkt["read_f111"] = b'\x02\xfd\x80\x01\x00\x00\x00\x07\x0e\x80\x14\xb4\x22\xf1\x11'

while True :
    index = index + 1
    print("{}".format(index))

    sock.send( pkt["veh_id_req"] )
    msg = sock.recv(pkt_len)
    print("resp from server with vehicle id req: {}".format(msg))  # 서버로부터 응답받은 메시지 출력

    sock.send(pkt["routine_req"])
    msg = sock.recv(pkt_len)
    print("resp from server with routing activation: {}".format(msg))  # 서버로부터 응답받은 메시지 출력

    sock.send(pkt["read_f111"])
    msg = sock.recv(pkt_len)
    print("resp from server with reading did: {}".format(msg))  # 서버로부터 응답받은 메시지 출력

    time.sleep(1)