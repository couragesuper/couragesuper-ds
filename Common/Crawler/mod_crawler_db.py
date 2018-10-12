from   selenium import webdriver
import platform
import time
import os
import re
import sys
from time      import sleep
from xml.etree import ElementTree as ET

sys.path.append("../Mysql")
from libmysql import dbConMysql

path_chrome_driver_linux = "/lib/chromedriver"
path_chrome_driver_win   = "\\lib\\chromedriver.exe"

testdbconfig = { 'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'Crawling', 'raise_on_warnings': True,}

def get_platform():
    if platform.system() == 'Linux' :
        return "linux"
    elif platform.system() == 'Darwin' :
        return "apple"
    elif platform.system() == "Windows" :
        return "win"
    return "unknown"

class crawler_engine_db :
    def __init__( self , isHidden, dbInfo , contentIndex ):
        self.contentID = contentIndex
        # 1.get platform
        szPlatform = get_platform()
        print( "[crawler_base] platform is identified with {} ".format(szPlatform) );
        if( szPlatform == "linux" ) :
            self.isLinux = True
            self.isHidden = True
        elif ( szPlatform == "win" ) :
            self.isLinux = False
            self.isHidden = isHidden
        curPath = os.path.dirname( os.path.abspath(__file__))
        if (self.isLinux):
            self.path_chrome_driver = curPath + path_chrome_driver_linux
        else:
            self.path_chrome_driver = curPath + path_chrome_driver_win
        print( "[crawler_base] path of chrome driver is {} ".format( self.path_chrome_driver ) );
        # 2.Hidden
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
        self.openDB( dbInfo )

    def isExistData(self, Url, DataDate, Title ):
        qryAdd = ""
        isFirst = True
        if( Url != None ) :
            if( isFirst ) :
                qryAdd += " Where "
            else :
                qryAdd += " Or "
            qryAdd += "( Url = \"%s\" )" % Url
        if (DataDate != None):
            if (isFirst):
                qryAdd += " Where "
            else:
                qryAdd += " Or "
            qryAdd += "( DataDate = \"%s\" )" % DataDate
        if (Title != None):
            if (isFirst):
                qryAdd += " Where "
            else:
                qryAdd += " Or "
            qryAdd += "( Title = \"%s\" )" % Title
        qry = "Select COUNT(*) as CNT " \
              "From TB_CRAWLER_TEXTDATA" + qryAdd
        retList = self.db.selectQuery(qry)
        if( retList[0]["CNT"] != 0 ) : return True
        else : return False

    def isFailedData(self , url ):
        qry = "SELECT Count(*) as Cnt FROM TB_CRAWLER_TEXTDATA WHERE (url = \"%s\") and (Succeed = 0)" % (url)
        retList = self.db.selectQuery(qry)
        if (retList[0]["Cnt"] != 0):
            return True
        else:
            return False

    def updateData(self, url, IsSucceed, KeyWord , DataDate , Title , Author , TextData ):
        qry = "UPDATE TB_CRAWLER_TEXTDATA SET Keyword = \"%s\", DataDate = \"%s\", CrtDate = CurDate(), Title = \"%s\", Author = \"%s\", TextData = \"%s\", Succeed = %d WHERE url = \"%s\"" % (
        KeyWord, DataDate, Title, Author, TextData, 1,  url)
        try :
            self.db.commitQuery(qry)
        except:
            print("updateData :: exception ={}".format(qry))
        return False

    def writeData(self,  Url, IsSucceed, KeyWord = None, DataDate = None, Title = None, Author = None, TextData = None ):
        qryFinal = ""
        try :
            qry = "INSERT INTO TB_CRAWLER_TEXTDATA "
            qryField = "( IDX_CrawInfo , Url , CrtDate "
            qryValues  ="VALUES ( %d,  \"%s\" , CurDate() " % ( self.contentID,  Url )

            if( IsSucceed ) :
                qryField  += ", Succeed "
                qryValues += ", 1 "
                if( KeyWord != None ) :
                    qryField += ", Keyword "
                    qryValues += ", \"%s\" " % KeyWord
                if( Title != None ) :
                    qryField += ", Title "
                    qryValues += ", \"%s\" " % Title
                if( DataDate != None ) :
                    qryField += ", DataDate "
                    qryValues += ", \"%s\" " % DataDate
                if (Author != None):
                    qryField += ", Author "
                    qryValues += ", \"%s\" " % Author
                if( TextData != None ) :
                    qryField += ", TextData "
                    qryValues += ", \"%s\" " % TextData
            else :
                qryField += ", Succeed "
                qryValues += ", 0 "

            qryField += ") "
            qryValues += ")"
            qryFinal = qry + qryField + qryValues

            print( "query = {}".format( qryFinal) )
            return self.db.commitQuery( qryFinal )
        except :
            print( "except = {}".format( qryFinal ) )

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
    def scrape(self, url, isShowContent = None, isUpdated = None ):
        return
    def save(self):
        return
    def openDB(self , dbInfo ):
        self.db = dbConMysql( dbInfo )

# Test for isExist
if False :
    db = crawler_engine_db(True, testdbconfig, 1)
    if True :
        cnt = db.isExistData( "www.joins.com" , None, None  )
        print( cnt )
        cnt = db.isExistData(None, "2018.01.01", None)
        print(cnt)
    if False :
        print("----")
        #def writeData(self,  Url, KeyWord, DataDate, Title, Author, TextData ):
        db.writeData( "www.joins.com" , True,  "가족|바보|간헐천", "2018.01.01" , "Title" , "안혜리", "그렇습니까? 그렇습니다요. 왜요. 어쩔까요" )
        db.writeData("www.joins.com", True, "가족|바보|간헐천", "2018.01.01", "Title", "안혜리", "그렇습니까? 그렇습니다요. 왜요. 어쩔까요")
        db.writeData("www.joins.com", True, "가족|바보|간헐천", "2018.01.01", "Title", "안혜리", "그렇습니까? 그렇습니다요. 왜요. 어쩔까요")
    print( "[MSG][Load Crawler Base Component]" )





