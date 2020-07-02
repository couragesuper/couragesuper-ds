import sys
import time
import os
sys.path.append("../Common/Crawler")
sys.path.append("../Common/Util")
sys.path.append("../Common")
from Mysql.libmysql import dbConMysql


from mod_crawler_base import craw_base
from time import sleep
from selenium import webdriver
import json
import re


path_chrome_driver_win   = "\\..\\Common\\lib\\chromedriver.exe"
path_chrome_driver_win_abs = "D:/workspace/PyCharm/PyTorch/couragesuper-ds/Common/Crawler/lib/chromedriver.exe"

# crawler common api
#   initalize the web driver

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

url = "http://www.ucc.or.kr/bbs/board.php?bo_table=board_19"

wd = InitWebDriver( False, False )
OpenWebPage( wd , url , False )

# 버튼은 다음과 같이 찾는 것이 용이
# 1.get pages
# 2.loop pages
# 3.loop page
# 4.crawling page

#1
css_name = "pg_end"
elem = wd.find_element_by_class_name(css_name)
print(elem.text)
elem.click()

css_name = "pg_current"
elem = wd.find_element_by_class_name(css_name)
print(elem.text)

maxpage = int(elem.text)
listLink = []
tarpage = maxpage



config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
             'raise_on_warnings': True}
db = dbConMysql(config_db)

listSermon = []

for page in range( 1, tarpage + 1 ) :
    page_url = "http://www.ucc.or.kr/bbs/board.php?bo_table=board_19&page={}".format(page)
    OpenWebPage( wd, page_url, False )
    sleep(0.5)
    # test to obtain url of sermon from lists
    if( False ) :
        listElem = wd.find_elements_by_class_name('ngeb')
        for i, elem in enumerate ( listElem ) :
            url = elem.find_element_by_tag_name('a').get_attribute('href')
            listLink.append( url )
        for url in listLink:
            OpenWebPage( wd , url , False)
            iframes = wd.find_elements_by_tag_name("iframe")
            for elem_iframe in iframes :
                print( elem_iframe.get_attribute("src") )
    else :
        listElem = wd.find_elements_by_class_name('rt_area')
        for i, elem in enumerate ( listElem ) :
            try :
                title_elem = elem.find_element_by_class_name( 'ngeb' )
                #print( title_elem.text )
                #print( title_elem.find_element_by_tag_name('a').get_attribute('href') )
                cnt_elem = elem.find_element_by_class_name('cnt')
                strCnt = str( cnt_elem.text )
                tokstrCnt =  strCnt.split("\n")
                if( len( tokstrCnt ) == 2 ):
                    dictSermon = {"title": title_elem.text, "url": title_elem.find_element_by_tag_name('a').get_attribute('href'), "content": tokstrCnt[0], "date": tokstrCnt[1]}
                else :
                    dictSermon = {"title": title_elem.text,"url": title_elem.find_element_by_tag_name('a').get_attribute('href'),"content": "", "date": tokstrCnt[0]}
                listSermon.append( dictSermon )
            except:
                print("error in page:{},elem:{}".format(page,i))



file = open( "output.bin" , "w")
with file :
    json_data = json.dumps( listSermon )
    file.write( json_data )


exit(0)

listSermon_rev = listSermon.reverse()
for i, elem in enumerate(listSermon_rev):
    url = elem["url"]
    OpenWebPage(wd, url, False)
    iframes = wd.find_elements_by_tag_name("iframe")
    for elem_iframe in iframes:
        print(elem_iframe.get_attribute("src"))
        listSermon[i]["youtube"] = elem_iframe.get_attribute("src")
    query = "INSERT INTO tUccSermon( sDate ,url ,title ,biblecontent ,youtubeURL ,content ,succeed) VALUES ( \"{}\" ,\"{}\"  ,\"{}\"  ,\"{}\"  ,\"{}\"  ,\"{}\" ,1 )".format(
        listSermon[i]['date'], listSermon[i]['url'], listSermon[i]['title'], listSermon[i]['content'], listSermon[i]['youtube'], listSermon[i]['content'])
    db.commitQuery(query)
    sleep(0.3)

print(listSermon)
#for elem in listSermon :



