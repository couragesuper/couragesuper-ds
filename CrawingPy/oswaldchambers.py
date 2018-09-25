from selenium import webdriver
import time
from time import sleep

def InitWebDriver(isHidden):
    path_chrome_driver = "D:\\Workspace\\temp\\DataScience-GitData\\DataScience-master\\chromedriver"
    if isHidden:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920x1080')
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        webDrv = webdriver.Chrome(path_chrome_driver, chrome_options=options)
    else:
        webDrv = webdriver.Chrome(path_chrome_driver)
    return webDrv

def OpenWebPage(webDrv, URL, delay):
    webDrv.get(URL)
    webDrv.implicitly_wait(delay)

wd = InitWebDriver( False )



with open( "oswald_chamber_myutmost.txt", "w+" , encoding="utf-8") as f :
    for mon in range(1, 13):
        for day in range(1, 32):
            try :
                szUrl = "https://utmost.org/2004/%02d/%02d?calendar-redirect=true&amp;post-type=post" % (mon, day)
                szContent = ""
                OpenWebPage(wd, szUrl, 1)
                szContent += str(mon)
                szContent += "\t"
                szContent += str(day)
                szContent += "\t"

                elem = wd.find_element_by_class_name("entry-title")
                szContent += elem.text
                szContent += "\t"

                elem = wd.find_element_by_class_name("entry-meta")
                szContent += elem.text
                szContent += "\t"

                elem = wd.find_element_by_class_name("post-content")
                szContent += elem.text
                szContent += "\n\n"
                print(szContent)
                f.write( szContent )
                sleep(1)
            except :
                print("{}:{} except".format(mon,day))
                sleep(1)




