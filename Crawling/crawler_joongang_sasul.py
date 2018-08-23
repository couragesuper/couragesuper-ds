isLinux = False
isHidden = False
isShowContent = False

import time
import sys

sys.path.append('lib')
import mod_craw as craw
from time import sleep

delay_sleep = 1.2
wd = craw.InitWebDriver(isLinux, isHidden)

listTopic = ['책속으로', '책 속으로']

def crawler_joins_maxpage( topic ) :
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

crawler_joins_maxpage( listTopic[1] )
exit(0)

def crawler_joongang_books(page_start, page_end):
    now = time.localtime()
    time_str = "%04d%02d%02d_%02d%02d%02d_from%d_to%d" % (
    now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec, page_start, page_end)
    with open("scrap\\bunsudae\\joongang_opnion_bunsudae_" + time_str + ".txt", "w+", encoding='utf-8') as f:
        for i in range(page_start, page_end):
            print(i)
            baseUrl = "https://news.joins.com/find/list?page=%d&IsDuplicate=True&key=EditorialColumn&Keyword=%s&SourceGroupType=Joongang" % (i , topic)
            craw.OpenWebPage(wd, baseUrl, 1)

            listLink = []
            listElem = wd.find_elements_by_class_name('headline')
            for i, elem in enumerate(listElem):
                listLink.append(elem.find_element_by_tag_name('a').get_attribute('href'))

            for i, elem in enumerate(listLink):
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
            sleep(delay_sleep)

for i in range( 1, 230, 10 ) :
    crawler_joongang_bunsudae( i, i + 9 )
    sleep( 20 )

