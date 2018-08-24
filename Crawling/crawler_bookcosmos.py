import sys
import time
sys.path.append("../Common/Crawler")
sys.path.append("../Common/Util")

from mod_crawler_base import craw_base
from time import sleep
from selenium import webdriver

# history
# 20180827 .
#   running test
#   xml working is well

class Crawler_Bookcosmos( craw_base ) :
    def __init__( self , isHidden, outDir, title ) :
        super().__init__( isHidden, outDir, title )
        self.dict_xpath = {"userid": "/html/body/div/div[2]/div/ul[1]/li[1]/form/div/div[1]/input[1]",
                      "userpw": "/html/body/div/div[2]/div/ul[1]/li[1]/form/div/div[1]/input[2]",
                      "btnlogin": "//*[@id=\"btnLogin\"]",
                      "link_main": "/html/body/div/div[2]/div/ul[1]/li[2]/a",
                      "list_main_1": "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[1]/table[3]/tbody/tr[1]/td/table[2]/tbody/tr[1]/td/table[1]",
                      "list_main_2": "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[1]/table[3]/tbody/tr[1]/td/table[2]/tbody/tr[1]/td/table[2]",
                      "cnt_title": "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/div[1]/p",
                      "cnt_author": "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/div[2]",
                      "cnt_pub": "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/div[3]",
                      "cnt_pub_date": "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/div[4]",
                      "xpath_word_dn": "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/table/tbody/tr/td/div[2]/div[2]/a[1]",
                      "xpath_hangul_dn": "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/table/tbody/tr/td/div[2]/div[2]/a[2]",
                      "xpath_pdf_dn": "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/table/tbody/tr/td/div[2]/div[2]/a[3]"}
        self.lists_content_xpath= [ "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/a",
            "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[3]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/a",
            "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[5]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/a",
            "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[5]/td/table/tbody/tr/td[3]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/a",
            "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[9]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/a",
            "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[9]/td/table/tbody/tr/td[3]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/a",
            "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[13]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/a",
            "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[13]/td/table/tbody/tr/td[3]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/a",
            "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[17]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/a",
            "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[17]/td/table/tbody/tr/td[3]/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/a"]
        self.dict_page_xpath = { "title_in_page":"/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/div[1]/p",
            "Writer":"/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/div[2]",
            "Company":"/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/div[3]",
            "DatePublished":"/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/div[4]",
            "Category":"/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/div[5]",
            "Content":"//*[@id=\"contentForm\"]/tbody/tr[1]/td/table/tbody/tr/td",
            "dn_word":"/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/table/tbody/tr/td/div[2]/div[2]/a[1]",
            "dn_hangul":"/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/table/tbody/tr/td/div[2]/div[2]/a[2]",
            "dn_pdf":"/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/div[1]/div/table/tbody/tr/td[2]/table/tbody/tr/td/div[2]/div[2]/a[3]"}
        self.delay_dn = 1.5
    def login(self):
        #fill id and pw
        elem = self.webDrv.find_element_by_xpath(self.dict_xpath["userid"])
        elem.clear()
        elem.send_keys("hamtorigun")
        elem = self.webDrv.find_element_by_xpath(self.dict_xpath["userpw"])
        elem.clear()
        elem.send_keys("saturn")
        self.webDrv.find_element_by_xpath(self.dict_xpath["btnlogin"]).click()
        self.webDrv.find_element_by_xpath(self.dict_xpath["link_main"]).click()
    def makeCateLinks(self):
        self.listSiteMapLink = []
        # 2 group is exists
        elemGrp1 = self.webDrv.find_element_by_xpath(self.dict_xpath["list_main_1"])
        elemGrp2 = self.webDrv.find_element_by_xpath(self.dict_xpath["list_main_2"])
        listGrp1 = elemGrp1.find_elements_by_class_name("text_under");
        listGrp2 = elemGrp2.find_elements_by_class_name("text_under");
        listTags = elemGrp1.find_elements_by_tag_name('a')
        for elem in listTags:
            self.listSiteMapLink .append(elem.get_attribute('href'))
        listTags = elemGrp2.find_elements_by_tag_name('a')
        for elem in listTags:
            self.listSiteMapLink .append(elem.get_attribute('href'))
    def naviSites(self):
        for link in self.listSiteMapLink :
            print( "Cate ={}".format( link ) )
            self.openPage(link)
            self.navigate(link)
            sleep(1)
    def navigate(self , link):
        # get max pages
            # bookcosmos maxpage has function to go to last page , so we dont need loop
        xpath_next_btn = "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[2]/td/a[11]/img"
        xpath_last     = "/html/body/table/tbody/tr/td/table/tbody/tr[1]/td[1]/table/tbody/tr/td/table[4]/tbody/tr/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[2]/td/strong/font"
        self.webDrv.find_element_by_xpath(xpath_next_btn).click()
        elem           = self.webDrv.find_element_by_xpath(xpath_last)
        maxpage        = int(elem.text)
        print("\tnavigatePages : maxpage:{}".format(maxpage))
        # loop for pages
        for page in range(1,maxpage + 1):
            print("\t\t: page:{}".format(page))
            pagelink = link + "&page=%d" % (page)
            self.openPage(pagelink)
            self.navigatePage()
            sleep(0.5)
            print("save logger");
            self.logger.close()
    def navigatePage(self):
        listBooksUrl = []
        for xpath in self.lists_content_xpath :
            try :
                elem = self.webDrv.find_element_by_xpath(xpath)
                listBooksUrl.append( elem.get_attribute('href'))
            except :
                print("{} is failed".format( xpath ))
                continue
        for BookUrl in listBooksUrl :
            if( self.isLogger ) :
                if( self.logger.getHistory(BookUrl) == False ) :
                    self.openPage(BookUrl)
                    if( self.isTxt ) :
                        self.crawContents()
                    #download
                    elem = self.webDrv.find_element_by_xpath(self.dict_page_xpath['dn_pdf'])
                    elem.click()
                    sleep(self.delay_dn)
                    self.logger.updateHistory(BookUrl,True)
                else:
                    print("[history]this page is already added.")
    def run(self):
        super().run("http://www.bookcosmos.com")
    def crawContents(self):
            # title
        elem = self.webDrv.find_element_by_xpath( self.dict_page_xpath['title_in_page'] )
        self.txt.write( elem.text )
            # writer
        elem = self.webDrv.find_element_by_xpath(self.dict_page_xpath['Writer'])
        self.txt.write(elem.text.strip().split(":")[1])
            # Company
        elem = self.webDrv.find_element_by_xpath(self.dict_page_xpath['Company'])
        self.txt.write(elem.text.strip().split(":")[1])
            # datepublish
        elem = self.webDrv.find_element_by_xpath(self.dict_page_xpath['DatePublished'])
        self.txt.write(elem.text.strip().split(":")[1])
            # Category
        elem = self.webDrv.find_element_by_xpath(self.dict_page_xpath['Category'])
        self.txt.write(elem.text.strip().split(":")[1])
            # Contents
        xpath = "//*[@id=\"contentForm\"]/tbody/tr[1]/td/table/tbody/tr/td"
        elem = self.webDrv.find_element_by_xpath(xpath)
        szContext = ""
        for content in elem.text.split("▣"):
            if (content.lower().find('Short Summary'.lower()) != -1):
                listContents = content.split("\n")[1:]
                for elem in listContents:
                    if (elem != ""):
                        szContext += elem
                        szContext += "  "
        self.txt.writeLast(szContext)

szTitle = "BookCosmos"
MOD = Crawler_Bookcosmos( False , "../Data/Text/BookCosmos" , szTitle )
listTxtColumn = ['title', 'writer', 'company','datepublish', 'category', 'Contents']
MOD.setTxtColumn(listTxtColumn)
MOD.run()
MOD.close()




