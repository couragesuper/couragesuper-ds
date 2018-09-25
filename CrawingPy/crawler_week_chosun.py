import sys
import time
sys.path.append("../Common/Crawler")
sys.path.append("../Common/Util")

from mod_crawler_base import craw_base
from time import sleep
from selenium import webdriver

szKeyword    = "주간 조선"
szTitle      = "WeeklyChosun"

# histroy
#   20180827 : using unified common library

#book cosmos용 entity checker이다.
class crawler_chosunweek (craw_base):
    def __init__( self , isHidden, outdir, title, keyword ) :
        list = []
        self.keyword = keyword
        super().__init__(isHidden, outdir, title)
    def run(self):
        StartUrl = "http://weekly.chosun.com/client/news/passho.asp"
        super().run( StartUrl )
    def makeCateLinks(self):
        classNo = "ac"
        elem = self.webDrv.find_element_by_class_name(classNo)
        self.max_page = int( elem.text.split("호")[0] )
        print( "[Crawler][ChosunWeekly] maximum page = {}".format( self.max_page ) )
        # Hueristic value
        self.min_page = 2092
        return
    def naviSites(self):
        #iterative the series specified number
        for page in range( self.max_page , self.min_page , -1 ) :
            print( "[Crawler][ChosunWeekly] page={}".format( page ) )
            SeriesUrl = "http://weekly.chosun.com/client/news/alllst.asp?nHo=%d" % (page)
            self.openPage( SeriesUrl )
            self.navigate( SeriesUrl )
            self.logger.close()
        sleep(1)
    def navigate(self , link):
        if False :
            class_line = "at"
            elem_list = self.webDrv.find_elements_by_class_name(class_line)
            listLink = []
            for i, elem in enumerate(elem_list):
                listAElem = elem.find_elements_by_tag_name('a')
                if (len(listAElem) != 0):
                    url = listAElem[0].get_attribute('href')
                    print(i, elem.text, url)
                    listLink.append(url)
        else :
            listAElem = self.webDrv.find_elements_by_tag_name('a')
            listUrl = []
            for i, elem in enumerate(listAElem):
                url = elem.get_attribute('href')
                # print(i, elem.text , url )
                if (url.find("NewsNumb") != -1):
                    print(i, elem.text, url)
                    listUrl.append(url)
            listLink = list(set(listUrl))
        sleep(1)
        for urlContent in listLink :
            if (self.logger.getHistory(urlContent) == False):
                try:
                    print("[history]add new page")
                    start_time = time.time()
                    self.openPage(urlContent)
                    self.crawContent(True)
                    self.logger.updateHistory(urlContent, "ok")
                except:
                    print("")
                    self.logger.updateHistory(urlContent, "fail")
            else:
                print("[history]this page is already added.")
    def crawContent(self,isShowContent):
        print("crawContents =".format(isShowContent))
        css_title = "title_title"
        elem = self.webDrv.find_element_by_class_name(css_title)
        txt = elem.text.split("\n")[0]
        print("{}={}".format(css_title, txt))
        txt_cate = ""
        txt_title = txt
        if( (txt.find("[") != -1) and (txt.find("]") != -1) ) :
            txt_cate  = txt[ txt.find("[") + 1:txt.find("]") ]
            txt_title = txt[ txt.find("]") + 1:].lstrip()
        self.txt.write( txt_cate )
        self.txt.write( txt_title )
        if( isShowContent ) : print( "title = {}".format(txt) )
        css_author = "name_ctrl"
        elem = self.webDrv.find_element_by_class_name(css_author)
        txt = elem.text.split()[0]
        print("{}={}".format(css_title, txt))
        self.txt.write( txt )
        if (isShowContent): print("name = {}".format(txt))
        css_article = "article_body"
        elem = self.webDrv.find_element_by_class_name(css_article)
        txt = elem.text.replace("  ", "").replace("\n", "  ")
        print("{}={}".format(css_article, txt))
        self.txt.writeLast( txt )
        if (isShowContent): print("content = {}".format(txt))

def Main() :
   listTxtColumn = ['title','category','writer','content']
   mod = crawler_chosunweek(False,"../Data/Text/ChosunWeekly","WeeklyChosun_","WeeklyChosun")
   mod.setTxtColumn( listTxtColumn )
   mod.run()
   mod.close()

Main()