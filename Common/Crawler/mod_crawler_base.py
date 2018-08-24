from selenium import webdriver
import platform
import time
import os
import sys
from time import sleep
from mod_craw_logger import Crawler_Logger as LOGGER
from mod_craw_filewriter import crawler_filewriter as FT

path_chrome_driver_linux = "/lib/chromedriver"
path_chrome_driver_win   = "\\lib\\chromedriver.exe"

def get_platform():
    if platform.system() == 'Linux' :
        return "linux"
    elif platform.system() == 'Darwin' :
        return "apple"
    elif platform.system() == "Windows" :
        return "win"
    return "unknown"

class crawler_base :
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
        self.logger = LOGGER( pathnameLogger +".xml" , isDebug)
        self.isLogger = True
    def createTxt( self , pathnameTxt ):
        self.txt = FT( pathnameTxt + ".txt")
        self.isTxt = True
    def setTxtColumn(self, listTxt ):
        for i,elem in enumerate( listTxt ):
            if( i != (len(listTxt) -1) ) : self.txt.write( listTxt[i] )
            else : self.txt.writeLast( listTxt[i] )
    def close(self):
        if( self.isLogger ) : self.logger.close()
        if( self.isTxt) : self.txt.close()
    def openPage(self, URL, delay=2.0):
        print( "  [crawler_base] openPage = {}".format( URL ) )
        self.webDrv.get(URL)
        self.webDrv.implicitly_wait(delay)
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