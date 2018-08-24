import sys
import time
import datetime
sys.path.append("../Common/Crawler")
sys.path.append("../Common/Util")

from mod_crawler_base import craw_base
from time import sleep
from selenium import webdriver

# joins
    # histroy
    #   20180828 : created
    #               - this crawler craws the articls with range of date

#book cosmos용 entity checker이다.
class crawler_naver_sec_rank (craw_base):
    def __init__( self , isHidden, outdir, title, keyword , sectionID , startDate, endDate ) :
        self.keyword     = keyword
        super().__init__(isHidden, outdir, title)
        self.sectionID   = sectionID
        self.startDate   = startDate
        self.endDate     = endDate
    def run(self):
        super().run( "" )
    def naviSites(self):
        # 시계열 순회를 하려면...
        _start = datetime.datetime.strptime(self.startDate, '%Y%m%d')
        _end = datetime.datetime.strptime(self.endDate, '%Y%m%d')
        step = datetime.timedelta(days=1)
        _cur = _start
        while _cur < _end:
            #print(_cur.strftime("%Y%m%d"))
            self.curDate = _cur.strftime("%Y%m%d")
            print("[Crawler_Joins_Kwd] SecitonID:%s Data:%s" % (self.sectionID, self.curDate))
            urlPage = "https://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId=%s&date=%s" % (self.sectionID, self.curDate)
            self.openPage(urlPage)
            self.navigate(urlPage)
            _cur = _cur + step
            sleep(1)
    # process the unit of page lists
    def navigate(self , link):
        listSections = []
        listSections_URL = []
        listElem = self.webDrv.find_elements_by_class_name('ranking_item')
        for i, elem in enumerate(listElem):
            listSections.append(elem.text.split("\n")[0])
            listSections_URL.append(elem.find_element_by_tag_name('a').get_attribute('href'))
        css_head = "tts_head"
        css_contents = "article_body"
        for i, url in enumerate(listSections_URL):
            if (self.logger.getHistory(url) == False):
                try:
                    self.openPage(url)
                    self.crawContents(i+1,True)
                    self.logger.updateHistory(url, "ok")
                except:
                    print("")
                    self.logger.updateHistory(url, "fail")
            else:
                print("[history]this page is already added.")
            sleep(1)
        self.logger.close()
    # process the unit of one page
    def crawContents(self,rank,isShowContent):
        css_head = "tts_head"
        css_contents = "article_body"
        try:
            #1.date
            self.txt.write( self.curDate )
            #2.rank
            self.txt.write( str(rank) )
            #3. title
            elem = self.webDrv.find_elements_by_class_name(css_head)
            txt = elem[0].text
            if (isShowContents): print(txt)
            self.txt.write(txt)
            #4. content
            elem = self.webDrv.find_elements_by_class_name(css_contents)
            content_txt = elem[0].text.replace("\n", "  ").replace("\r", "  ")
            pos1 = content_txt.find("좋아요")
            pos2 = content_txt.find("훈훈해요")
            if ((pos2 - pos1) < 20): content_txt = content_txt[:pos1]
            if (isShowContents): print(content_txt)
            self.txt.writeLast(content_txt)
            sleep(delay_per_url)
        except Exception as e:
            print( "[naverseciton] Date:%s %d "  % (self.curDate, rank) )

#키워드로 보는 사설
listSectionNm    = ['종합', '정치', '경제', '사회', '생활/문화', '세계', 'IT/과학', '포토', 'TV']
listSectionID    = ['100', '101', '102', '103', '104', '105', '106', '003', '115']

def Main() :
    MOD = crawler_naver_sec_rank( False, "../Data/Text/Naver/Section/100" , "Naver_News_Sec_100" , "네이버_섹션_뉴스_종합" , 100 , '20180101', '20180828' )
    MOD.run()
Main()




