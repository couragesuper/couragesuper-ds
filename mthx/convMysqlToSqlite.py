import sys

sys.path.append("../Common")
from Mysql.libmysql import dbConMysql
import sqlite3
import urllib

# convertor mysql to sqlite
# 20200707 : (mthx_2nd)
    # bible , qt , poem , sermon , iword
# 20200714 : (mthx_3nd)
    # add paragraph title to biblecont
# 20200715: (mthx_4th)
    # add word for praise
# 20200908 : splitting version
# 20200919 : make final url
# 20200922 : bible (paragraph)

dbName_Bible = "bible_20200922.db"
dbName_Content = "shinechurch_20200922.db"

# mysql -> sqlite3 database

print("sqlite3.version:{}".format(sqlite3.version))
print("sqlite3.sqlite_version:{}".format(sqlite3.sqlite_version))

config_db_org = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
             'raise_on_warnings': True}
config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'mthx_app',
             'raise_on_warnings': True}

db = dbConMysql(config_db)
con_bible = sqlite3.connect( dbName_Bible )
con_cont = sqlite3.connect( dbName_Content )


with con_bible:
    cursor = con_bible.cursor()
    dictCreateQueries = {
        "tbible": {"create": "CREATE TABLE tBible( bibleSeq int, bibleType text,bibleDesc text )",
                   "select": "select * from tBible",
                   "insert": 'INSERT INTO tBible VALUES( {bibleSeq} ,"{bibleType}" ,"{bibleDesc}")'
                   ,"isInsert" : True}
        , "tbibleBook": {
            "create": "CREATE TABLE tBibleBook (biblebook_seq int, biblebook_type text, biblebook_krnm text, biblebook_engnm text, biblebook_krsumnm text)",
            "select": "select * from tBibleBook",
            "insert": 'INSERT INTO tBibleBook VALUES( {biblebook_seq} , "{biblebook_type}" ,"{biblebook_krnm}" ,"{biblebook_engnm}", "{biblebook_krsumnm}")'
            ,"isInsert" : True
        }

        , "tbibleCont": {
            "create": "CREATE TABLE tBibleCont ( bible_seq int, book_seq int, book_chap int, book_verse int, book_content text, book_paratitle )",
            "select": "select * from tBibleContV2",
            "insert": 'INSERT INTO tBibleCont VALUES( {bible_seq} , {book_seq} , {book_chap}, {book_verse} ,"{book_content}" ,"{book_paratitle}" )'
            , "isInsert": True
        }
        , "tbibleqt": {
            "create": "CREATE TABLE tBibleQtCont(  bibleqt_seq int,  bibleqt_type int,  bibleqt_day int,  bibleqt_mon int,  bibltqt_content text, bibleqt_data text)",
            "select": "select * from tBibleQtCont",
            "insert": 'INSERT INTO tBibleQtCont VALUES ( {bibleqt_seq}, {bibleqt_type}, {bibleqt_day}, {bibleqt_mon}, "{bibltqt_content}" , "{bibleqt_data}" )'
            , "isInsert": True
        }
        , "tbibleIWord": {
            "create": "CREATE TABLE tBibleIWord (  bibleiword_seq int,  bibleiword_nm text,  bibleiword_desc text )",
            "select": "select * from tBibleIWord",
            "insert": 'insert into tBibleIWord (bibleiword_seq ,  bibleiword_nm ,  bibleiword_desc  ) values( {bibleiword_seq} , "{bibleiword_nm}", "{bibleiword_desc}" )'
            , "isInsert": True
        }
        , "tbibleIWordCont": {
            "create": "CREATE TABLE tBibleIWordCont (  bibleiword_seq int,  bibleiword_subseq int,  bibleiword_bookseq int,  bibleiword_chapseq int,  bibleiword_verse_begin int,  bibleiword_verse_end int ) ",
            "select": "select * from tBibleIWordCont",
            "insert": 'insert into tBibleIWordCont ( bibleiword_seq ,  bibleiword_subseq ,  bibleiword_bookseq ,  bibleiword_chapseq ,  bibleiword_verse_begin ,  bibleiword_verse_end  )  values'\
            '( {bibleiword_seq} , {bibleiword_subseq} , {bibleiword_bookseq} ,{bibleiword_chapseq} ,{bibleiword_verse_begin} ,  {bibleiword_verse_end})'
            ,"isInsert" : True
            }
        , "tbibleIWordAdv": {
            "create": "CREATE TABLE tBibleIWordAdv (  iw_cateid int,  iw_catenm text,  iw_catedesc_desc text )",
            "select": "select * from tBibleIWordAdv",
            "insert": 'insert into tBibleIWordAdv (iw_cateid ,  iw_catenm ,  iw_catedesc_desc  ) values( {iw_cateid} , "{iw_catenm}", "{iw_catedesc_desc}" )'
            , "isInsert": True
        }
        , "tbibleIWordContAdv": {
            "create": "CREATE TABLE tBibleIWordContAdv (  iw_cateid int,  iw_seq int,  iw_subseq int,  iw_content text , iw_bookseq int,  iw_chapseq int, iw_verse_begin int , iw_verse_end int ) ",
            "select": "select * from tBibleIWordContAdv",
            "insert": 'insert into tBibleIWordContAdv ( iw_cateid ,  iw_seq ,  iw_subseq ,  iw_content ,  iw_bookseq ,  iw_chapseq , iw_verse_begin , iw_verse_end  )  values' \
                      '( {iw_cateid} ,  {iw_seq} ,  {iw_subseq} ,  "{iw_content}" ,  {iw_bookseq} ,  {iw_chapseq} , {iw_verse_begin} , {iw_verse_end} )'
            , "isInsert": True
        }
        , "tWordForPraise": {
            "create" : 'CREATE TABLE tWordForPray ( seq int, name text, word text, category1 text, category2 text)',
            "select": "select * from tWordForPray",
            "insert": 'insert into tWordForPray ( seq, name , word , category1 , category2 ) values ( {seq}  , "{name}" , "{word}" , "{category1}" , "{category2}")'
            , "isInsert": True
        }
        , "tAppLog": {
            "create": 'CREATE TABLE tAppLog ( log_seq integer primary key AUTOINCREMENT , cdate text , log_lvl int , log text )',
            "isInsert": False
        },
        "tBibleIWordContAdv2": {
            "create": "CREATE TABLE tBibleIWordContAdv2 ( iw_cateid int, iw_seq int, iw_subseq int, iw_subsubseq int, iw_content text, iw_bookseq int, iw_chapseq int, iw_verse_begin int, iw_verse_end int, book_contentk text, book_contente text )",
            "select": "select * from tBibleIWordContAdv2",
            "insert": 'insert into tBibleIWordContAdv2 ( iw_cateid , iw_seq , iw_subseq , iw_subsubseq , iw_content , iw_bookseq , iw_chapseq , iw_verse_begin , iw_verse_end , book_contentk , book_contente  ) Values ( {iw_cateid} , {iw_seq} , {iw_subseq} , {iw_subsubseq} , "{iw_content}" , {iw_bookseq} , {iw_chapseq} , {iw_verse_begin} , {iw_verse_end} , "{book_contentk}" , "{book_contente}"  )'
            , "isInsert": True
        }

    }
    # idx, sdate, url, title, biblecontent, youtubeurl, content, succeed
        # loop for query lists
    for query in dictCreateQueries.keys():
        # perform .. create table
        print("query {}={}".format(query, dictCreateQueries[query]['create']))
        cursor.execute(dictCreateQueries[query]['create'])
        if( dictCreateQueries[query]['isInsert'] == True ) :
            # pull data from mysql server
            ret = db.selectQueryWithRet( dictCreateQueries[query]['select'] )
            for elem in ret['data'] :
                for elem_field in elem.keys() :
                    # handle tsermon
                    if( elem_field == 'url') :
                        #https://stackoverflow.com/questions/3556266/how-can-i-get-the-final-redirect-url-when-using-urllib2-urlopen/3556287
                        elem['url'] = urllib.urlopen( elem['url'] ).geturl()

                    if( (query ==  "tsermon") and (elem_field == "youtubeURL") ) :
                        data = elem['youtubeURL']
                        if( data != None ) :
                            print( data.split("/")[4].split("?")[0])
                            elem[elem_field] = data.split("/")[4].split("?")[0]
                    # handle string field
                    if( type( elem[elem_field] ) == str ) :
                        elem[elem_field] = elem[elem_field].replace('"', '""')

                if( query == "tWordForPraise" ) : print( dictCreateQueries[query]['insert'].format(**elem) )
                cursor.execute( dictCreateQueries[query]['insert'].format(**elem) )
    con_bible.commit()

