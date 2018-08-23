import os
import sys
from xml.etree import ElementTree as ET

#reference
#https://fun25.co.kr/blog/python-xml-element-tree-example/?category=002
#https://wikidocs.net/42
#https://docs.python.org/2/library/xml.etree.elementtree.html
pathXMLFile = "D:\\Workspace\\config"
nameXMLFile = "UnifiedSDKConfig_UI.xml"

def LoadXMLConfig() :
    global xmltree
    xmltree  = ET.parse( pathXMLFile + "\\" +  nameXMLFile )
    xml_root = xmltree.getroot()
    print("xml_root : tag = {0} attrib ={1}".format( xml_root.tag, xml_root.attrib ))

    for child in xml_root :
        print("child : tag = {0} attrib ={1}".format(child.tag, child.attrib))

    #access the specified index
    if False :
        print(xml_root.find("VERSION").find("MAJOR").attrib)
        print(xml_root.find("VERSION").find("MINOR").attrib)

    TopicList = find_ret = xml_root.find("Synchronizer").find("TopicList")

    for child in TopicList :
        print("child : tag = {0} attrib ={1}".format(child.tag, child.attrib))

    Topic = xml_root.find( "Synchronizer" ).find("TopicList").find("Topic")
    for child in Topic:
        print("child : tag = {0} attrib ={1}".format(child.tag, child.attrib))
    return

def LoadXMLConfig_V2():
    global xmltree
    xmltree = ET.parse("UnifiedSDKConfig.xml")
    xml_root = xmltree.getroot()
    print("xml_root : tag = {0} attrib ={1}".format(xml_root.tag, xml_root.attrib))
    for child_l1 in xml_root:
        print("child l1 : tag = {0} attrib ={1}".format(child_l1.tag, child_l1.attrib))
        for child_l2 in child_l1:
            print("\tchild l2 : tag = {0} attrib ={1}".format(child_l2.tag, child_l2.attrib))
            for child_l3 in child_l2:
                print("\t\tchild l3 : tag = {0} attrib ={1}".format(child_l3.tag, child_l3.attrib))
                for child_l4 in child_l3:
                    print("\t\t\tchild l4 : tag = {0} attrib ={1}".format(child_l4.tag, child_l4.attrib))

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

class Crawling_History :

    def __init__( self , filepathname ):
        if( -1 == filepathname.lower().find(".xml") ) :
            filepathname_xml = filepathname + ".xml"
        if( False == os.path.isfile( filepathname ) ) :
            self.filepathname = filepathname
            self.iscreate = True
        else :
            self.xmltree = ET.parse( filepathname )
        self.dictConf = {}
        self.articles = []
    def setMxPage(self, maxpage):
        self.dictConf = {}
        self.dictConf['maxpage'] = int(maxpage)
    def getMaxPage(self):
        return self.dictConf['maxpage']
    def addPage(self, url, ret):
        return
    def update(self):
        self.dictConf = {}
        if( iscreate ) :
            rootNode = ET.Element('root')
            child['Config']   = ET.SubElement( rootNode , "Config" )
            child['Articles'] = ET.SubElement( rootNode , "Articles" )
            tree = ET.ElementTree(root)
            tree.write( filename )
        elif :
            xml_root = self.xmltree.getroot()
            for k,v in self.dictConf.getitem() :
                xml_root.find( k ).text = v

craw_his = Crawling_History( "create2.xml" )
craw_his.update()

def SaveXMLConfig( filename ) :
    global xmltree
    root = ET.Element("root")
    doc = ET.SubElement(root, "doc")
    ET.SubElement(doc, "field1", name="blah").text = "some value1"
    ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"
    tree = ET.ElementTree(root)
    tree.write( filename )

def createXMLConfig( filename ):
    # make root node
    rootNode = ET.Element('root')
    child_info  = ET.SubElement( rootNode, 'info')
    child_info_maxpage = ET.SubElement(child_info, 'maxpage')
    child_info_maxpage.attrib['a'] = 'b'
    child_info_maxpage.attrib['b'] = 'c'
    child_info_maxpage.attrib['c'] = 'd'
    tree = ET.ElementTree(rootNode)
    indent( rootNode )
    tree.write( filename , encoding="utf-8", xml_declaration=True )

#LoadXMLConfig()
SaveXMLConfig( "test.xml" )
createXMLConfig('create.xml')




