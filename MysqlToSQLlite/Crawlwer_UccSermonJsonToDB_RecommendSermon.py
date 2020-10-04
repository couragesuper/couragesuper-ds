
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

if False :

    file = open("..\CrawingPy\output.bin" , "r")
    with file:
        data = file.read()
        listSermon = json.loads(data)
        print( listSermon )
        print( len( listSermon) )

    listSermon.reverse()
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
else :
    url = "http://www.shinechurch.or.kr/%ec%98%88%eb%b0%b0%ec%99%80-%eb%a7%90%ec%94%80/%ec%b6%94%ec%b2%9c%ec%84%a4%ea%b5%90/"

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

    maxpage = 1

    url_for_page = "http://www.shinechurch.or.kr/%EC%98%88%EB%B0%B0%EC%99%80-%EB%A7%90%EC%94%80/%EC%B6%94%EC%B2%9C%EC%84%A4%EA%B5%90/?pageid={page}&mod=list"
    for nPage in range(1, maxpage + 1) :
        url_target = url_for_page.format(page=nPage)
        OpenWebPage(wd, url_target, False)

        class_namn="video_list_item_wrapper"
        elems = wd.find_elements_by_class_name( class_namn )
        for elem in elems :
            listSermon.append( elem.find_elements_by_tag_name("a")[0].get_attribute("href") )

    print( listSermon )

    # iterate sermon
    listMissedSermon = []

    for sermon in listSermon :
        OpenWebPage(wd, sermon, False)
        title = wd.find_elements_by_class_name("kboard-title")[0].text

        content = wd.find_elements_by_class_name("content-view")[0].text

        arr_content = content.split("\n")
        #print( arr_content )
        #print(content)

        biblecontent = ""

        for elem in arr_content :
            for biblename in listBibleName :
                if( biblename in elem ) :
                    if( biblecontent != "" ) : biblecontent += " / "
                    biblecontent += elem

        url = wd.find_elements_by_class_name("fluid-width-video-wrapper")[0].find_elements_by_tag_name("iframe")[0].get_attribute("src")
        print( title , url )
        query = "select * from tUccSermon where youtubeURL='{url}'".format( url = url )
        ret = db2.selectQueryWithRet( query )
        print( len( ret['data'] ) )

        if( len(ret['data']) == 0 ) :
            listMissedSermon.append( {"title": title , "youtubeURL" : url , "url" : sermon , "content" : biblecontent } )
        else :
            break;
        sleep(0.5)


    print( listMissedSermon )

    revlistMissedSermon = list(reversed(listMissedSermon))

    for i in range(0,len(revlistMissedSermon)) :
        query = "INSERT INTO tUccSermonRecommend( sDate ,url ,title ,biblecontent  ,youtubeURL ,content ,succeed ) VALUES ('{sDate}' ,'{url}' ,'{title}' ,'{biblecontent}'  ,'{youtubeURL}' ,'{content}' ,{succeed})"
        dicData = {}
        dicData["title"] = revlistMissedSermon[i]["title"]
        dicData["youtubeURL"] = revlistMissedSermon[i]["youtubeURL"]
        dicData["url"] = revlistMissedSermon[i]["url"]
        listToken = dicData["title"].split("(")
        #dicData["sDate"] = listToken[ len(listToken) - 1 ].replace(")","")
        dicData["sDate"] = "20200616"
        dicData["succeed"] = 1
        dicData["biblecontent"] = revlistMissedSermon[i]["content"]
        dicData["content"] = revlistMissedSermon[i]["content"]
        realQuery = query.format(**dicData)
        db2.commitQuery( realQuery )
        print(dicData)



