import platform
import sys
import time
import os
sys.path.append("../Common")
from Mysql.libmysql import dbConMysql

from time import sleep
from selenium import webdriver

import urllib3

config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'mthx_app', 'raise_on_warnings': True}
db = dbConMysql(config_db)
db2 = dbConMysql(config_db)

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

listContent =[{"url":"http://www.shinechurch.or.kr/%EC%83%A4%EC%9D%B8-%EC%BB%A8%ED%85%90%EC%B8%A0/%EC%83%A4%EC%9D%B8%ED%86%A1" , "type":"videopager" }, # shine talk
              {"url":"http://www.shinechurch.or.kr/%ec%83%a4%ec%9d%b8-%ec%bb%a8%ed%85%90%ec%b8%a0/%ec%83%a4%ec%9d%b8%eb%89%b4%ec%8a%a4", "type":"videopager" }, # shine news
               {"url":"http://www.shinechurch.or.kr/%ec%83%a4%ec%9d%b8-%ec%bb%a8%ed%85%90%ec%b8%a0/%ec%98%88%ec%88%98%eb%8b%a4tv", "type":"youtube" },
              {"url":"http://www.shinechurch.or.kr/%EC%9E%90%EB%85%80%EB%93%A4-%EC%86%8C%EC%8B%9D/%EC%8B%A0%EC%95%99%EA%B0%84%EC%A6%9D","type":"youtube"},
              {"url":"http://www.shinechurch.or.kr/%ec%9e%90%eb%85%80%eb%93%a4-%ec%86%8c%ec%8b%9d/%ec%98%81%ec%83%81/","type":"youtube"}
              ] # yesuda


url_template = "{url}/?pageid=1&mod=list"
url_for_page_template = "{url}/?pageid={page}&mod=list"

# all contents
for i in range(0,len(listContent)) :
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
                listShineContent.append({"sDate": sdate, "url": url, "title": title, "type": content_idx, "youtubeURL": src, "succeed": 1 })

                #listShineContent.append( {"sDate": sDate, "url": contenturl, "title": title, "type": "2" , "youtubeURL": src, "succeed": "OK"})

    if src_type =="youtube":
        for contenturl in yesdatv_url:
            OpenWebPage(wd, contenturl , False)
            title = wd.find_elements_by_class_name("kboard-title")[0].text
            sDate = wd.find_elements_by_class_name("detail-value")[1].text
            video_elem = wd.find_elements_by_class_name("fluid-width-video-wrapper")[0]
            src = video_elem.find_elements_by_tag_name("iframe")[0].get_attribute( "src" )
            listShineContent.append({ "sDate":sDate.split(" ")[0].replace("-",""), "url": contenturl, "title": title , "type" : content_idx , "youtubeURL": src , "succeed": 1 } )

    revlistShineContent = list(reversed(listShineContent))

    for elem  in revlistShineContent :
        query = "INSERT INTO tUccShineContent( sDate , url , title, type , youtubeURL, succeed ) VALUES ( '{sDate}' , '{url}' , '{title}', {type} , '{youtubeURL}' , '{succeed}' )"
        realQuery = query.format(**elem)
        print( realQuery )
        db2.commitQuery( realQuery )
