from selenium import webdriver
import time
from time import sleep
from bs4 import BeautifulSoup

import warnings
warnings.simplefilter(action='ignore' ,  category=FutureWarning)

path_chrome_driver = "D:\\Workspace\\temp\\DataScience-GitData\\DataScience-master\\chromedriver"

def InitWebDriver( isLinux = False, isHidden = False ) :
    if False :
        path_chrome_driver = "/root/chromedriver/chromedriver"
    else :
        path_chrome_driver = "D:\\Workspace\\temp\\DataScience-GitData\\DataScience-master\\chromedriver"
    if( isHidden ) :
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920x1080')
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        webDrv = webdriver.Chrome(path_chrome_driver, chrome_options=options)
    else :
        webDrv  = webdriver.Chrome(path_chrome_driver)
    return webDrv

def OpenWebPage( webDrv, URL , delay ) :
    webDrv.get(URL)
    webDrv.implicitly_wait(delay)

def Main() :
    wd = InitWebDriver( False, False )
    now = time.localtime()

    #szBaseUrl_Sasul ="http://news.joins.com/find/list?page=1&IsDuplicate=True&key=EditorialColumn&Keyword=사설&SourceGroupType=Joongang&ServiceCode=20" % (1)
    time_str = "%d_%d_%d_%d_%d_%d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

    #중앙일보는 다음과 같이 Page 분류 기능이 만들어져 있기 때문에, Crawling이 매우 용이하다.

    with open("joongang_series_saul_" + time_str + ".txt", "w+", encoding='utf-8') as f:
        #for i in range(1, 228):701
        for i in range(1, 100):
            szBaseUrl_Sasul = "http://news.joins.com/find/list?page=%d&IsDuplicate=True&key=EditorialColumn&Keyword=사설&SourceGroupType=Joongang&ServiceCode=20" % (i)
            OpenWebPage(wd, szBaseUrl_Sasul , 1)
            listElem = wd.find_elements_by_class_name('headline')
            listLink = []
            for i, elem in enumerate(listElem):
                listLink.append(elem.find_element_by_tag_name('a').get_attribute('href'))
            for i, elem in enumerate(listLink):
                OpenWebPage(wd, listLink[i], 1)

                elem = wd.find_element_by_id('article_title')
                txt_headline_org = elem.text
                f.write(txt_headline_org)
                f.write("||")

                elem = wd.find_element_by_class_name('article_body')
                txt_org = elem.text
                txt_proc = txt_org.replace("\n", " ")
                print(txt_proc)
                f.write(txt_proc)
                f.write("\n")
                sleep(0.5)

Main()