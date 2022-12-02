import pyshark

# https://thepacketgeek.com/pyshark/packet-object/

# Results
  # Durations for starting


# Helpers
def network_conversation(packet):
  try:
    protocol = packet.transport_layer
    source_address = packet.ip.src
    source_port = packet[packet.transport_layer].srcport
    destination_address = packet.ip.dst
    destination_port = packet[packet.transport_layer].dstport
    return (f'{protocol} {source_address}:{source_port} --> {destination_address}:{destination_port}')
  except AttributeError as e:
    pass
  except Exception as e:
    print( e )


def IsDoip ( packet ) :
  if ( ('DOIP' in packet)  ) : return True
  return False

def GetDoipKeys( packet ):
  return packet.doip._all_fields.keys()

def GetDoipValues( packet ):
  return packet.doip._all_fields.values()

def GetDoipValue( packet , key):
  if( key in  packet.doip._all_fields.keys() ) : return packet.doip._all_fields[key];
  return None

def IsAddress ( packet , address) :
  doipkeys = GetDoipKeys(  packet )
  if( ('doip.logical_address' in doipkeys ) and (address == packet.doip.logical_address )) : return True
  if (('doip.source_address' in doipkeys) and (address == packet.doip.source_address)): return True
  if (('doip.target_address' in doipkeys) and (address == packet.doip.target_address)): return True
  if (('doip.destination_address' in doipkeys) and (address == packet.doip.destination_address)): return True
  return False

def IsAddress_Check ( packet , address) :
  doipkeys = GetDoipKeys(  packet )
  ret = False
  if( ('doip.logical_address' in doipkeys )  ) : ret = True
  if (('doip.source_address' in doipkeys) ): ret = True
  if (('doip.target_address' in doipkeys) ): ret = True
  return ret


# Code
capture = pyshark.FileCapture('test_2.pcap')

print( "capture type:{} ".format( type(capture) ) )
print( "capture len:{}".format( len(capture) ) )

conversations = []
idx = 0

fp = open("output.txt" , "w+", encoding='UTF-8')

isConversationTest = False
hasDoip = False
isDoipTest = True

for packet in capture:
  idx  = idx + 1

  #print("\n\nidx:{} packet = {}".format(idx, packet))
  #fp.write(  "\n\nidx:{} packet = {}".format(idx, packet) )

  if isConversationTest :
    results = network_conversation(packet)
    if results != None:
      conversations.append(results)

  # how to access fields in xml
  if hasDoip :
    if( "DOIP" in packet ) :
      doip = packet
      # list all fields in doip packet
      #print( packet.doip._all_fields.keys() )
      if( "doip.logical_address" in  packet.doip._all_fields.keys() ) :
        #print( "doip la = {}".format(packet.doip.logical_address ) )
        if( packet.doip.logical_address == '0x14b4' ) : print("la")
      if ("doip.source_address" in packet.doip._all_fields.keys()):
        #print("doip sa = {}".format(packet.doip.source_address))
        if (packet.doip.source_address == '0x14b4'): print("sa")
      if ("doip.destination_address" in packet.doip._all_fields.keys()):
        #print("doip da = {}".format(packet.doip.destination_address))
        if (packet.doip.destination_address == '0x14b4'): print("da")
      if ("doip.target_address" in packet.doip._all_fields.keys()):
        #print("doip da = {}".format(packet.doip.destination_address))
        if (packet.doip.target_address == '0x14b4'): print("ta")
      #if( 'logical_address' in  packet.doip._all_fields.keys() ) : print("I'm here")
    #if("UDS" in packet) : print(packet.uds)

  if isDoipTest :
    if( IsDoip(packet) ) :
      if( IsAddress( packet , '0x14b4' )) :
        #print( GetDoipKeys(packet) , GetDoipValues(packet))
        #val = GetDoipValue(packet, 'doip.source_address')
        #if( val != None ) : print( val )
        print( packet.doip)
        #fp.write( str( packet.doip) )

fp.close()
# print( len(conversations) ) : 1648

# this sorts the conversations by protocol
# TCP and UDP
for item in sorted(conversations):
  print (item)








