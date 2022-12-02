
# Detect
#

# Sample for broadcast
# https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=happy_jhyo&logNo=70145362608

# send broadcast
# https://stackoverflow.com/questions/64066634/sending-broadcast-in-python


import socket

s1 = socket.socket( socket.AF_INET , socket.SOCK_DGRAM )
s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s1.bind(("" , 13400))
count = 0

while True :
    print( "waiting...." )
    msg, addr = s1.recvfrom(1024)
    print( "msg:{0} , msglen:{2} , addr:{1}".format(msg,addr,len(msg)) )
    print( "end of transmission count:{}".format(count) )
    count = count + 1

# Recevied Data Sample
# msg:b'\x02\xfd\x00\x04\x00\x00\x00!067L550JPJSV08v1M\x14\xb4\x02\x00\x86\x9f\xed<\x00\x00\x00\x00\x00\x00\x00\x00' , addr:('169.254.221.6', 13400)



