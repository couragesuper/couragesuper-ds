import sys
import time
sys.path.append("C:/Users/couragesuper/PycharmProjects/SampleProject/venv/Common")

from Crawler import mod_craw as craw
from Crawler.mod_craw_logger import Crawler_Logger as logger
from time import sleep

listSectionNm    = ['종합', '정치', '경제', '사회', '생활/문화', '세계', 'IT/과학', '포토', 'TV']
listSectionID    = ['100', '101', '102', '103', '104', '105', '106', '003', '115']

#  이 파일은 관리되지 않습니다.
#  일반 함수 버전입니다.

def crawler_joins_maxpage( wd, topic ) :
    baseUrl = "https://news.joins.com/find/list?page=1&IsDuplicate=True&key=EditorialColumn&Keyword=%s&SourceGroupType=Joongang" % (topic)
    css_name = "btn_next"
    craw.OpenWebPage(wd, baseUrl, 1)
    while( True ) :
        elem = wd.find_element_by_class_name( css_name )
        pos =  elem.text.find("없음")
        if( pos == -1 ) :
            print("다음페이지 있음")
            elem.click()
        else :
            print("다음페이지 없음")
            elems = wd.find_elements_by_class_name( 'link_page' )
            listPages = []
            for eobj in elems:
                listPages.append( int(eobj.text) )
            listPages = sorted( listPages , reverse = True )
            return listPages[0]
        sleep(0.5)

def crawler_joins_keyword( wd, keyword, page , isShowContent):
    now = time.localtime()
    #time_str = "%04d%02d%02d_%02d%02d%02d_from%d_to%d" % ( now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    logger_craw = logger( keyword + ".xml" , False )
    with open("scrap\\bunsudae\\joins_bunsudae.txt", "a+", encoding='utf-8') as f:
        print(page)
        baseUrl = "https://news.joins.com/find/list?page=%d&IsDuplicate=True&key=EditorialColumn&Keyword=%s&SourceGroupType=Joongang" % (page , keyword)
        craw.OpenWebPage(wd, baseUrl, 1)
        listLink = []
        listElem = wd.find_elements_by_class_name('headline')
        for i, elem in enumerate(listElem):
            listLink.append(elem.find_element_by_tag_name('a').get_attribute('href'))
        for i, elem in enumerate(listLink):
            url = listLink[i]
            dicRet = logger_craw.getHistory(url)
            if( (dicRet['check'] == 'fail') or ((dicRet['check'] == 'ok') and (dicRet['ret'] == 'fail'))) :
                try :
                    start_time = time.time()
                    craw.OpenWebPage(wd, listLink[i], 1)
                    elem = wd.find_element_by_id('article_title')
                    txt_head = elem.text
                    f.write(txt_head)
                    f.write("\t")
                    elem = wd.find_element_by_class_name ('byline')
                    txt_date_input = elem.text.split()[2]
                    f.write(txt_date_input)
                    f.write("\t")
                    elem = wd.find_element_by_class_name('profile')
                    txt_profile = elem.text
                    f.write(txt_profile)
                    f.write("\t")
                    elem = wd.find_element_by_class_name('article_body')
                    txt_org = elem.text
                    txt_proc = txt_org.replace("\n", "  ")
                    if( isShowContent ) : print(  txt_proc)
                    f.write(txt_proc)
                    f.write("\n")
                    print( "Title:%s Writer:%s interval:%d" % ( txt_head, txt_profile, (time.time() - start_time)) )
                    logger_craw.updateHistory( url , "ok" )
                except :
                    logger_craw.updateHistory( url , "fail" )
            sleep(1)
    logger_craw.updateXML()

def Main() :
    wd = craw.InitWebDriver(False, False)
    keyword = "분수대"
    #max_page = crawler_joins_maxpage( wd, keyword )
    max_page = 394
    for i in range(1,max_page + 1) :
        crawler_joins_keyword( wd, keyword, i , False )
        sleep(2)
Main()