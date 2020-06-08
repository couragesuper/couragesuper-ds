import os
import sys
from xml.etree import ElementTree as ET


# XML을 생성합니다.
def updateXML( filename , listURLHistory ) :
    #1.File is exists
    if( os.path.exists( filename ) ) :
        xmltree = ET.parse(filename)
        xml_root = xmltree.getroot()
    else :
        xml_root = ET.Element('root')

    #2.History is exists
    history_node = xml_root.find('history')
    print( "history_node" , history_node )
    if (history_node == None) :
        history_node = ET.SubElement(xml_root, 'history')
        listnodes = {}
    else :
        listnodes = {node.attrib['url']: {'node': node, 'ret': node.attrib['ret'], 'url': node.attrib['url']} for node in history_node}
    print(listnodes)

    #3.
    for elem in listURLHistory:
        print( "" )
        if( elem['url'] in listnodes.keys() ) :
            print("-----")
            print( listnodes[elem['url']]['node'].attrib['ret'] )
        else :
            print("new nodes")
            new_node = ET.SubElement( history_node , 'elem_node' )
            # 새로 만들고 이것이 안되는 이유가 뭐여?
            new_node.set('ret', 'Fail')
            new_node.set('url', '000000')
            print(new_node.attrib)
    indent(xml_root)
    tree = ET.ElementTree(xml_root)
    tree.write( filename, encoding='utf-8' , xml_declaration= True)

class Crawler_Logger :
    def __init__(self, filename, isDebug ) :
        self.filename = filename
        self.isDebug  = isDebug
        if( os.path.exists( filename ) == True ) :
            if (self.isDebug): print("[Crawler_Logger] open existed file")
            self.xmltree = ET.parse(filename)
            self.xmlroot = self.xmltree.getroot()
        else :
            if (self.isDebug): print("[Crawler_Logger] create new file")
            self.xmlroot = ET.Element('root')
        history_node = self.xmlroot.find('histories')
        if (self.isDebug): print("[Crawler_Logger] history node:", history_node )
        if( history_node == None) :
            ET.SubElement( self.xmlroot , 'histories' )
    def updateHistory( self, url , ret ) :
        node_his = self.xmlroot.find("histories")
        node_history = node_his.find("history[@url='%s']" % (url) )
        if( node_history == None ) :
            history = ET.SubElement( node_his , 'history' )
            history.attrib['url'] = url
            history.attrib['ret'] = ret
            if (self.isDebug): print("[Crawler_Logger] history node:", history.attrib)
        else :
            node_history.attrib['ret'] = ret
    def getHistory(self , url, ret ):
        node_his = self.xmlroot.find("histories")
        node_history = node_his.find("history[@url='%s']" % (url))
        if( node_history == None ) :
            return { "check":"fail" }
        else :
            return { "check":"ok" , "ret": node_history['ret']}

    def updateXML(self) :
        #indent(self.xmlroot)
        tree = ET.ElementTree(self.xmlroot)
        tree.write(self.filename, encoding='utf-8', xml_declaration=True)

def rewrite( filename , filename2 ) :
    xmltree = ET.parse(filename)
    xmlroot = xmltree.getroot()
    indent( xmlroot )
    tree = ET.ElementTree( xmlroot )
    tree.write( filename2 , encoding='utf-8', xml_declaration=True)

def rewrite_update(filename ,filename2 ) :
    xmltree = ET.parse(filename)
    xmlroot = xmltree.getroot()
    his_node = xmlroot.find('histories')
    print(his_node.find("history[@url='aaa1']").attrib )
    print(his_node.find("history[@url='aaa2']").attrib )
    print(his_node.find("history[@url='aaa3']").attrib )
    print(his_node.find("history[@url='aaa4']").attrib )
    print(his_node.find("history[@url='aaa5']"))
    indent( xmlroot )
    tree = ET.ElementTree( xmlroot )
    tree.write( filename2 , encoding='utf-8', xml_declaration=True)

if True :
    craw_logger = Crawler_Logger( 'joins_bunsu_dae.xml' , True )
    craw_logger.updateHistory('aaa1','fail')
    craw_logger.updateHistory('aaa2','fail')
    craw_logger.updateHistory('aaa3','fail')
    craw_logger.updateHistory('aaa4','fail')
    craw_logger.updateXML()
else :
    rewrite_update( 'joins_bunsu_dae.xml' , 'joins_bunsu_dae_2.xml' )




