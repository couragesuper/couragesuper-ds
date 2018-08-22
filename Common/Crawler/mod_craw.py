from selenium import webdriver
import time
from time import sleep

path_chrome_driver_linux = "/root/chromedriver/chromedriver"
path_chrome_driver_win = "D:\\Workspace\\temp\\DataScience-GitData\\DataScience-master\\chromedriver"

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
    value = value[1:]  # 전체 제거?
    element = driver.find_element_by_id( selectId )
    element.send_keys(value[order])
    sleep(0.5)  # this makes correct result
    
def InitWebDriver( isLinux = False, isHidden = False  ) :
    if( isLinux ) : path_chrome_driver = path_chrome_driver_linux       
    else : path_chrome_driver = path_chrome_driver_win               
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
    
print( "[Load] module for crawler" )