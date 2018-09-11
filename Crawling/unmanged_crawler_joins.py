import sys
import time
sys.path.append("C:/Users/couragesuper/PycharmProjects/SampleProject/venv/Common")

from Crawler import mod_craw as craw
from Crawler.mod_craw_logger import Crawler_Logger as logger
from time import sleep

# 이 샘플은 Joins_Keyword에서 좀 더 일반화 되었음.
# 관리하지 않습니다.

class craw_joins_keyword :
    def __init__( self, keyword, filename, logger_name, maxpage = 0):
        self.keyword  = keyword
        self.filename = filename
        self.logger_name = logger_name
        self.webdriver = craw.InitWebDriver(False, False)
        self.isShowContent = True
        self.maxpage = maxpage
        self.delay_between_page = 1

    def get_maxpage( self ):
        baseUrl = "https://news.joins.com/find/list?page=1&Keyword=%s&SourceGroupType=Joongang" % ( self.keyword )
        css_name = "btn_next"
        craw.OpenWebPage(self.webdriver, baseUrl, 1)
        self.max_page = 0
        while (True):
            elem = self.webdriver.find_element_by_class_name(css_name)
            pos = elem.text.find("없음")
            if (pos == -1):
                print("다음페이지 있음")
                elem.click()
            else:
                print("다음페이지 없음")
                elems = self.webdriver.find_elements_by_class_name('link_page')
                listPages = []
                for eobj in elems:
                    listPages.append(int(eobj.text))
                listPages = sorted(listPages, reverse=True)
                self.max_page = listPages[0]
                break
            sleep( self.delay_between_page )
    def crawling( self):
        self.get_maxpage()
        print( "keyword = {} , maxpage = {}".format(self.keyword, self.max_page) )
        if( self.max_page > 0 ) :
            for i in range(1,self.max_page + 1) :
                self.craw_page( i )
    def craw_page( self, page ):
        logger_craw = logger( self.logger_name , False)
        with open( self.filename , "a+", encoding='utf-8') as f:
            listLink = []
            baseUrl = "https://news.joins.com/find/list?page=%d&IsDuplicate=True&key=EditorialColumn&Keyword=%s&SourceGroupType=Joongang" % (page, self.keyword)
            craw.OpenWebPage(self.webdriver, baseUrl, 1)
            listElem = self.webdriver.find_elements_by_class_name('headline')
            for i, elem in enumerate(listElem):
                listLink.append(elem.find_element_by_tag_name('a').get_attribute('href'))
            for i, elem in enumerate(listLink):
                url = listLink[i]
                dicRet = logger_craw.getHistory(url)
                if ((dicRet['check'] == 'fail') or ((dicRet['check'] == 'ok') and (dicRet['ret'] == 'fail'))):
                    try:
                        start_time = time.time()
                        craw.OpenWebPage(self.webdriver, listLink[i], 1)
                        # Title
                        elem = self.webdriver.find_element_by_id('article_title')
                        txt_head = elem.text
                        f.write(txt_head)
                        f.write("\t")
                        # Date
                        elem = self.webdriver.find_element_by_class_name('byline')
                        txt_date_input = elem.text.split()[2]
                        f.write(txt_date_input)
                        f.write("\t")
                        # Writer
                        elem = self.webdriver.find_element_by_class_name('profile')
                        txt_profile = elem.text
                        f.write(txt_profile)
                        f.write("\t")
                        # Tag
                        elem = self.webdriver.find_elements_by_class_name('tag_list')
                        listKeyword = elem[0].text.split("\n#")
                        txt_Keyword = ""
                        for i in range(1,len(listKeyword)) :
                            txt_Keyword += listKeyword[i]
                            txt_Keyword += ","
                        f.write(txt_proc)
                        f.write("\n")
                        # Content
                        elem = self.webdriver.find_element_by_class_name('article_body')
                        txt_org = elem.text
                        txt_proc = txt_org.replace("\n", "  ")
                        if (isShowContent): print(txt_proc)
                        f.write(txt_proc)
                        f.write("\n")
                        print("Title:%s Writer:%s interval:%d" % (txt_head, txt_profile, (time.time() - start_time)))
                        logger_craw.updateHistory(url, "ok")
                    except:
                        logger_craw.updateHistory(url, "fail")
                sleep(1)
        logger_craw.updateXML()

def Main() :
    craw_joins_bunsudae = craw_joins_keyword("분수대", "bunsudae.txt", "bunsudae_history.xml")
    craw_joins_bunsudae.crawling()

Main()