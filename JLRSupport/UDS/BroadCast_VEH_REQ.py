import socket

msg = b'\x02\xfd\x00\x01\x00\x00\x00\x00'

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(msg, ("255.255.255.255", 13400))

