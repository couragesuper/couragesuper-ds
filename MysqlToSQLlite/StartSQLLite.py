import sys
sys.path.append("../Common")
from Mysql.libmysql import dbConMysql
import sqlite3

isCreate = False

#mysql -> sqlite3 start sample
#202007

if( isCreate ) :
    print("sqlite3.version:{}".format(sqlite3.version))
    print("sqlite3.sqlite_version:{}".format(sqlite3.sqlite_version))

    config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
                 'raise_on_warnings': True}
    db = dbConMysql(config_db)
    ret1 = db.selectQueryWithRet("select * from tBible")
    print(ret1['data'][0])
    ret2 = db.selectQueryWithRet("select * from tBibleBook")
    print(ret2['data'][0])
    ret3 = db.selectQueryWithRet("select * from tBibleCont")
    print(ret3['data'][0])
    ret4 = db.selectQueryWithRet("select * from tBibleQtCont")
    print(ret4['data'][0])
    ret5 = db.selectQueryWithRet("select * from tBibleIWord")
    print(ret5['data'][0])
    ret6 = db.selectQueryWithRet("select * from tBibleIWordCont")
    print(ret6['data'][0])

    con = sqlite3.connect("mthx.db")
    with con :
        cursor = con.cursor()
        create_query_tbible ="CREATE TABLE tBible( bibleSeq int, bibleType text,bibleDesc text )"
        create_query_tbibleBook = "CREATE TABLE tBibleBook (biblebook_seq int, biblebook_type text, biblebook_krnm text, biblebook_engnm text, biblebook_krsumnm text)"
        create_query_tbibleCont = "CREATE TABLE tBibleCont ( bible_seq int, book_seq int, book_chap int, book_verse int, book_content text)"
        create_query_tbibleqt = "CREATE TABLE tBibleQtCont(  bibleqt_seq int,  bibleqt_type int,  bibleqt_day int,  bibleqt_mon int,  bibltqt_content text, bibleqt_data text)"
        create_query_tbibleIWord = "CREATE TABLE tBibleIWord (  bibleiword_seq int,  bibleiword_nm text,  bibleiword_desc text )"
        create_query_tbibleIWordCont = "CREATE TABLE tBibleIWordCont (  bibleiword_seq int,  bibleiword_subseq int,  bibleiword_bookseq int,  bibleiword_chapseq int,  bibleiword_verse_begin int,  bibleiword_verse_end int ) "

        cursor.execute( create_query_tbible )
        cursor.execute( create_query_tbibleBook )
        cursor.execute( create_query_tbibleCont )
        cursor.execute( create_query_tbibleqt )
        cursor.execute( create_query_tbibleIWord )
        cursor.execute( create_query_tbibleIWordCont )


        #tBible
        print( "tBible" )
        for elem in ret1['data'] :
            query = 'INSERT INTO tBible VALUES( {} ,"{}" ,"{}")'.format(elem['bibleSeq'], elem['bibleType'] ,elem['bibleDesc'] )
            cursor.execute(query)
        #tBibleBook
        print("tBibleBook")
        for elem in ret2['data'] :
            query = 'INSERT INTO tBibleBook VALUES( {} , "{}" ,"{}" ,"{}", "{}")'.format(elem['biblebook_seq'] , elem['biblebook_type'] , elem['biblebook_krnm'] , elem['biblebook_engnm'] , elem['biblebook_krsumnm']  )
            cursor.execute(query)
        #tBileCont
        print("tBibleCont")
        for elem in ret3['data'] :
            query = 'INSERT INTO tBibleCont VALUES( %d , %d , %d, %d ,"%s")'%( elem['bible_seq'], elem['book_seq'] ,elem['book_chap'] , elem['book_verse'] , elem['book_content'].replace('"' , '""'))
            #print(query)
            cursor.execute(query)
        # tBileCont
        print("tBibleQT")
        for elem in ret4['data']:
            query = 'INSERT INTO tBibleQtCont VALUES ( %d, %d, %d, %d, "%s" , "%s" )' % (  elem['bibleqt_seq'],  elem['bibleqt_type'], elem['bibleqt_day'],  elem['bibleqt_mon'], elem['bibltqt_content'].replace('"', '""') , elem['bibleqt_data'].replace('"','""'))
            print(query)
            cursor.execute(query)
            print("tBibleQT")
        for elem in ret5['data']:
            query = 'insert into tBibleIWord (bibleiword_seq ,  bibleiword_nm ,  bibleiword_desc  ) values( {} , \"{}\", \"{}\" )'.format( elem['bibleiword_seq'] , elem['bibleiword_nm'].replace('"', '""') , elem['bibleiword_desc'].replace('"', '""'))
            print(query)
            cursor.execute(query)
        print("tBibleQT")
        for elem in ret6['data']:
            query = 'insert into tBibleIWordCont ( bibleiword_seq ,  bibleiword_subseq ,  bibleiword_bookseq ,  bibleiword_chapseq ,  bibleiword_verse_begin ,  bibleiword_verse_end  )  values( {} , {} , {} ,{} ,{} ,  {})'.format(
                elem['bibleiword_seq'], elem['bibleiword_subseq'], elem['bibleiword_bookseq'], elem['bibleiword_chapseq'], elem['bibleiword_verse_begin'],elem['bibleiword_verse_end'])
            print(query)
            cursor.execute(query)
        con.commit()


#check sqlite3 database
if( isCreate == False ) :
    con = sqlite3.connect("mthx.db")
    with con :
        #primary select query test
        if False:
            query = "select * from tBible"
            cursor = con.cursor().execute(query)
            rows = cursor.fetchall()
            for  row in rows :
                print( row )
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

        #query for biblebook list test
        if True :
            query ="select book_seq, max(book_chap) as cntChap from tBibleCont where book_seq = {}".format(1)
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














