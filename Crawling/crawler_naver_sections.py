import sys
import time
import mod_craw as craw
from time import sleep

listSectionNm    = ['종합', '정치', '경제', '사회', '생활/문화', '세계', 'IT/과학', '포토', 'TV']
listSectionID    = ['100', '101', '102', '103', '104', '105', '106', '003', '115']


def craw_naver_section_ymd( wd , ymd , sectionID, delay_per_url , isShowContents ) :
    listSections = []
    listSections_URL = []
    #1.open page
    urlSect = "https://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId=%s&date=%s" % ( sectionID, ymd )
    craw.OpenWebPage(wd, urlSect ,1)
    #2.obtains the lists of article links
    listElem = wd.find_elements_by_class_name( 'ranking_item' )
    for i,elem in enumerate( listElem ):
        listSections.append( elem.text.split("\n")[0] )
        listSections_URL.append( elem.find_element_by_tag_name('a').get_attribute('href')  )
    #3.iterates the links and crawl the contents
    with open("scrap\\naver\\naver_section_" + str(sectionID) + "_" + str(ymd) + ".txt", "w+", encoding='utf-8') as f:
        idx = 0
        css_head = "tts_head"
        css_contents = "article_body"
        for i,url in enumerate( listSections_URL ):
            try:
                craw.OpenWebPage(wd, url, 1)
                # 1.TODAY_INDEX
                f.write(str(idx))
                f.write("\t")
                idx = idx + 1

                if False :
                    # 2.time_str_day
                    f.write(time_str_day)
                    f.write("\t")
                # 3.TITLE
                elem = wd.find_elements_by_class_name(css_head)
                if( isShowContents ) : print(elem[0].text)
                f.write(elem[0].text)
                f.write("\t")
                # 4.CONTENT
                elem = wd.find_elements_by_class_name(css_contents)
                content_txt = elem[0].text.replace("\n", "  ").replace("\r", "  ")
                # 5.Remove the useless area
                pos1 = content_txt.find("좋아요")
                pos2 = content_txt.find("훈훈해요")
                if ((pos2 - pos1) < 20) : content_txt = content_txt[:pos1]
                if( isShowContents ) : print(content_txt)
                f.write(content_txt)
                f.write("\n")
                sleep(delay_per_url)
            except Exception as e:
                print( "date:%s section:%s url:%s" % ( str(ymd) , str(sectionID), url ) )
                continue

def Main() :
    time_now = time.localtime()

    # process with Periods
    listDate = [ "201807%02d" % i for i in range(1, time_now.tm_mday + 1) ]
    listSects = [100, 103, 104, 105, 106, 3, 115]
    listSectsAll = listSectionID.copy()

    delay_per_day = 15
    delay_per_url = 2.2

    wd = craw.InitWebDriver(False, False)

    for date in listDate :
        for section in listSects :
            print( "progress date:%s section:%s " % (date,section) )
            craw_naver_section_ymd( wd, date, section, delay_per_url , False )
            sleep( delay_per_day )
Main()




