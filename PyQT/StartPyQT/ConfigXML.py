from xml.etree import ElementTree as ET

xmltree = ET.parse( "config\OmsSTAUI.xml" )

# access top xml node
xmlroot = xmltree.getroot()
if (xmlroot == None):
    print("[Error] SQT Configuration file doesn't have not root.")
    exit(0)

print("---")
for menus in xmlroot :
    print( "{}".format(menus.attrib) )
    for menu in menus :
        print ( "\t{}".format(menu.attrib) )
