
import sys
import time
import os
sys.path.append("../Common")
from Mysql.libmysql import dbConMysql

from time import sleep
from selenium import webdriver
import json
import re

from time import sleep
import json

config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
             'raise_on_warnings': True}
db = dbConMysql(config_db)
db2 = dbConMysql(config_db)
db3 = dbConMysql(config_db)

path_chrome_driver_win   = "\\..\\Common\\lib\\chromedriver.exe"
path_chrome_driver_win_abs = "D:/workspace/PyCharm/PyTorch/couragesuper-ds/Common/Crawler/lib/chromedriver.exe"

url_biblebook = [ 'Gen', 'Exo','Lev','num','deu','jos','jdg','rth','1sa','2sa','1ki','2ki','1ch','2ch','ezr','neh','est','job','psa','pro','ecc','son','isa','jer','lam',
'eze','dan','hos','joe','amo','oba','jon','mic','nah','hab','zep','hag','zec','mal','mat','mar','luk','joh','act','rom','1co','2co','gal','eph','phi','col',
'1th','2th','1ti','2ti','tit','phm','heb','jam','1pe','2pe','1jo','2jo','3jo','jud','rev' ]

url_prefix = "http://kcm.co.kr/bible/kor/"
url_postfix = ".html"
max_bible = 66

ret = db.selectQueryWithRet("select * from tBibleBook")
data  = ret['data']

# loop per chapter
def InitWebDriver(isLinux=False, isHidden=False):
    if( False ) :
        curPath = os.path.dirname(os.path.abspath(__file__))
        print( "InitWebDriver:curPath{}".format(curPath) )
        if (isLinux):
            path_chrome_driver = curPath + path_chrome_driver_linux
        else:
            path_chrome_driver = curPath + path_chrome_driver_win
        print("InitWebDriver:curPath:{} , chrome_driver:{}".format(curPath, path_chrome_driver))
    else :
        path_chrome_driver = path_chrome_driver_win_abs
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

wd = InitWebDriver( False, False )

for iBook in range( 1 , len(data) + 1 ):
    bibleseq = 3
    if( iBook > 39 ) : bibleseq = 4
    ret2 = db2.selectQueryWithRet("select max(book_chap) as cntChap from (Select book_chap from tBibleCont where book_seq = {} and bible_seq= {} group by book_chap) as a ".format(iBook, bibleseq))
    cntChap = ret2['data'][0]['cntChap']
    #print( "{} : cnt-{}".format( iBook, cntChap ) )
    for iChap in range( 1, cntChap + 1) :
        url = ( url_prefix + str(url_biblebook[iBook-1]) +  str(iChap) + url_postfix )
        OpenWebPage( wd , url , False )
        nodes = wd.find_elements_by_xpath("//p | //td")
        isTitle = False
        for node in nodes :
            #print( "node.tag {} , node.text {}".format( node.tag_name,  node.text ) )
            if isTitle :
                hypers = node.find_elements_by_tag_name("a")
                if( len( hypers ) != 0 )  :
                    for hyper in hypers :
                        print( "Title {} , Word:{} ".format( Title,  hyper.get_attribute("name") ) )
                isTitle = False
                Title = ""
            if ( node.tag_name == "p" ) :
                isTitle = True
                Title = node.text

exit(0)

for i, elem in enumerate(listSermon):
    try :
        url = elem["url"]
        OpenWebPage(wd, url, False)
        # get youtube
        iframes = wd.find_elements_by_tag_name("iframe")
        for elem_iframe in iframes:
            #print(elem_iframe.get_attribute("src"))
            listSermon[i]["youtube"] = elem_iframe.get_attribute("src")

        if( "김형민 목사" in listSermon[i]['content']) :
            elem_sides = wd.find_elements_by_class_name("side")
            if False :
                for elem_side in elem_sides:
                    print( "side :id:{}:text{}".format( i, elem_side.text ) )
            else :
                listSermon[i]['content'] = elem_sides[0].text
                listSermon[i]['biblecontent'] = elem_sides[0].text

        if( 'youtube' in listSermon[i].keys() ) :
            query = "INSERT INTO tUccSermon( sDate ,url ,title ,biblecontent ,youtubeURL ,content ,succeed) VALUES ( \"{}\" ,\"{}\"  ,\"{}\"  ,\"{}\"  ,\"{}\"  ,\"{}\" ,1 )".format(
                listSermon[i]['date'], listSermon[i]['url'], listSermon[i]['title'], listSermon[i]['content'], listSermon[i]['youtube'], listSermon[i]['content'])
        else :
            query = "INSERT INTO tUccSermon( sDate ,url ,title ,biblecontent ,content ,succeed) VALUES ( \"{}\" ,\"{}\"  ,\"{}\"  ,\"{}\" ,\"{}\" ,1 )".format(
                listSermon[i]['date'], listSermon[i]['url'], listSermon[i]['title'], listSermon[i]['content'], listSermon[i]['content'])
        db.commitQuery(query)
        sleep(0.3)
        #print("[OK]idx:{} {} is ok ".format(i , listSermon[i] ))
    except Exception as e:
        print("[FAIL]idx:{} {} with Exception {} ".format(i , listSermon[i] , e ))



