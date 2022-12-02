#https://stackoverflow.com/questions/64066634/sending-broadcast-in-python

import socket
from time import sleep

# 1.BroadCast Socket
# Find Network Interface
# Send VEH Request to BroadCast
# Need to receive Routine Broadcast message


data2 = b'\x02\xfd\x00\x01\x00\x00\x00\x00'
msg = data2

def main():
    interfaces = socket.getaddrinfo( host = socket.gethostname(), port = None, family = socket.AF_INET)
    print( interfaces )

    allips = [ip[-1][0] for ip in interfaces]

    print( allips )
    # ip is listed with ipconfig command in prompt

    sock = {}
    for ip in allips:
        if ( '169' in ip ) :
            print(f'sending on {ip}')
            sock['ip'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
            sock['ip'].setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock['ip'].bind((ip,13400))

            #s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            #s1.bind(("", 13400))

            sock['ip'].sendto(msg, ("255.255.255.255", 13400))
            #msg1, addr2 = s1.recvfrom(1024)
            #print("{0}={1}".format(msg1, addr2))

            sock['ip'].close()
            sleep(1)
            #s1.close()
            sleep(1)

main()

