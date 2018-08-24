from   selenium import webdriver
import platform
import time
import os
import sys
from time      import sleep
from xml.etree import ElementTree as ET

path_chrome_driver_linux = "/lib/chromedriver"
path_chrome_driver_win   = "\\lib\\chromedriver.exe"

# crawler common api
#   initalize the web driver
def InitWebDriver(isLinux=False, isHidden=False):
    curPath = os.path.dirname(os.path.abspath(__file__))
    if (isLinux):
        path_chrome_driver = curPath + path_chrome_driver_linux
    else:
        path_chrome_driver = curPath + path_chrome_driver_win
    if (isHidden):
        options = webdriver.ChromeOptions()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920x1080')
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        webDrv = webdriver.Chrome(path_chrome_driver, chrome_options=options)
    else :
        webDrv = webdriver.Chrome(path_chrome_driver)
    return webDrv

#   open the web page
def OpenWebPage(webDrv, URL, delay=2.0):
    webDrv.get(URL)
    webDrv.implicitly_wait(delay)

#   get platform types
def get_platform():
    if platform.system() == 'Linux' :
        return "linux"
    elif platform.system() == 'Darwin' :
        return "apple"
    elif platform.system() == "Windows" :
        return "win"
    return "unknown"

#   process the indent of xml
def proc_xml_indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            proc_xml_indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

#   Usage
#   writer = craw_filewriter( "Test.txt" )
#
#       setFeatures() : contents in line content
#       write() :  write the feature in line
#                   this api doesnt check the number of entry
#       writeLast() : make new lines
#
#       -- basic features components :
class craw_file_writer :
    def __init__(self, fileName ):
        self.fobj = open( fileName , "a+", encoding='utf-8')
        self._isFirst = False
        if( os.path.getsize (fileName) == 0 ) : self._isFirst = True
    def close(self):
        self.fobj.close()
    def setFeatures(self, listFeat ):
        self.listFeat = listFeat
        for feat in listFeat :
            self.fobj.write( feat )
            self.fobj.write( "\t")
        self.fobj.write("\n")
    def write(self, entry):
        self.fobj.write(entry)
        self.fobj.write("\t")
    def writeLast(self, entry):
        self.fobj.write(entry)
        self.fobj.write("\n")
    def isFirst(self ):
        return self._isFirst

#   Usage
#   writer = craw_file_reader( "corpus.txt" , isOnlySentence  )
class craw_file_reader:
    def __init__(self, corpus_fname, onlySentence):
        self.corpus_fname = corpus_fname
        self.fobj = open(self.corpus_fname, 'r', encoding='utf-8')
        # read first line
        line = self.fobj.readline()
        listCols = line.replace("\n", "").split("\t")
        # print(listCols)
        self.isSentence = onlySentence
    def __iter__(self):
        line = self.fobj.readline()
        while (line):
            listLine = line.split("\t")
            if (len(listLine) == 5):
                if (self.isSentence):
                    for i, sent in enumerate(listLine[4].split("  ")):
                        for sent_l2 in sent.split("."):
                            if (sent_l2 != ""): yield sent_l2
                else:
                    # doc
                    yield listLine[4]
            else:
                continue
            line = self.fobj.readline()

class craw_history_logger :
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
        # this makes to be easyily find url elements
        node_history = node_his.find("history[@url='%s']" % (url) )
        if( ret == False ) : szRet = "False"
        else : szRet = "True"
        if( node_history == None ) :
            node_history = ET.SubElement( node_his , 'history' )
            node_history.attrib['url'] = url
            if (self.isDebug): print("[Crawler_Logger] history node:", node_history.attrib)
        node_history.attrib['ret'] = szRet
    def getHistory(self , url ):
        print("[craw_history_logger] url={}".format(url))
        node_his = self.xmlroot.find("histories")
        node_history = node_his.find("history[@url='%s']" % (url))
        if( (node_history != None) and (node_history.attrib['ret'] == "True") ) :
            return True
        return False;
    def close(self) :
        proc_xml_indent(self.xmlroot)
        tree = ET.ElementTree(self.xmlroot)
        tree.write(self.filename, encoding='utf-8', xml_declaration=True)

class craw_base :
    def __init__( self , isHidden, outDir , title ) :
        szPlatform = get_platform()
        print( "[crawler_base] platform is identified with {} ".format(szPlatform) );
        if( szPlatform == "linux" ) :
            self.isLinux = True
            self.isHidden = True
        elif ( szPlatform == "win" ) :
            self.isLinux = False
            self.isHidden = isHidden
        self.isLogger = False
        self.isTxt    = False
        self.createLogger( outDir + "/"  + title , True )
        self.createTxt( outDir + "/" + title)
        curPath = os.path.dirname( os.path.abspath(__file__))
        if (self.isLinux):
            self.path_chrome_driver = curPath + path_chrome_driver_linux
        else:
            self.path_chrome_driver = curPath + path_chrome_driver_win
        print( "[crawler_base] path of chrome driver is {} ".format( self.path_chrome_driver ) );
        if (self.isHidden):
            print( "[crawler_base] chromdriver option is hidden" );
            self.options = webdriver.ChromeOptions()
            self.options.add_argument('--headless')
            self.options.add_argument('--window-size=1920x1080')
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--no-sandbox")
            self.webDrv = webdriver.Chrome(self.path_chrome_driver, chrome_options=self.options)
        else:
            self.webDrv = webdriver.Chrome(self.path_chrome_driver)
        self.delay_dn = 1.5
    def createLogger( self , pathnameLogger , isDebug):
        self.logger = craw_history_logger( pathnameLogger +".xml" , isDebug)
        self.isLogger = True
    def createTxt( self , pathnameTxt ):
        self.txt = craw_file_writer( pathnameTxt + ".txt")
        self.isTxt = True
    def setTxtColumn(self, listTxt ):
        if( self.txt.isFirst() ) :
            for i,elem in enumerate( listTxt ):
                if( i != (len(listTxt) -1) ) : self.txt.write( listTxt[i] )
                else : self.txt.writeLast( listTxt[i] )
    def close(self):
        if( self.isLogger ) : self.logger.close()
        if( self.isTxt) : self.txt.close()
    def openPage(self, URL, delay=2.0):
        try :
            print( "[crawler_base] openPage = {}".format( URL ) )
            self.webDrv.get(URL)
            self.webDrv.implicitly_wait(delay)
        except :
            print("[crawler][base] with URL ".format(URL))
    def run(self , mainUrl ):
        print( "  [crawler_base] run()" )
        self.openPage(mainUrl)
        self.login()
        self.makeCateLinks()
        self.naviSites()
        return
    def login(self):
        return
    def makeCateLinks(self):
        return
    def naviSites(self):
        return
    def navigate(self,links):
        return

print( "[MSG][Load Crawler Base Component]" )