
# https://stackoverflow.com/questions/20638006/convert-list-of-dictionaries-to-a-pandas-dataframe

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

import datetime
import pandas as pd

if False :
    config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
                 'raise_on_warnings': True}
    db = dbConMysql(config_db)
    db2 = dbConMysql(config_db)
    db3 = dbConMysql(config_db)

    ret = db.selectQueryWithRet("select * from tBibleBook")
    data  = ret['data']


path_chrome_driver_win   = "\\..\\Common\\lib\\chromedriver.exe"
path_chrome_driver_win_abs = "D:/workspace/PyCharm/PyTorch/couragesuper-ds/Common/Crawler/lib/chromedriver.exe"

url = "https://www.youtube.com/playlist?list=PLax91QpCgwn0bUCwbPwQ894HO3AsPym1r"



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
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1920x1080')
        webDrv = webdriver.Chrome(path_chrome_driver , chrome_options=options)

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

#1.WebDrv
webDrv = InitWebDriver( False, False )

print(webDrv)

#2.OpenWebPage
OpenWebPage( webDrv , url , False )

#3.리스트의 x_path
#x_path_list =
#nodes = webDrv.find_elements_by_xpath(x_path)

x_path_list = "//*[@id=\"contents\"]"
selector = "#video-title"
x_path_list_item = "//*[@id=\"video-title\"]"


def doScrollDown(wd , whileSeconds):
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=whileSeconds)
    while True:
        #wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        wd.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
        time.sleep(1)
        if datetime.datetime.now() > end:
            break

if False :
    node_list_roots = webDrv.find_elements("xpath", x_path_list )

    for node in node_list_roots :
        try :
            nodes = node.find_elements("tag", "ytd-playlist-video-renderer")
            print(nodes )
        except Exception as e:
            print(e)

doScrollDown( webDrv , 10)

nodes = webDrv.find_elements("xpath" , x_path_list_item)
print( nodes )

listSurmon = []

for elem in nodes :
    #print( elem.text )
    #print( elem.tag_name )
    #print( elem.get_attribute("href"))
    sermon_dict = {
        "title" : elem.text ,
        "link" : elem.get_attribute("href")
    }
    listSurmon.append( sermon_dict )

print( listSurmon )

df = pd.DataFrame( listSurmon )
print( df )
df.to_excel( "hsnewact_praise.xlsx" )




exit(0)


