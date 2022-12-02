import pyshark

#https://thepacketgeek.com/pyshark/packet-object/

cap = pyshark.FileCapture( "test.pcap")

# 'pyshark.packet.layers.xml_layer.XmlLayer'
print( dir( cap ))
print( dir( cap[0] ))
print( dir( cap[0].layers ))










