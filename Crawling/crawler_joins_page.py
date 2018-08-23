import sys
import time
sys.path.append("C:/Users/couragesuper/PycharmProjects/SampleProject/venv/Common")

from Crawler import mod_craw as craw
from Crawler.mod_craw_logger import Crawler_Logger as LOGGER
from Crawler.mod_craw_filewriter import crawler_filewriter as FT
from time import sleep
from selenium import webdriver

path_chrome_driver_linux = "/root/chromedriver/chromedriver"
path_chrome_driver_win   = "C:/Users/couragesuper/PycharmProjects/SampleProject/venv\crawler\lib/chromedriver.exe"

szKeyword    = "키워드로 보는 사설"
szKeyword_En = "Keywordsasul"

class crawler_main :
    def __init__( self , isLinux, isHidden, keyword_en ) :
        self.isLogger = False
        self.isTxt    = False
        self.createLogger(keyword_en , True)
        self.createTxt(keyword_en)
        if (isLinux):
            self.path_chrome_driver = path_chrome_driver_linux
        else:
            self.path_chrome_driver = path_chrome_driver_win
        if (isHidden):
            self.options = webdriver.ChromeOptions()
            self.options.add_argument('--headless')
            self.options.add_argument('--window-size=1920x1080')
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--no-sandbox")
            self.webDrv = webdriver.Chrome(self.path_chrome_driver, chrome_options=self.options)
        else:
            self.webDrv = webdriver.Chrome(self.path_chrome_driver)
        self.delay_dn = 1.5
    def createLogger( self , nameLogger , isDebug):
        self.logger = LOGGER( nameLogger +".xml" , isDebug)
        self.isLogger = True
    def createTxt( self , nameTxt ):
        self.txt = FT( nameTxt + ".txt")
        self.isTxt = True
    def close(self):
        if( self.isLogger ) : self.logger.close()
        if( self.isTxt) : self.txt.close()
    def openPage(self, URL, delay=2.0):
        print( "  openpage = {}".format( URL ) )
        self.webDrv.get(URL)
        self.webDrv.implicitly_wait(delay)
    def run(self , mainUrl ):
        self.openPage(mainUrl)
        self.login()
        self.makeCateLinks()
        self.naviSites()
        return
    def login(self):
        return
    def makeCateLinks(self):
        return
    def naviSites(self):
        return
    def navigate(self,links):
        return

#book cosmos용 entity checker이다.
class crawler_joins_keyword (crawler_main):
    def __init__( self , isLinux, isHidden, keyword_en, keyword ) :
        self.keyword = keyword
        super().__init__(isLinux,isHidden, keyword_en)
    def run(self):
        baseUrl = "https://news.joins.com/find/list?IsDuplicate=True&key=EditorialColumn&Keyword=%s&SourceGroupType=Joongang" % (self.keyword)
        super().run( baseUrl )
    def naviSites(self):
        baseUrl = "https://news.joins.com/find/list?page=%d&IsDuplicate=True&key=EditorialColumn&Keyword=%s&SourceGroupType=Joongang" % (1, self.keyword)
        self.openPage(baseUrl)
        self.navigate(baseUrl)
        sleep(1)
    def getMaxPages(self):
        baseUrl = "https://news.joins.com/find/list?page=1&IsDuplicate=True&key=EditorialColumn&Keyword=%s&SourceGroupType=Joongang" % (self.keyword)
        css_name = "btn_next"
        self.openPage(baseUrl)
        while (True):
            elem = self.webDrv.find_element_by_class_name(css_name)
            pos = elem.text.find("없음")
            if (pos == -1):
                print("다음페이지 있음")
                elem.click()
            else:
                print("다음페이지 없음")
                elems = self.webDrv.find_elements_by_class_name('link_page')
                listPages = []
                for eobj in elems:
                    listPages.append(int(eobj.text))
                listPages = sorted(listPages, reverse=True)
                return listPages[0]
            sleep(0.5)
    def navigate(self , link):
        max_page = self.getMaxPages( )
        for i in range(1, max_page + 1):
            self.navigatePage( i, False )
            sleep(2)
    def navigatePage( self,page, isShowContent ):
        now = time.localtime()
        print(page)
        baseUrl = "https://news.joins.com/find/list?page=%d&IsDuplicate=True&key=EditorialColumn&Keyword=%s&SourceGroupType=Joongang" % (page, self.keyword )
        self.openPage( baseUrl )
        listLink = []
        listElem = self.webDrv.find_elements_by_class_name('headline')
        if (self.isTxt == False ) :
            print("text file isnt configured.")
            return
        for i, elem in enumerate(listElem):
            listLink.append(elem.find_element_by_tag_name('a').get_attribute('href'))
        for i, elem in enumerate(listLink):
            url = listLink[i]
            if( self.logger.getHistory(url) == False ) :
                try:
                    start_time = time.time()
                    self.openPage(url)
                    self.crawContents(True)
                    self.logger.updateHistory(url, "ok")
                except:
                    self.logger.updateHistory(url, "fail")
            sleep(1)
        self.logger.close()
    def crawContents(self,isShowContent):
        #article_title
        elem = self.webDrv.find_element_by_id('article_title')
        txt_head = elem.text
        self.txt.write(txt_head)
        #byline
        elem = self.webDrv.find_element_by_class_name('byline')
        txt_date_input = elem.text.split()[2]
        self.txt.write(txt_date_input)
        #profile
        elem = self.webDrv.find_element_by_class_name('profile')
        txt_profile = elem.text
        self.txt.write(txt_profile)
        # tags , |로 구분
        elem = self.webDrv.find_element_by_class_name('tag_list')
        listTags = elem.text.split("#")[1:]
        szTags = ""
        for tags in listTags:
            szTags += tags.replace("\n", "")
            szTags += "|"
        if (isShowContent): print(szTags)
        self.txt.write(szTags)
        #article_body
        elem = self.webDrv.find_element_by_class_name('article_body')
        txt_org = elem.text
        txt_proc = txt_org.replace("\n", "  ")
        if (isShowContent): print(txt_proc)
        self.txt.writeLast(txt_proc)


if False :
    MOD = crawler_joins_keyword( False, False, "joins_keywordNSasul" , "키워드로 보는 사설" )
else :
    MOD = crawler_joins_keyword(False, False, "Joins_Bunsudae", "분수대")

MOD.run()
MOD.close()




