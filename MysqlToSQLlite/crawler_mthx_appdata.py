import platform
import sys
import time
import os
sys.path.append("../Common")
from Mysql.libmysql import dbConMysql

from time import sleep
from selenium import webdriver

import sqlite3
import urllib3

import time

config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'mthx_app', 'raise_on_warnings': True}
db = dbConMysql(config_db)
db2 = dbConMysql(config_db)
db3 = dbConMysql(config_db)

path_chrome_drvier_linux = "/root/chromedriver/chromedriver"
path_chrome_driver_win   = "\\..\\Common\\lib\\chromedriver.exe"
path_chrome_driver_win_abs = "D:/workspace/PyCharm/PyTorch/couragesuper-ds/Common/Crawler/lib/chromedriver.exe"

# crawler common api
#   initalize the web driver

def InitWebDriver(isLinux=False, isHidden=False):
    print("InitWebDriver {} , {} ".format(isLinux, isHidden))
    if( isLinux ) :
        curPath = os.path.dirname(os.path.abspath(__file__))
        print( "InitWebDriver:curPath{}".format(curPath) )
        if (isLinux):
            path_chrome_driver = curPath + path_chrome_driver_linux
        else:
            path_chrome_driver = curPath + path_chrome_driver_win_abs
        print("InitWebDriver:curPath:{} , chrome_driver:{}".format(curPath, path_chrome_driver))
    else :
        print("-----")
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

def geturl(request_type, url):
    http = urllib3.PoolManager()
    response = http.request(request_type, url)
    if len(response.retries.history):
        return response.retries.history[-1].redirect_location
    else:
        return url

isLinux = False
if( get_platform() == "linux") : isLinux = True
wd = InitWebDriver( isLinux , isLinux )

isUpdateDB = False

def updateSermon() :
    url = "http://www.shinechurch.or.kr/%ec%98%88%eb%b0%b0%ec%99%80-%eb%a7%90%ec%94%80/%eb%8b%b4%ec%9e%84%eb%aa%a9%ec%82%ac-%ec%84%a4%ea%b5%90/?pageid=1&mod=list"
    maxpage = 0

    OpenWebPage(wd, url, False)
    elems = wd.find_elements_by_class_name("last-page")
    print("maxpage:{}".format(len(elems)))

    listSermon = []

    for elem in elems:
        elems_a_tag = elem.find_elements_by_tag_name("a")
        print(len(elems_a_tag))
        for elem_a_tag in elems_a_tag:
            href = elem_a_tag.get_attribute("href")
            if False:
                print(href)
                print(str(href).split("?")[1])
                toks = str(href).split("?")[1]
                print(toks.split("&")[0].split("=")[1])
            maxpage = int(str(href).split("?")[1].split("&")[0].split("=")[1])
            print(maxpage)

    url_for_page = "http://www.shinechurch.or.kr/%ec%98%88%eb%b0%b0%ec%99%80-%eb%a7%90%ec%94%80/%eb%8b%b4%ec%9e%84%eb%aa%a9%ec%82%ac-%ec%84%a4%ea%b5%90/?pageid={page}&mod=list"
    for nPage in range(1, maxpage + 1):
        url_target = url_for_page.format(page=nPage)
        OpenWebPage(wd, url_target, False)

        class_namn = "video_list_item_wrapper"
        elems = wd.find_elements_by_class_name(class_namn)
        for elem in elems:
            listSermon.append(elem.find_elements_by_tag_name("a")[0].get_attribute("href"))

    print(listSermon)

    # iterate sermon
    listMissedSermon = []

    for sermon in listSermon:
        OpenWebPage(wd, sermon, False)
        title = wd.find_elements_by_class_name("kboard-title")[0].text
        content = wd.find_elements_by_class_name("content-view")[0].text
        arr_content = content.split("\n")
        # print( arr_content )
        # print(content)
        biblecontent = ""
        print(arr_content)
        for elem in arr_content:
            for biblename in listBibleName:
                if (biblename in elem):
                    if (biblecontent != ""): biblecontent += " / "
                    biblecontent += elem
                    print("biblename:{}".format(biblename))
        print(biblecontent)
        url = wd.find_elements_by_class_name("fluid-width-video-wrapper")[0].find_elements_by_tag_name("iframe")[
            0].get_attribute("src")
        print(title, url)
        query = "select * from tUccSermon where youtubeURL='{url}'".format(url=url)
        ret = db2.selectQueryWithRet(query)
        print(len(ret['data']))
        if (len(ret['data']) == 0):
            isUpdateDB = True
            listMissedSermon.append({"title": title, "youtubeURL": url, "url": sermon, "content": biblecontent})
        else:
            break;
        sleep(0.5)

    print(listMissedSermon)

    revlistMissedSermon = list(reversed(listMissedSermon))

    for i in range(0, len(revlistMissedSermon)):
        query = "INSERT INTO tUccSermon( sDate ,url ,title ,biblecontent  ,youtubeURL ,content ,succeed ) VALUES ('{sDate}' ,'{url}' ,'{title}' ,'{biblecontent}'  ,'{youtubeURL}' ,'{content}' ,{succeed})"
        dicData = {}
        dicData["title"] = revlistMissedSermon[i]["title"]
        dicData["youtubeURL"] = revlistMissedSermon[i]["youtubeURL"]
        dicData["url"] = revlistMissedSermon[i]["url"]
        listToken = dicData["title"].split("(")
        szDate = listToken[len(listToken) - 1].replace(")", "")
        if ((szDate).isdigit()):
            dicData["sDate"] = szDate
        else:
            dicData["sDate"] = "20200914"
        dicData["succeed"] = 1

        if (len(revlistMissedSermon[i]["content"]) < 100):
            dicData["biblecontent"] = revlistMissedSermon[i]["content"]
            dicData["content"] = revlistMissedSermon[i]["content"]
        else:
            dicData["biblecontent"] = ""
            dicData["content"] = ""
        realQuery = query.format(**dicData)
        print(realQuery)
        #db2.commitQuery(realQuery)
        print(dicData)


