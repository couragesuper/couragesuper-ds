import socket
import threading

#NO DHCP
#NO POLL
#NO VEH

#TCP socket으로 PIVI에 접속하는 샘플

print( "Create and Connect " )

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
socket.connect( ( "169.254.115.244", 13400 ) );

# 응답이 없으면 끊어진다.

print( "Finish" )






