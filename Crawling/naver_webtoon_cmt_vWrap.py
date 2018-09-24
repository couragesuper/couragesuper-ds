import sys
import time
sys.path.append("../Common/Crawler")
sys.path.append("../Common/Util")

from mod_crawler_base import crawler_engine
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup

class crawler_naver_moive (crawler_engine):
    def __init__( self , isHidden, outdir, title, keyword ) :
        self.keyword = keyword
        super().__init__(isHidden, outdir, title)
    def setMovieID (self,movieID):
        self.movieID = movieID
    def run(self):
        self.fetch()
    def fetch(self):
        now = time.localtime()
        url = "https://movie.naver.com/movie/bi/mi/detail.nhn?code=%d" % (self.movieID)
        if (True or self.logger.getHistory(url) == False):
            #try:
                print("[history]add new page")
                start_time = time.time()
                self.openPage(url)
                self.scrape(True)
                self.logger.updateHistory(url, "ok")
            #except:
            #    print("[history] add new page has exception.")
            #    self.logger.updateHistory(url, "fail")
        else:
            print("[history]this page is already added.")
        sleep(1)
        self.logger.close()
        sleep(2)
    def scrape(self,isShowContent):
        req = self.webDrv.page_source
        soup = BeautifulSoup( req , "html.parser")

        # title : #content > div.article > div.mv_info_area > div.mv_info > h3 > a
        elem_text = soup.select("#content > div.article > div.mv_info_area > div.mv_info > h3 > a")

        # #content > div.article > div.mv_info_area > div.mv_info > strongd

# 대학일기
szMovieName  = "인테스텔라"
szMovieID    = 45290
szKeyword    = "네이버영화"
szKeyword_En = "NaverMovie"

MOD = crawler_naver_moive( False , "../Data/Text/NaverMovie/" + str(szMovieID) , szKeyword_En , szKeyword )
MOD.setMovieID( szMovieID )
MOD.run()
MOD.close()

