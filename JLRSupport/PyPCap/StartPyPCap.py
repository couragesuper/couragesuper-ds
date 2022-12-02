import pyshark

#    cap = pyshark.FileCapture("test.pcap")
#    print( cap[0] )
#    print( type(cap[1]) )

if False :
    capture = pyshark.LiveCapture(interface='eth0')
    capture.sniff(timeout=50)
    capture

if True:
    capture = pyshark.FileCapture("test.pcap")
    #print( capture[0] )
    print( type( capture[0]) )
    print( len(capture[0]))

    id = 0
    for i in capture[0] :
        id = id + 1
        print( "id:{0} entry:{1}".format(id,i) )


