from selenium import webdriver
import time
from time import sleep
from bs4 import BeautifulSoup


import pandas as pd
import matplotlib.pyplot as plt

import folium
import json
import warnings
warnings.simplefilter(action='ignore' ,  category=FutureWarning)

#references : http://selenium-python.readthedocs.io/
path_chrome_driver = "D:\\Workspace\\temp\\DataScience-GitData\\DataScience-master\\chromedriver"

#for resource
import platform
from matplotlib import font_manager,rc
def checkFontResource()  :
    path = "c:\\Windows\\Fonts\\malgun.ttf"

    if platform.system() == "Darwin" :
        rc('font', family='AppleGothic')
    elif platform.system() == "Windows" :
        font_name = font_manager.FontProperties(fname=path).get_name()
        rc('font', family = font_name)
    else :
        print("unknown system... sorry~~~~")
    plt.rcParams['axes.unicode_minus'] = False

def crawling_sendkey( driver, by , name, sendvalue ) :
    if( by.lower() == "name ") : elem = driver.find_element_by_name(name)
    elif (by.lower() == "xpath"): elem = driver.find_element_by_xpath(name)
    else : return False
    elem.clear()
    elem.send_keys(sendvalue)
    sleep(0.1)
    return True;

def crawling_select_getlist( driver, xpath ) :
    list = driver.find_element_by_xpath(xpath).find_elements_by_tag_name("option")
    value = [option.text for option in list]
    value = value[1:]  # 전체 제거?
    sleep(0.5)  # this makes correct result
    return value

def crawling_table_getlist_tag_xpath(driver, xpath, tag , isElemList ):
    list_webelem = driver.find_element_by_xpath(xpath).find_elements_by_tag_name(tag)
    if isElemList == True : return list_webelem
    else:  return [ {"text":elem.text, "href":elem.get_attribute("href"), "elem":elem , "src":elem.get_attribute("src")} for elem in list_webelem ]

def crawling_select_Item( driver, xpath , selectId , order ) :
    list = driver.find_element_by_xpath(xpath).find_elements_by_tag_name("option")
    value = [option.text for option in list]
    value = value[1:]  # 전체 제거
    element = driver.find_element_by_id( selectId )
    element.send_keys(value[order])
    sleep(0.5)  # this makes correct result

def crawling_click( driver , xpath  ) :
    driver.find_element_by_xpath(xpath).click()
    sleep(0.5)

def InitWebDriver( WebDriverPath) :
    webDriver = webdriver.Chrome(WebDriverPath)
    return webDriver

def OpenWebPage( webDrv, URL , delay ) :
    webDrv.get(URL)
    webDrv.implicitly_wait(delay)

def Main() :
    global path_chrome_driver
    checkFontResource()
    webDrv = InitWebDriver( path_chrome_driver )

    # page loop
    for i in range(1,250) :
        #자동으로 이전에 open한 페이지는 사라지네
        OpenWebPage( webDrv, "https://comic.naver.com/webtoon/detail.nhn?titleId=679519&no=%d" % i , 1 )

        webDrv.switch_to_frame("commentIframe")

        #best comment
        listBestCmts = webDrv.find_elements_by_class_name("u_cbox_comment_box")  # box의 레벨이 이 레벨이 맞음.
        if False:
            xpath_best_comment  = "//*[@id=\"cbox_module\"]/div/div[4]/div[1]/div/ul/li[1]/a/span[2]"
            xpath_whole_comment = "//*[@id=\"cbox_module\"]/div/div[4]/div[1]/div/ul/li[2]/a/span[2]"
            crawling_click( webDrv, xpath_best_comment )

        listClasses   = ['u_cbox_nick' ,'u_cbox_id' ,'u_cbox_contents' ,'u_cbox_date' ,'u_cbox_cnt_recomm' ,'u_cbox_cnt_unrecomm']
        print("iterative the boxs")
        for comment in listBestCmts :
            szCmtFormat = "%d\t" % i
            for iClass in listClasses:
                elem = comment.find_element_by_class_name( iClass )
                szCmtFormat += "{}{}".format( elem.text ,"\t" )
            print(szCmtFormat)
        sleep(1)

        #common comment

        #change the chapter
        xpath_whole_comment = "//*[@id=\"cbox_module\"]/div/div[4]/div[1]/div/ul/li[2]/a/span[2]"
        crawling_click(webDrv, xpath_whole_comment)

        cnt_comment_class = 'u_cbox_count'

        # 순회하는 것이 좀 힘드네 ㅠㅠ
        # 댓글은 15개씩 표시됨.
        # best 댓글과 얻어내는 방법은 똑같지만. Page이동이 어려움 ㅠㅠ
        # 일단은 베댓이나 모으자.
        cntComment = int(webDrv.find_element_by_class_name(cnt_comment_class).text.replace(",", ""))
        cntPage = int(cntComment / 150)
        xpath_next = "//*[@id=\"cbox_module\"]/div/div[6]/div/a[10]"
        for loop in range(0, cntPage ) :
            eleNext = webDrv.find_element_by_xpath(xpath_next)
            eleNext.click()
            sleep(1)

Main()
