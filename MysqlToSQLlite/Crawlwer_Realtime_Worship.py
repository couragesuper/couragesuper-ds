
import sys
import time
import os
sys.path.append("../Common")
from Mysql.libmysql import dbConMysql

from time import sleep
from selenium import webdriver


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

listContent =[{"url":"http://www.shinechurch.or.kr/%EC%83%A4%EC%9D%B8-%EC%BB%A8%ED%85%90%EC%B8%A0/%EC%83%A4%EC%9D%B8%ED%86%A1" , "type":"videopager" }, # shine talk
              {"url":"http://www.shinechurch.or.kr/%ec%83%a4%ec%9d%b8-%ec%bb%a8%ed%85%90%ec%b8%a0/%ec%83%a4%ec%9d%b8%eb%89%b4%ec%8a%a4", "type":"videopager" }, # shine news
               {"url":"http://www.shinechurch.or.kr/%ec%83%a4%ec%9d%b8-%ec%bb%a8%ed%85%90%ec%b8%a0/%ec%98%88%ec%88%98%eb%8b%a4tv", "type":"youtube" }] # yesuda

url = "https://www.youtube.com/channel/UC4YCuEErpMBa6H1Wn50YcEg"

OpenWebPage(wd, url, False)

elems = wd.find_elements_by_class_name( "yt-img-shadow" )
for elem in elems :
    href = elem.get_attribute("src")
    if( "i.ytimg.com" in str(href) ) : print(href)


