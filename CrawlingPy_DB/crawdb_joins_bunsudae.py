import sys
import time
sys.path.append("../Common/Crawler")
sys.path.append("../Common/Util")
sys.path.append("../Common/Mysql")
from mod_crawler_db import crawler_engine_db
from time import sleep
from libmysql import dbConMysql

testdbconfig = { 'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'Crawling', 'raise_on_warnings': True,}

class crawdb_joins_keyword ( crawler_engine_db ):
    def __init__( self , isHidden, config , contentIndex , keyword ) :
        self.keyword = keyword
        super().__init__(isHidden, config, contentIndex )
    def run(self):
        self.fetch()
    def fetch(self):
        baseUrl = "https://news.joins.com/find/list?page=%d&IsDuplicate=True&key=EditorialColumn&Keyword=%s&SourceGroupType=Joongang" % ( 1, self.keyword)
        self.openPage(baseUrl)

        #max_page = self.getMaxPages()
        max_page = 337
        print("[navigate] maxpage is found = {} ", max_page)

        delayPage = 0.5
        delayScrap = 1

        for i in range( 1 , max_page + 1):
            page = i
            now = time.localtime()
            baseUrl = "https://news.joins.com/find/list?page=%d&IsDuplicate=True&key=EditorialColumn&Keyword=%s&SourceGroupType=Joongang" % ( page, self.keyword)
            self.openPage(baseUrl)
            listLink = []
            listElem = self.webDrv.find_elements_by_class_name('headline')
            for i, elem in enumerate(listElem):
                try:
                    listLink.append(elem.find_element_by_tag_name('a').get_attribute('href'))
                except:
                    print("[navigatePage] get_attribue in elem .. {}".format(elem.text))
                    continue
            for i, elem in enumerate(listLink):
                url = listLink[i]
                if (super().isExistData(url,None,None) == False):
                     try:
                        print("[history]add new page")
                        start_time = time.time()
                        self.openPage(url)
                        self.scrape(url,True,False)
                        sleep(delayScrap)
                     except Exception as e:
                        print("[history] add new page has exception.= {}".format(e))
                        super().writeData( url , False   )
                else:
                    if( super().isFailedData( url) ) :
                        print("[history]add new page")
                        start_time = time.time()
                        self.openPage(url)
                        self.scrape(url,True,True)
                        sleep(delayScrap)
                    else :
                        print("[history]this page is already added.")
            sleep(delayPage)
        self.navigate( baseUrl )

    def getMaxPages(self):
        baseUrl = "https://news.joins.com/find/list?page=1&IsDuplicate=True&key=EditorialColumn&Keyword=%s&SourceGroupType=Joongang" % (self.keyword)
        css_name = "btn_next"
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
            sleep(1)

    def scrape(self, url, isShowContent , isUpdate):

        title = None
        datadate = None
        profile = None
        Keywords = None
        txt_proc = None

        #1.article_title
        try :
            elem = self.webDrv.find_element_by_id('article_title')
            title = elem.text
            if( isShowContent ):print("[crawContents] article_title - {}".format(title) )
        except Exception as e :
            print("[crawContents] in article_title = {}".format(e))

        #2.byline
        try :
            elem = self.webDrv.find_element_by_class_name('byline')
            datadate = elem.text.split()[2]
            if (isShowContent):print("[crawContents] date - {}".format(datadate))
        except Exception as e:
            print("[crawContents] in byline = {}".format(e))

        #3.profile
        try :
            elem = self.webDrv.find_element_by_class_name('profile')
            profile = elem.text
            if (isShowContent):print("[crawContents] profile - {}".format(profile))
        except Exception as e:
            print("[crawContents] in profile = {}".format(e))

        #4.tags , |로 구분
        try :
            elem = self.webDrv.find_element_by_class_name('tag_list')
            listTags = elem.text.split("#")[1:]
            Keywords = ""
            for tags in listTags:
                Keywords += tags.replace("\n", "")
                Keywords += "|"
        except Exception as e:
            print("[crawContents] in tag_list = {}".format(e))

        #article_body
        try :
            elem = self.webDrv.find_element_by_class_name('article_body')
            text = elem.text
            txt_proc = text.replace("\n", "  ")
            txt_proc = txt_proc.replace( "\"" , "\"\"" )
            if (isShowContent):print(txt_proc)
        except Exception as e:
            print("[crawContents] in article_body = {}".format(e))

        try :
            if( isUpdate == True ) :
                retQuery = super().updateData( url , True, Keywords , datadate , title , profile , txt_proc )
            else :
                retQuery = super().writeData( url , True, Keywords , datadate , title , profile , txt_proc )
                if( retQuery == False ) :
                    super().writeData( url, False )
        except Exception as e:
            print("[crawContents] in WriteData = {}".format(e))

MOD = crawdb_joins_keyword( False, testdbconfig, 1 , "분수대")
MOD.run()
MOD.close()







