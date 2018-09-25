import sys
import time
sys.path.append("../Common/Crawler")
sys.path.append("../Common/Util")

from mod_crawler_base import craw_base
from time import sleep
from selenium import webdriver

# bs
from bs4 import BeautifulSoup

szKeyword    = "키워드로 보는 사설"
szKeyword_En = "Keywordsasul"

# joins
    # histroy
    # 20180910 : created
    #   -  use beautiful soup method
    #   -  use link_text method

class crawler_movie_scene (craw_base):
    def __init__( self , isHidden, outdir, title, keyword ) :
        self.keyword = keyword
        super().__init__(isHidden, outdir, title)
    def run(self):
        baseUrl = "https://www.filmmakers.co.kr"
        super().run( baseUrl )
    def naviSites(self):
        baseUrl = "https://www.filmmakers.co.kr"
        self.openPage( baseUrl )
        self.navigate( baseUrl )
        sleep(1)
    def navigate(self, link):
        if True:
            max_page = self.logger.getMaxPagesHistory()
            if (max_page == 0):
                print("[navigate] maxpage is not found")
                max_page = 21 # Hard coding
                self.logger.updatePageHistory(max_page)
            else:
                print("[navigate] maxpage is found = {} ", max_page)
            for i in range(1, max_page + 1):
                self.navigatePage(i, False)
                self.logger.close()
                sleep(2)
    def getMaxPages(self):
        baseUrl = "https://www.filmmakers.co.kr/index.php?mid=koreanScreenplays&page=1"
        self.openPage( baseUrl )
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

    # navigatePage with unit of page
    def navigatePage( self,page, isShowContent ):
        now = time.localtime()
        print(page)
        baseUrl = "https://www.filmmakers.co.kr/index.php?mid=koreanScreenplays&page=%d" % (page)
        self.openPage( baseUrl )

        listLink = []
        if False :
            listElem = self.webDrv.find_elements_by_class_name('headline')
            if (self.isTxt == False ) :
                print("text file isnt configured.")
                return
            for i, elem in enumerate(listElem):
                try :
                    listLink.append(elem.find_element_by_tag_name('a').get_attribute('href'))
                except :
                    print( "[navigatePage] get_attribue in elem .. {}".format(elem.text) )
                    continue
        else :  # beautiful soup version
            html = self.webDrv.page_source
            soup = BeautifulSoup(html, 'html.parser')
            notices = soup.select('#board > tbody > tr > td.title > a')
            for n in notices:
                #print(n.text)
                print(n.get('href'))
                listLink.append(n.get('href'))

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
                    print("[history] add new page has exception.")
                    self.logger.updateHistory(url, "fail")
            else : print("[history]this page is already added.")
            sleep(1)

        self.logger.close()
    def crawContents(self,isShowContent):
        #article_title
        if False :
            xpathList = ["//*[@id=\"board\"]/div[2]/div[3]/div[2]/span[2]/div/p/a",
                         "//*[@id=\"board\"]/div[2]/div[3]/div[2]/span/div/p/a"]
            for xpath in xpathList :
                try :
                    elem = self.webDrv.find_element_by_xpath(xpath)
                    link_text = elem.text
                    self.webDrv.find_element_by_link_text(link_text).click()
                    break
                except Exception as e :
                    print("[Exception] in article_title = {}" , e)
                    continue
        else :
            class_file_box = "file-box"
            try :
                elem_file_boxs = self.webDrv.find_elements_by_class_name( class_file_box )
                for elem_file_box in elem_file_boxs :
                    elem_tag_a = elem_file_box.find_element_by_tag_name('a')
                    link_text = elem_tag_a.text
                    self.webDrv.find_element_by_link_text(link_text).click()
            except :
                print("[Exception] in article_title = {}", e)


#키워드로 보는 사설
MOD = crawler_movie_scene( False , "../Data/MovieScene/Korea" , "MovieSceneKr" , "영화시나리오" )
MOD.run()
MOD.close()