def updateShineContent() :
    listContent =[{"url":"http://www.shinechurch.or.kr/%EC%83%A4%EC%9D%B8-%EC%BB%A8%ED%85%90%EC%B8%A0/%EC%83%A4%EC%9D%B8%ED%86%A1" , "type":"videopager" }, # shine talk
                  {"url":"http://www.shinechurch.or.kr/%ec%83%a4%ec%9d%b8-%ec%bb%a8%ed%85%90%ec%b8%a0/%ec%83%a4%ec%9d%b8%eb%89%b4%ec%8a%a4", "type":"videopager" }, # shine news
                   {"url":"http://www.shinechurch.or.kr/%ec%83%a4%ec%9d%b8-%ec%bb%a8%ed%85%90%ec%b8%a0/%ec%98%88%ec%88%98%eb%8b%a4tv", "type":"youtube" }] # yesuda
    url_template = "{url}/?pageid=1&mod=list"
    url_for_page_template = "{url}/?pageid={page}&mod=list"

    # all contents
    for i in range(0,3) :
        maxpage = 0
        content_idx = i

        url_tar = listContent[content_idx]["url"]
        src_type = listContent[content_idx]["type"]

        url = url_template.format( url = url_tar )

        OpenWebPage(wd, url, False)
        elems = wd.find_elements_by_class_name("last-page")
        print( "maxpage:{}".format( len(elems) ) )

        for elem in elems :
            elems_a_tag = elem.find_elements_by_tag_name("a")
            print( len(elems_a_tag) )
            for elem_a_tag in elems_a_tag :
                href = elem_a_tag.get_attribute("href")
                if True :
                    print( "href={}".format(href) )
                    print( str( href ).split("?")[1] )
                    toks = str(href).split("?")[1]
                    print( toks.split("&")[0].split("=")[1])
                maxpage = int( str(href).split("?")[1].split("&")[0].split("=")[1] )
                print(maxpage)

        print("maxpage={}".format(maxpage))

        listShineContent = []
        yesdatv_url = []

        for nPage in range(1, maxpage + 1) :
            url_target = url_for_page_template.format(url = url_tar, page=nPage)
            OpenWebPage(wd, url_target, False)
            print( "type:{}".format( src_type ) )
            if src_type == "youtube" :
                # add only url
                class_name="kboard-list"
                elems = wd.find_elements_by_class_name( class_name )
                print( len(elems ))
                for elem in elems :
                    arr = elem.find_elements_by_tag_name("a")
                    print( "lenarr:{}".format(len(arr)) )
                    for arr_elem in arr :
                        yesdatv_url.append( arr_elem.get_attribute("href") )
            else :
                # image based
                # add full context
                class_name = "gallery-img-wrapper"
                elems = wd.find_elements_by_class_name(class_name)
                for elem in elems :
                    arr = elem.find_elements_by_tag_name("a")
                    url = arr[0].get_attribute("href")
                    print("url={}..1".format(url))
                    url = geturl( "HTTP" , url )
                    print( "url={}..2".format(arr[0].get_attribute("href")) )
                    src = arr[0].find_elements_by_tag_name("img")[0].get_attribute("src")
                    print( "src={}".format(arr[0].find_elements_by_tag_name("img")[0].get_attribute("src")) )
                    txt = elem.text
                    print( "txt={}".format(elem.text) )

                    title = txt.split("\n")[0]
                    sdate = txt.split("\n")[1].split("(")[1].replace(")", "")

                    print( title, sdate )
                    if True :
                        query = "select * from tUccShineContent where youtubeURL='{url}'".format(url=src)
                        ret = db2.selectQueryWithRet(query)
                        print(len(ret['data']))
                        if (len(ret['data']) == 0):
                            isUpdateDB = True
                            #listMissedSermon.append({"title": title, "youtubeURL": url, "url": sermon, "content": biblecontent})
                            listShineContent.append({"sDate": sdate, "url": url, "title": title, "type": content_idx, "youtubeURL": src,"succeed": 1})
                        else:
                            break;

                    #listShineContent.append( {"sDate": sDate, "url": contenturl, "title": title, "type": "2" , "youtubeURL": src, "succeed": "OK"})

        if src_type =="youtube":
            for contenturl in yesdatv_url:
                OpenWebPage(wd, contenturl , False)
                title = wd.find_elements_by_class_name("kboard-title")[0].text
                sDate = wd.find_elements_by_class_name("detail-value")[1].text
                video_elem = wd.find_elements_by_class_name("fluid-width-video-wrapper")[0]
                src = video_elem.find_elements_by_tag_name("iframe")[0].get_attribute( "src" )

                if True:
                    query = "select * from tUccShineContent where youtubeURL='{url}'".format(url=contenturl)
                    ret = db2.selectQueryWithRet(query)
                    print(len(ret['data']))
                    if (len(ret['data']) == 0):
                        isUpdateDB = True
                        # listMissedSermon.append({"title": title, "youtubeURL": url, "url": sermon, "content": biblecontent})
                        listShineContent.append({ "sDate":sDate.split(" ")[0].replace("-",""), "url": contenturl, "title": title , "type" : 2 , "youtubeURL": src , "succeed": 1 } )
                    else:
                        break;

        revlistShineContent = list(reversed(listShineContent))

        for elem  in revlistShineContent :
            query = "INSERT INTO tUccShineContent( sDate , url , title, type , youtubeURL, succeed ) VALUES ( '{sDate}' , '{url}' , '{title}', {type} , '{youtubeURL}' , '{succeed}' )"
            realQuery = query.format(**elem)
            print( realQuery )
            #db2.commitQuery( realQuery )

