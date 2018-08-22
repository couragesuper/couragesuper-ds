import os
import sys
from  xml.etree import ElementTree as ET

#XML을 전달하면, 줄을 바꾸어 줍니다.
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
        if( ret == False ) : szRet = "False"
        else : szRet = "True"
        if( node_history == None ) :
            node_history = ET.SubElement( node_his , 'history' )
            node_history.attrib['url'] = url                    
            if (self.isDebug): print("[Crawler_Logger] history node:", history.attrib)        
        node_history.attrib['ret'] = szRet
    def getHistory(self , url ):
        node_his = self.xmlroot.find("histories")
        node_history = node_his.find("history[@url='%s']" % (url))
        if( node_history == None ) :
            return { "exist":False }
        else :
            valBool = True
            if( node_history.attrib['ret'] == "False" ) : valBool = False            
            return { "exist":True , "ret": valBool }
    def updateXML(self) :
        indent(self.xmlroot)
        tree = ET.ElementTree(self.xmlroot)
        tree.write(self.filename, encoding='utf-8', xml_declaration=True)