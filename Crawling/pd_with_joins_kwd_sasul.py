import pandas as pd
from collections import defaultdict
from collections import Counter

import sys
import time
sys.path.append("C:/Users/couragesuper/PycharmProjects/SampleProject/venv/Common/Crawler")

from mod_craw_logger import Crawler_Logger as LOGGER
from mod_craw_filereader import cTxtReader as TXTREADER
from mod_crawler_base import crawler_base as crawler_main

# 특수문자 특수 기호를 제거해야 함.
#

if True :
    df = pd.read_csv("joins_bunsudae_edit.txt", sep="\t")
    print( df.columns )

    #fillna 처리
    df['profile'] = df['profile'].fillna('unknown')
    df['tag_list'] = df['tag_list'].fillna('|')
    df['article_body'] = df['article_body'].fillna('no data')
    print( df.info() )

    if False :
        #1.Counter 작업
        listAllKeyword = []
        def countKeyword( x ) :
            try :
                listElem = x.split("|")
                for elem in listElem:
                    listAllKeyword.append( elem )
            except :
                print(x)
        df['tag_list'].apply( countKeyword )
        cnt_kwd = Counter( listAllKeyword )

    if False :
        print( cnt_kwd )
else :
    txtreader = TXTREADER("joins_bunsudae_edit.txt" , True , True )
    for sent in txtreader :
        print( sent )




