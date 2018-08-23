import sys
import time
sys.path.append("C:/Users/couragesuper/PycharmProjects/SampleProject/venv/Common/Crawler")

import mod_craw as craw
from mod_craw_logger import Crawler_Logger as LOGGER
from mod_craw_filewriter import crawler_filewriter as FT
from mod_crawler_base import crawler_base as crawler_main

from time import sleep
import datetime

def date_range(start_date, end_date):
    for ordinal in range(start_date.toordinal(), end_date.toordinal()):
        yield datetime.date.fromordinal(ordinal)

#book cosmos용 entity checker이다.
class crawler_naver_news_ranking (crawler_main):
    def __init__( self , isLinux, isHidden, keyword_en, keyword , start_date, end_date ) :
        self.keyword = keyword
        super().__init__(isLinux,isHidden, keyword_en)
        self.listSectionNm = ['종합', '정치', '경제', '사회', '생활/문화', '세계', 'IT/과학', '포토', 'TV']
        self.listSectionID = []
        self.dictSection = { '종합':'100',  '정치':'101', '경제':'102', '사회':'103', '생활/문화':'104', '세계':'105', 'IT/과학':'106', '포토':'003', 'TV':'115' }
        self.start_date = start_date
        self.end_date   = end_date
    def run(self):
        baseUrl = "https://news.naver.com"
        super().run( baseUrl )
    def openNewFile(self, ymd, section ):
        self.closeTxt()
        self.createTxt("scrap/naver_rank/naver_rank_{}_{}".format(ymd,section))
    def naviSites(self):
        for k,v in self.dictSection.items() :
            for single_date in date_range(self.start_date, self.end_date):
                listTitles = []
                listUrls = []
                sec = int(v)
                ymd = single_date.strftime("%Y%m%d")
                self.openNewFile(ymd,sec)
                urlbase = "https://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId=%s&date=%s" % (sec,ymd)
                self.openPage(urlbase)
                listElem = self.webDrv.find_elements_by_class_name('ranking_item')
                for i, elem in enumerate(listElem):
                    listTitles.append(elem.text.split("\n")[0])
                    listUrls.append(elem.find_element_by_tag_name('a').get_attribute('href'))
                for url in listUrls:
                    if (self.logger.getHistory(url) == False):
                        if False :
                            self.crawContents(sec, ymd, url, True)
                        else :
                            try:
                                self.crawContents(sec,ymd,url,True)
                                self.logger.updateHistory(url, "ok")
                            except Exception as e:
                                print("error -- date:%s section:%s url:%s" % (str(ymd), str(sec), url))
                                self.logger.updateHistory(url, "fail")
                    else :
                        print("skip:date:%s sec:%s url:%s" % (str(ymd),str(sec),url ))
                    self.logger.close()
                    sleep(1.2)
                sleep(1)
                self.closeTxt()

    def crawContents(self,sec,ymd,url,isShowContent):
        css_head = "tts_head"
        css_contents = "article_body"
        self.openPage(url)
        elem = self.webDrv.find_elements_by_class_name(css_head)
        if (isShowContent): print(elem[0].text)
        self.txt.write(elem[0].text)
        # 2.CONTENT
        elem = self.webDrv.find_elements_by_class_name(css_contents)
        content_txt = elem[0].text.replace("\n", "  ").replace("\r", "  ")
        # 3.Remove the useless area
        pos1 = content_txt.find("좋아요")
        pos2 = content_txt.find("훈훈해요")
        if ((pos2 - pos1) < 20): content_txt = content_txt[:pos1]
        if (isShowContent): print(content_txt)
        self.txt.writeLast(content_txt)



MOD = crawler_naver_news_ranking(False, False, "NaverNews", "20180707" , datetime.datetime(2018,1,1) , datetime.datetime(2018,8,13))
MOD.run()
MOD.close()




