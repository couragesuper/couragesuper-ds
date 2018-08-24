from selenium import webdriver
import time
import os
import sys
from time import sleep
from mod_craw_logger import Crawler_Logger as LOGGER
from mod_craw_filewriter import crawler_filewriter as FT

sys.path.append("../Util")

from Util import helpPlatform

path_chrome_driver_linux = "/lib/chromedriver"
path_chrome_driver_win   = "\\lib\\chromedriver.exe"

class crawler_base :
    def __init__( self , isHidden, keyword_en ) :
        helperPlatform = helpPlatform()

        if( helperPlatform.platform == "linux" ) :
            self.isLinux = True
            self.isHidden = True
        elif ( helperPlatform.platform == "win" ) :
            self.isLinux = False
            self.isHidden = isHidden

        self.isLogger = False
        self.isTxt    = False
        self.createLogger(keyword_en , True)
        self.createTxt(keyword_en)
        curPath = os.path.dirname( os.path.abspath(__file__))
        if (self.isLinux):
            self.path_chrome_driver = curPath + path_chrome_driver_linux
        else:
            self.path_chrome_driver = curPath + path_chrome_driver_win
        if (self.isHidden):
            self.options = webdriver.ChromeOptions()
            self.options.add_argument('--headless')
            self.options.add_argument('--window-size=1920x1080')
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--no-sandbox")
            self.webDrv = webdriver.Chrome(self.path_chrome_driver, chrome_options=self.options)
        else:
            self.webDrv = webdriver.Chrome(self.path_chrome_driver)
        self.delay_dn = 1.5
    def createLogger( self , nameLogger , isDebug):
        self.logger = LOGGER( nameLogger +".xml" , isDebug)
        self.isLogger = True
    def createTxt( self , nameTxt ):
        self.txt = FT( nameTxt + ".txt")
        self.isTxt = True
    def setTxtColumn(self, listTxt ):
        for i,elem in enumerate( listTxt ):
            if( i != (len(listTxt) -1) ) : self.txt.write( listTxt[i] )
            else : self.txt.writeLast( listTxt[i] )
    def close(self):
        if( self.isLogger ) : self.logger.close()
        if( self.isTxt) : self.txt.close()
    def openPage(self, URL, delay=2.0):
        print( "  openpage = {}".format( URL ) )
        self.webDrv.get(URL)
        self.webDrv.implicitly_wait(delay)
    def run(self , mainUrl ):
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