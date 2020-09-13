
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

config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'mthx',
             'raise_on_warnings': True}
db = dbConMysql(config_db)

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

wd = InitWebDriver( False, False )

#20200803
url_prefix = 'http://www.shinechurch.or.kr/%ec%98%88%eb%b0%b0%ec%99%80-%eb%a7%90%ec%94%80/%eb%8b%b4%ec%9e%84%eb%aa%a9%ec%82%ac-%ec%84%a4%ea%b5%90'
listSermon = [{"url" :'?uid=1607&mod=document&pageid=1', "sDate": "20200704" , "content" : "출14:19-20,롬5:8" },
              {"url" :'?uid=1616&mod=document&pageid=1' , "sDate": "20200705" , "content" : "마26:30,마27:5"  },
              {"url" :'?uid=1639&mod=document&pageid=1' , "sDate": "20200712" , "content" : "눅9:61-62"},
              {"url" :'?uid=1672&mod=document&pageid=1' , "sDate": "20200719" , "content" : "고후4:7"},
              {"url" :'?uid=1688&mod=document&pageid=1' , "sDate": "20200726", "content" : "창32:1-2,창31:25-26"} ]

    # iterate sermon

for sermon in listSermon :
    OpenWebPage(wd, url_prefix + "/" + sermon['url'], False)

    title = wd.find_elements_by_class_name('content-view')[0].find_elements_by_tag_name('iframe')[0].get_attribute("src")
    print( title )
    sermon['title'] = title
    youtubeURL = wd.find_elements_by_class_name('kboard-title')[0].text
    print( youtubeURL )
    sermon['youtubeURL'] = youtubeURL
    sermon['biblecontent'] = sermon['content']

    sleep(0.5)

query = "INSERT INTO mthx.tUccSermon( sDate ,url ,title ,biblecontent ,youtubeURL ,content ,succeed )  VALUES ('{sDate}' ,'{url}','{title}','{biblecontent}','{youtubeURL}','{content}',0)"

for sermon in listSermon :
    query_tar = query.format( **sermon )
    print( query_tar )
    #db.commitQuery ( query_tar )
