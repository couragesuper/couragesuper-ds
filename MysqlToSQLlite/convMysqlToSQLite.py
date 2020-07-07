import sys

sys.path.append("../Common")
from Mysql.libmysql import dbConMysql
import sqlite3

isCreate = False

# convertor mysql to sqlite
# 20200707 :
# bible
# qt
# poem
# sermon
# iword


# mysql -> sqlite3 database
if (isCreate):
    print("sqlite3.version:{}".format(sqlite3.version))
    print("sqlite3.sqlite_version:{}".format(sqlite3.sqlite_version))

    config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
                 'raise_on_warnings': True}
    db = dbConMysql(config_db)

    con = sqlite3.connect("mthx_2nd.db")
    with con:
        cursor = con.cursor()
        dictCreateQueries = {
            "tbible": {"create": "CREATE TABLE tBible( bibleSeq int, bibleType text,bibleDesc text )",
                       "select": "select * from tBible",
                       "insert": 'INSERT INTO tBible VALUES( {bibleSeq} ,"{bibleType}" ,"{bibleDesc}")'}
            , "tbibleBook": {
                "create": "CREATE TABLE tBibleBook (biblebook_seq int, biblebook_type text, biblebook_krnm text, biblebook_engnm text, biblebook_krsumnm text)",
                "select": "select * from tBibleBook",
                "insert": 'INSERT INTO tBibleBook VALUES( {biblebook_seq} , "{biblebook_type}" ,"{biblebook_krnm}" ,"{biblebook_engnm}", "{biblebook_krsumnm}")'}
            , "tbibleCont": {
                "create": "CREATE TABLE tBibleCont ( bible_seq int, book_seq int, book_chap int, book_verse int, book_content text)",
                "select": "select * from tBibleCont",
                "insert": 'INSERT INTO tBibleCont VALUES( {bible_seq} , {book_seq} , {book_chap}, {book_verse} ,"{book_content}")'}
            , "tbibleqt": {
                "create": "CREATE TABLE tBibleQtCont(  bibleqt_seq int,  bibleqt_type int,  bibleqt_day int,  bibleqt_mon int,  bibltqt_content text, bibleqt_data text)",
                "select": "select * from tBibleQtCont",
                "insert": 'INSERT INTO tBibleQtCont VALUES ( {bibleqt_seq}, {bibleqt_type}, {bibleqt_day}, {bibleqt_mon}, "{bibltqt_content}" , "{bibleqt_data}" )'}
            , "tbibleIWord": {
                "create": "CREATE TABLE tBibleIWord (  bibleiword_seq int,  bibleiword_nm text,  bibleiword_desc text )",
                "select": "select * from tBibleIWord",
                "insert": 'insert into tBibleIWord (bibleiword_seq ,  bibleiword_nm ,  bibleiword_desc  ) values( {bibleiword_seq} , "{bibleiword_nm}", "{bibleiword_desc}" )'
                }
            , "tbibleIWordCont": {
                "create": "CREATE TABLE tBibleIWordCont (  bibleiword_seq int,  bibleiword_subseq int,  bibleiword_bookseq int,  bibleiword_chapseq int,  bibleiword_verse_begin int,  bibleiword_verse_end int ) ",
                "select": "select * from tBibleIWordCont",
                "insert": 'insert into tBibleIWordCont ( bibleiword_seq ,  bibleiword_subseq ,  bibleiword_bookseq ,  bibleiword_chapseq ,  bibleiword_verse_begin ,  bibleiword_verse_end  )  values'\
                '( {bibleiword_seq} , {bibleiword_subseq} , {bibleiword_bookseq} ,{bibleiword_chapseq} ,{bibleiword_verse_begin} ,  {bibleiword_verse_end})'
                }
            , "tsermon": {
                "create" : "CREATE TABLE tUccSermon ( idx int , sdate text, url text, title text, biblecontent text, youtubeurl text , content text, succeed int )",
                "select" : "select * from tUccSermon",
                "insert" : 'insert into tUccSermon ( idx , sdate , url, title , biblecontent , youtubeurl , content, succeed ) Values ( {idx} , "{sDate}" , "{url}", "{title}" , "{biblecontent}" , "{youtubeURL}" , "{content}", {succeed} )'
                }
        }

        # idx, sdate, url, title, biblecontent, youtubeurl, content, succeed

        for query in dictCreateQueries.keys():
            print("query {}={}".format(query, dictCreateQueries[query]['create']))
            cursor.execute(dictCreateQueries[query]['create'])
            ret = db.selectQueryWithRet( dictCreateQueries[query]['select'] )
            for elem in ret['data'] :
                for elem_field in elem.keys() :
                    if( (query ==  "tsermon") and (elem_field == "youtubeURL") ) :
                        data = elem['youtubeURL']
                        if( data != None ) :
                            print( data.split("/")[4].split("?")[0])
                            elem[elem_field] = data.split("/")[4].split("?")[0]
                    if( type( elem[elem_field] ) == str ) :
                        elem[elem_field] = elem[elem_field].replace('"', '""')
                cursor.execute( dictCreateQueries[query]['insert'].format(**elem) )
        con.commit()
        exit(0)

# check sqlite3 database
if (isCreate == False):
    con = sqlite3.connect("mthx_2nd.db")
    with con:
        # primary select query test
        if False:
            query = "select * from tBible"
            cursor = con.cursor().execute(query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            query = "select * from tBibleBook"
            cursor = con.cursor().execute(query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            query = "select * from tBibleCont"
            cursor = con.cursor().execute(query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)

        # query for biblebook list test
        if True:
            if False :
                query = "select book_seq, max(book_chap) as cntChap from tBibleCont where book_seq = {}".format(1)
                cursor = con.cursor().execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                query = "select * from tBibleQtCont where bibleqt_seq = {}".format(2)
                cursor = con.cursor().execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                query = "select * from tBibleIWord"
                cursor = con.cursor().execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                query = "select * from tBibleIWordCont"
                cursor = con.cursor().execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
            else:
                #query = "select * from tUccSermon where sdate like '%2012%' "
                query = "select * from tUccSermon order by idx desc"
                cursor = con.cursor().execute(query)
                rows = cursor.fetchall()
                print("size{}".format( len(rows) ))
                for row in rows:
                    print(row)











