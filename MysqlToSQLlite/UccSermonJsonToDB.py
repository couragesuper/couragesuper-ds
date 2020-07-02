
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



#print(listSermon)
#for elem in listSermon :
