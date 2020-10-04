
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

config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'mthx_app', 'raise_on_warnings': True}
db = dbConMysql(config_db)
db2 = dbConMysql(config_db)

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

#make bible book name
queryBibleBook = "select biblebook_krnm from tBibleBook"
ret = db2.selectQueryWithRet(queryBibleBook)
dataBibleBook = ret['data']
listBibleName = []

for row in dataBibleBook :
    listBibleName.append(row['biblebook_krnm'])
print(listBibleName)

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

url = "http://www.shinechurch.or.kr/%EC%98%88%EB%B0%B0%EC%99%80-%EB%A7%90%EC%94%80/%EC%83%88%EB%B2%BD%EC%A0%9C%EC%9E%90%ED%9B%88%EB%A0%A8/?pageid=1&mod=list"
maxpage = 0

OpenWebPage(wd, url, False)
elems = wd.find_elements_by_class_name("last-page")
print( "maxpage:{}".format( len(elems) ) )



listSermon = []

for elem in elems :
    elems_a_tag = elem.find_elements_by_tag_name("a")
    print( len(elems_a_tag) )
    for elem_a_tag in elems_a_tag :
        href = elem_a_tag.get_attribute("href")
        if False :
            print( href )
            print( str( href ).split("?")[1] )
            toks = str(href).split("?")[1]
            print( toks.split("&")[0].split("=")[1])
        maxpage = int( str(href).split("?")[1].split("&")[0].split("=")[1] )
        print( maxpage )



url_for_page = "http://www.shinechurch.or.kr/%EC%98%88%EB%B0%B0%EC%99%80-%EB%A7%90%EC%94%80/%EC%83%88%EB%B2%BD%EC%A0%9C%EC%9E%90%ED%9B%88%EB%A0%A8/?pageid={page}&mod=list"
for nPage in range(1, maxpage + 1) :
    url_target = url_for_page.format(page=nPage)
    OpenWebPage(wd, url_target, False)
    class_name="kboard-list"
    elems = wd.find_elements_by_class_name( class_name )
    print( len(elems ))
    for elem in elems :
        arr = elem.find_elements_by_tag_name("a")
        print( "lenarr:{}".format(len(arr)) )
        for arr_elem in arr :
            listSermon.append( arr_elem.get_attribute("href") )

listMissedSermon = []

for sermon in listSermon :
    OpenWebPage(wd, sermon, False)
    dicData = {"url":sermon }
    dicData["title"]= wd.find_elements_by_class_name("kboard-title")[0].text
    #dicData["txt"] = wd.find_elements_by_class_name("content-view")[0].text
    #dicData["txt"] = dicData["txt"].replace('"', '""')
    dicData["txt"] = ""
    dicData["sDate"] = wd.find_elements_by_class_name("detail-value")[1].text
    dicData["youtubeURL"] = ""
    dicData["content"] = ""
    listMissedSermon.append( dicData )
    print( dicData)


print( listMissedSermon )

revlistMissedSermon = list(reversed(listMissedSermon))

for i in range(0,len(revlistMissedSermon)) :
    query = "INSERT INTO tUccSermon_DawnJeja( sDate ,url ,title ,biblecontent  ,youtubeURL ,content ,succeed , type, txt ) VALUES ('{sDate}' ,'{url}' ,'{title}' ,'{biblecontent}'  ,'{youtubeURL}' ,'{content}' ,{succeed}, 'text', '{txt}')"
    dicData = {}
    dicData["title"] = revlistMissedSermon[i]["title"]
    dicData["youtubeURL"] = revlistMissedSermon[i]["youtubeURL"]
    dicData["url"] = revlistMissedSermon[i]["url"]

    listToken = dicData["title"].split("(")
    szDate = listToken[len(listToken) - 1].replace(")", "")
    if((szDate ).isdigit() ) :
        dicData["sDate"] = szDate
    else :
        dicData["sDate"] = "20200914"
    dicData["succeed"] = 1
    dicData["txt"] = revlistMissedSermon[i]["txt"]

    if( len( revlistMissedSermon[i]["content"] ) < 100 ) :
        dicData["biblecontent"] = revlistMissedSermon[i]["content"]
        dicData["content"] = revlistMissedSermon[i]["content"]
    else:
        dicData["biblecontent"] = ""
        dicData["content"] = ""
    realQuery = query.format(**dicData)
    print( realQuery )
    db2.commitQuery( realQuery )
    print(dicData)



