import sys
import time

sys.path.append("../Common/Crawler")
from mod_crawler_base import crawler_base as crawler_main
from time import sleep
from selenium import webdriver

szKeyword    = "키워드로 보는 사설"
szKeyword_En = "Keywordsasul"

#book cosmos용 entity checker이다.
class crawler_joins_kwd (crawler_main):
    def __init__( self , isHidden, outdir, title, keyword ) :
        self.keyword = keyword
        super().__init__(isHidden, outdir, title)
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
                    print("[history]add new page")
                    start_time = time.time()
                    self.openPage(url)
                    self.crawContents(True)
                    self.logger.updateHistory(url, "ok")
                except:
                    print("")
                    self.logger.updateHistory(url, "fail")
            else : print("[history]this page is already added.")
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

isRun = True

if isRun :
    MOD = crawler_joins_kwd( False , "..\/Data/Text/Joins" , "joins_keywordNSasul" , "키워드로 보는 사설" )
    MOD.run()
    MOD.close()




