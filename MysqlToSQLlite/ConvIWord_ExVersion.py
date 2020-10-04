import sys

sys.path.append("../Common")
from Mysql.libmysql import dbConMysql
import sqlite3


config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'mthx_app',
             'raise_on_warnings': True}

db = dbConMysql(config_db)
dbinput = dbConMysql(config_db)

ret_category = db.selectQueryWithRet("select * from tBibleIWordAdv;")
print( ret_category )

#ret = db.selectQueryWithRet("select * from tBibleIWordContAdv")
#print( ret )


iw_cateid = 0
iw_seq = 0
iw_subseq = 0
iw_subsubseq = 0

for category in ret_category['data'] :
    print( category )
    ret = db.selectQueryWithRet("select * from tBibleIWordContAdv where iw_cateid = {}".format(category['iw_cateid']))

    if( iw_cateid != category['iw_cateid'] ) :
        iw_seq = 0
        iw_subseq = 0
        iw_subsubseq = 0

    for word_sentence in ret['data'] :
        dicData = {}
        #print( word_sentence )

        if( word_sentence['iw_seq'] != iw_seq ) :
            iw_subseq = 1
            iw_subsubseq = 1
        if( word_sentence['iw_subseq'] != iw_subseq ) :
            iw_subsubseq = 1

        # search content in bible
        ret_k = {}
        ret_e = {}

        if( word_sentence['iw_bookseq'] <= 39) :
            ret_k = db.selectQueryWithRet(
                "select * from tBibleContV2 where bible_seq = 3 and book_seq = {iw_bookseq} and  book_chap = {iw_chapseq} and book_verse >= {iw_verse_begin} and book_verse <= {iw_verse_end} ".format(
                    iw_bookseq = word_sentence['iw_bookseq'],
                    iw_chapseq = word_sentence['iw_chapseq'],
                    iw_verse_begin = word_sentence['iw_verse_begin'],
                    iw_verse_end = word_sentence['iw_verse_end']
                ) )
            ret_e = db.selectQueryWithRet(
                "select * from tBibleContV2 where bible_seq = 1 and book_seq = {iw_bookseq} and  book_chap = {iw_chapseq} and book_verse >= {iw_verse_begin} and book_verse <= {iw_verse_end} ".format(
                    iw_bookseq=word_sentence['iw_bookseq'],
                    iw_chapseq=word_sentence['iw_chapseq'],
                    iw_verse_begin=word_sentence['iw_verse_begin'],
                    iw_verse_end=word_sentence['iw_verse_end']
                ))
        else :
            ret_k = db.selectQueryWithRet(
                "select * from tBibleContV2 where bible_seq = 4 and book_seq = {iw_bookseq} and  book_chap = {iw_chapseq} and book_verse >= {iw_verse_begin} and book_verse <= {iw_verse_end} ".format(
                    iw_bookseq=word_sentence['iw_bookseq'],
                    iw_chapseq=word_sentence['iw_chapseq'],
                    iw_verse_begin=word_sentence['iw_verse_begin'],
                    iw_verse_end=word_sentence['iw_verse_end']
                ))
            ret_e = db.selectQueryWithRet(
                "select * from tBibleContV2 where bible_seq = 2 and book_seq = {iw_bookseq} and  book_chap = {iw_chapseq} and book_verse >= {iw_verse_begin} and book_verse <= {iw_verse_end} ".format(
                    iw_bookseq=word_sentence['iw_bookseq'],
                    iw_chapseq=word_sentence['iw_chapseq'],
                    iw_verse_begin=word_sentence['iw_verse_begin'],
                    iw_verse_end=word_sentence['iw_verse_end']
                ))
        query = "insert into tBibleIWordContAdv2 (iw_cateid , iw_seq, iw_subseq, iw_subsubseq, iw_content, iw_bookseq, iw_chapseq, iw_verse_begin, iw_verse_end, book_contentk, book_contente ) values "\
            "( {iw_cateid} , {iw_seq}, {iw_subseq}, {iw_subsubseq}, '{iw_content}', {iw_bookseq}, {iw_chapseq}, {iw_verse_begin}, {iw_verse_end}, '{book_contentk}', '{book_contente}' )"

        #print( ret_e )
        #print( ret_k )

        idx = 0
        for elem in ret_k['data'] :
            dicData = { "iw_cateid":word_sentence['iw_cateid']
                , "iw_seq":word_sentence['iw_seq']
                , "iw_subseq":word_sentence['iw_subseq']
                , "iw_subsubseq":iw_subsubseq
                , "iw_content": str(word_sentence['iw_content'])
                , "iw_bookseq":word_sentence['iw_bookseq']
                , "iw_chapseq":word_sentence['iw_chapseq']
                , "iw_verse_begin":word_sentence['iw_verse_begin']
                , "iw_verse_end":word_sentence['iw_verse_end']
                , "book_contentk": str(ret_k['data'][idx]['book_content'])
                , "book_contente": str(ret_e['data'][idx]['book_content'])  }
            dicData['book_contentk'] = dicData['book_contentk'].replace('"', '""')
            dicData['book_contente'] = dicData['book_contente'].replace('"', '""')
            dicData['book_contentk'] = dicData['book_contentk'].replace("'", "''")
            dicData['book_contente'] = dicData['book_contente'].replace("'", "''")
            idx = idx + 1
            iw_subsubseq = iw_subsubseq + 1
            #print( dicData )
            real_query = query.format( **dicData )
            dbinput.commitQuery( real_query )