with con_cont:
    cursor = con_cont.cursor()
    # idx, sdate, url, title, biblecontent, youtubeurl, content, succeed
    dictCreateQueries = {
        "tsermon": {
            "create" : "CREATE TABLE tUccSermon ( idx int , sdate text, url text, title text, biblecontent text, youtubeurl text , content text, succeed int )",
            "select" : "select * from tUccSermon",
            "insert" : 'insert into tUccSermon ( idx , sdate , url, title , biblecontent , youtubeurl , content, succeed ) Values ( {idx} , "{sDate}" , "{url}", "{title}" , "{biblecontent}" , "{youtubeURL}" , "{content}", {succeed} )'
            , "isInsert": True
        },
        "tUccSermonRecommend": {
            "create": "CREATE TABLE tUccSermonRecommend ( idx int , sdate text, url text, title text, biblecontent text, youtubeurl text , content text, succeed int )",
            "select": "select * from tUccSermonRecommend",
            "insert": 'insert into tUccSermonRecommend ( idx , sdate , url, title , biblecontent , youtubeurl , content, succeed ) Values ( {idx} , "{sDate}" , "{url}", "{title}" , "{biblecontent}" , "{youtubeURL}" , "{content}", {succeed} )'
            , "isInsert": True
        },
        "tUccSermonCTS": {
            "create": "CREATE TABLE tUccSermonCTS ( idx int , sdate text, url text, title text, biblecontent text, youtubeurl text , content text, succeed int )",
            "select": "select * from tUccSermonCTS",
            "insert": 'insert into tUccSermonCTS ( idx , sdate , url, title , biblecontent , youtubeurl , content, succeed ) Values ( {idx} , "{sDate}" , "{url}", "{title}" , "{biblecontent}" , "{youtubeURL}" , "{content}", {succeed} )'
            , "isInsert": True
        },
        "tUccSermonCTS2": {
            "create": "CREATE TABLE tUccSermonCTS2 ( idx int , sdate text, url text, title text, biblecontent text, youtubeurl text , content text, succeed int )",
            "select": "select * from tUccSermonCTS2",
            "insert": 'insert into tUccSermonCTS2 ( idx , sdate , url, title , biblecontent , youtubeurl , content, succeed ) Values ( {idx} , "{sDate}" , "{url}", "{title}" , "{biblecontent}" , "{youtubeURL}" , "{content}", {succeed} )'
            , "isInsert": True
        },
        "tUccSermonCTS3": {
            "create": "CREATE TABLE tUccSermonCTS3 ( idx int , sdate text, url text, title text, biblecontent text, youtubeurl text , content text, succeed int )",
            "select": "select * from tUccSermonCTS3",
            "insert": 'insert into tUccSermonCTS3 ( idx , sdate , url, title , biblecontent , youtubeurl , content, succeed ) Values ( {idx} , "{sDate}" , "{url}", "{title}" , "{biblecontent}" , "{youtubeURL}" , "{content}", {succeed} )'
            , "isInsert": True
        },
        "tUccSermon_DawnJeja": {
            "create": "CREATE TABLE tUccSermon_DawnJeja ( idx int , sdate text, url text, title text, biblecontent text, youtubeurl text , content text, succeed int, type text, txt text )",
            "select": "select * from tUccSermon_DawnJeja",
            "insert": 'insert into tUccSermon_DawnJeja ( idx , sdate , url, title , biblecontent , youtubeurl , content, succeed , type , txt ) Values ( {idx} , "{sDate}" , "{url}", "{title}" , "{biblecontent}" , "{youtubeURL}" , "{content}", {succeed}, "{type}" , "txt" )'
            , "isInsert": True
        },
        #INSERT INTO tUccShineContent(sDate, url, title, type, youtubeURL, succeed) VALUES('{sDate}', '{url}', '{title}', {type},'{youtubeURL}', '{succeed}')
        "tUccShineContent": {
            "create": "CREATE TABLE tUccShineContent ( idx int , sDate text , url text , title text , type int , youtubeURL text , succeed int )",
            "select": "select * from tUccShineContent",
            "insert": 'insert into tUccShineContent ( idx , sDate, url, title, type, youtubeURL, succeed ) Values ( {idx} , "{sDate}" , "{url}", "{title}", {type}, "{youtubeURL}", {succeed} )'
            , "isInsert": True
        },




    }
        # loop for query lists
    for query in dictCreateQueries.keys():
        # perform .. create table
        print("query {}={}".format(query, dictCreateQueries[query]['create']))
        cursor.execute(dictCreateQueries[query]['create'])
        if( dictCreateQueries[query]['isInsert'] == True ) :
            # pull data from mysql server
            ret = db.selectQueryWithRet( dictCreateQueries[query]['select'] )
            for elem in ret['data'] :
                for elem_field in elem.keys() :
                    # handle tsermon
                    if( (query ==  "tsermon") and (elem_field == "youtubeURL") ) :
                        data = elem['youtubeURL']
                        if( data != None ) :
                            print( data.split("/")[4].split("?")[0])
                            elem[elem_field] = data.split("/")[4].split("?")[0]
                    # handle string field
                    if( type( elem[elem_field] ) == str ) :
                        elem[elem_field] = elem[elem_field].replace('"', '""')

                if( query == "tWordForPraise" ) : print( dictCreateQueries[query]['insert'].format(**elem) )
                cursor.execute( dictCreateQueries[query]['insert'].format(**elem) )
    con_cont.commit()

exit(0)

