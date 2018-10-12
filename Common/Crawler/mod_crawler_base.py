from   selenium import webdriver
import platform
import time
import os
import re
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
    def setIterColumn(self , idx ):
        self.idx = idx
    def __iter__(self):
        line = self.fobj.readline()
        while (line):
            listLine = line.split("\t")
            if( self.isSentence == False ) :  yield line
            else :
                yield listLine[self.idx]
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
        return False
    def getMaxPagesHistory(self):
        node_max_history = self.xmlroot.find("maxpage")
        if( node_max_history == None ) :
            return 0
        else :
            return int( node_max_history.attrib['value'] )
    def updatePageHistory(self , maxValue ):
        node_max_history = self.xmlroot.find("maxpage")
        if (node_max_history == None):
            node_max_history = ET.SubElement( self.xmlroot ,  'maxpage')
        node_max_history.attrib['value'] = str(maxValue)
        self.close()
    def writeColumnInfo(self,listColumn):
        #create columns field
        node_columns = self.xmlroot.find('columns')
        if(node_columns != None):
            if (self.isDebug):
                print("[Crawler_Logger] list column:", column_node)
        if (node_columns == None):
            node_columns = ET.SubElement(self.xmlroot, 'columns')
        for idx,column in enumerate( listColumn ):
            node_column = node_columns.find("column[@id='%d']" % (idx))
            if( node_column == None ):
                node_column = ET.SubElement(node_columns, 'column')
                node_column.attrib['id'] = str(idx)
                node_column.attrib['name'] = str(column)
        self.close()
    def getColumnInfo(self):
        listColumns = []
        columns_node = self.xmlroot.find('columns')
        for column_node in columns_node:
            listColumns.append( column_node.attrib['name'] )
        return listColumns
    def close(self) :
        proc_xml_indent(self.xmlroot)
        tree = ET.ElementTree(self.xmlroot)
        tree.write(self.filename, encoding='utf-8', xml_declaration=True)


class DocPreprocessor :
    def __init__(self):
        self.listBrackets = [("\(", "\)"), ("\[", "\]"), ("［", "］"), ("【", "】"), ("<", ">"), ("＜", "＞"), ("{", "}"),
                            ("＜", "＞"), ("『", "』")]
        self.listSymToRemove = list("\"\'?!#＂,.`‘’’“▶”")
        self.listSymToEmpty = list("·/…∼~")
    def removeBlocks(self,s):
        for elem_tuple in self.listBrackets:
            reg_exp = "%s[^%s]*?%s" % (elem_tuple[0], elem_tuple[0], elem_tuple[1])
            while True:
                s_new = re.sub(reg_exp, '', s)
                if s_new == s:
                    break
                s = s_new
        return s

    def removeChars(self,s):
        for ch in self.listSymToRemove:
            s = s.replace(str(ch), "")
        return s
    def replaceEmpty(self,s):
        for ch in self.listSymToEmpty:
            s = s.replace(str(ch), " ")
        return s
    # 괄호안의 언어들이 단어라면, 추가하는 것도 좋겠음.


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
        if( self.isLogger ) : self.logger.writeColumnInfo(listTxt)
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

# version2
# make strucuture to be simply
    # 3 step
        # run
            # fetch
            # scrape & save
    # save file has type of csv
class crawler_engine :
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
    # cretae external device
    def createLogger( self , pathnameLogger , isDebug):
        self.logger = craw_history_logger( pathnameLogger +".xml" , isDebug)
        self.isLogger = True
    def createTxt( self , pathnameTxt ):
        self.txt = craw_file_writer( pathnameTxt + ".txt")
        self.isTxt = True
    def setTxtColumn(self, listTxt ):
        if( self.isLogger ) : self.logger.writeColumnInfo(listTxt)
    # close
    def close(self):
        if( self.isLogger ) : self.logger.close()
        if( self.isTxt) : self.txt.close()
    # web driver function
    def openPage(self, URL, delay=2.0):
        try :
            print( "[crawler_base] openPage = {}".format( URL ) )
            self.webDrv.get(URL)
            self.webDrv.implicitly_wait(delay)
        except :
            print("[crawler][base] with URL ".format(URL))
    def run(self ):
        print( "  [crawler_base] run()" )
        #self.fetch()
        return
    def fetch(self):
        # scrape
        return
    def scrape(self):
        #save
        return
    def save(self):
        return