if isUpdateDB == True :

    now = time.localtime()
    dbRev = "{}{}{}{}".format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour)
    dbName_Content = "shinechurch_" + dbRev + ".db"
    print(dbName_Content)
    con_cont = sqlite3.connect(dbName_Content)

    with con_cont:
        cursor = con_cont.cursor()
        # idx, sdate, url, title, biblecontent, youtubeurl, content, succeed
        dictCreateQueries = {
            "tsermon": {
                "create": "CREATE TABLE tUccSermon ( idx int , sdate text, url text, title text, biblecontent text, youtubeurl text , content text, succeed int )",
                "select": "select * from tUccSermon",
                "insert": 'insert into tUccSermon ( idx , sdate , url, title , biblecontent , youtubeurl , content, succeed ) Values ( {idx} , "{sDate}" , "{url}", "{title}" , "{biblecontent}" , "{youtubeURL}" , "{content}", {succeed} )'
                , "isInsert": True
            },
            "tUccSermonRecommend": {
                "create": "CREATE TABLE tUccSermonRecommend ( idx int , sdate text, url text, title text, biblecontent text, youtubeurl text , content text, succeed int )",
                "select": "select * from tUccSermonRecommend",
                "insert": 'insert into tUccSermonRecommend ( idx , sdate , url, title , biblecontent , youtubeurl , content, succeed ) Values ( {idx} , "{sDate}" , "{url}", "{title}" , "{biblecontent}" , "{youtubeURL}" , "{content}", {succeed} )'
                , "isInsert": True
            },
            "tUccSermonCTS": {
                "create": "CREATE TABLE tUccSermonCTS ( idx int , sdate text, url text, title text, biblecontent text, youtubeurl text , content text, succeed int )",
                "select": "select * from tUccSermonCTS",
                "insert": 'insert into tUccSermonCTS ( idx , sdate , url, title , biblecontent , youtubeurl , content, succeed ) Values ( {idx} , "{sDate}" , "{url}", "{title}" , "{biblecontent}" , "{youtubeURL}" , "{content}", {succeed} )'
                , "isInsert": True
            },
            "tUccSermonCTS2": {
                "create": "CREATE TABLE tUccSermonCTS2 ( idx int , sdate text, url text, title text, biblecontent text, youtubeurl text , content text, succeed int )",
                "select": "select * from tUccSermonCTS2",
                "insert": 'insert into tUccSermonCTS2 ( idx , sdate , url, title , biblecontent , youtubeurl , content, succeed ) Values ( {idx} , "{sDate}" , "{url}", "{title}" , "{biblecontent}" , "{youtubeURL}" , "{content}", {succeed} )'
                , "isInsert": True
            },
            "tUccSermonCTS3": {
                "create": "CREATE TABLE tUccSermonCTS3 ( idx int , sdate text, url text, title text, biblecontent text, youtubeurl text , content text, succeed int )",
                "select": "select * from tUccSermonCTS3",
                "insert": 'insert into tUccSermonCTS3 ( idx , sdate , url, title , biblecontent , youtubeurl , content, succeed ) Values ( {idx} , "{sDate}" , "{url}", "{title}" , "{biblecontent}" , "{youtubeURL}" , "{content}", {succeed} )'
                , "isInsert": True
            },
            "tUccSermon_DawnJeja": {
                "create": "CREATE TABLE tUccSermon_DawnJeja ( idx int , sdate text, url text, title text, biblecontent text, youtubeurl text , content text, succeed int, type text, txt text )",
                "select": "select * from tUccSermon_DawnJeja",
                "insert": 'insert into tUccSermon_DawnJeja ( idx , sdate , url, title , biblecontent , youtubeurl , content, succeed , type , txt ) Values ( {idx} , "{sDate}" , "{url}", "{title}" , "{biblecontent}" , "{youtubeURL}" , "{content}", {succeed}, "{type}" , "txt" )'
                , "isInsert": True
            },
            # INSERT INTO tUccShineContent(sDate, url, title, type, youtubeURL, succeed) VALUES('{sDate}', '{url}', '{title}', {type},'{youtubeURL}', '{succeed}')
            "tUccShineContent": {
                "create": "CREATE TABLE tUccShineContent ( idx int , sDate text , url text , title text , type int , youtubeURL text , succeed int )",
                "select": "select * from tUccShineContent",
                "insert": 'insert into tUccShineContent ( idx , sDate, url, title, type, youtubeURL, succeed ) Values ( {idx} , "{sDate}" , "{url}", "{title}", {type}, "{youtubeURL}", {succeed} )'
                , "isInsert": True
            },

        }
        # loop for query lists
        for query in dictCreateQueries.keys():
            # perform .. create table
            print("query {}={}".format(query, dictCreateQueries[query]['create']))
            cursor.execute(dictCreateQueries[query]['create'])
            if (dictCreateQueries[query]['isInsert'] == True):
                # pull data from mysql server
                ret = db.selectQueryWithRet(dictCreateQueries[query]['select'])
                for elem in ret['data']:
                    for elem_field in elem.keys():
                        # handle tsermon
                        if ((query == "tsermon") and (elem_field == "youtubeURL")):
                            data = elem['youtubeURL']
                            if (data != None):
                                print(data.split("/")[4].split("?")[0])
                                elem[elem_field] = data.split("/")[4].split("?")[0]
                        # handle string field
                        if (type(elem[elem_field]) == str):
                            elem[elem_field] = elem[elem_field].replace('"', '""')

                    if (query == "tWordForPraise"): print(dictCreateQueries[query]['insert'].format(**elem))
                    cursor.execute(dictCreateQueries[query]['insert'].format(**elem))
        con_cont.commit()

