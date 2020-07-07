import sys
sys.path.append("../Common")
from Mysql.libmysql import dbConMysql
import sqlite3

isCreate = True

#mysql -> sqlite3 database
if( isCreate ) :
    print("sqlite3.version:{}".format(sqlite3.version))
    print("sqlite3.sqlite_version:{}".format(sqlite3.sqlite_version))
    config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
                 'raise_on_warnings': True}
    db = dbConMysql(config_db)
    con = sqlite3.connect("local.db")

    with con :
        cursor = con.cursor()
        query = "CREATE TABLE if not exists userlog ( a int , b int , c text );"
        cursor.execute( query )

        if( False ) :
            query = "drop table if exists push_log"
            cursor.execute(query)
        query = "create table if not exists push_log ( seq integer primary key autoincrement, title text, body text,  pushOftime TEXT not null default (datetime('now','localtime')) )"
        cursor.execute(query)

        if ( False ) :
            query = "insert into userlog values (1,2,\"33\")"
            cursor.execute( query )

            query = "insert into userlog values (1,2,\"33\")"
            cursor.execute( query )
            print( "select db" )
            query = "select * from userlog;"
            rows = con.cursor().execute(query).fetchall()
            for row in rows:
                print(row)

        if ( True ):
            query = "insert into push_log( title, body, pushOftime ) values ( 'title' ,'body' , datetime('now','localtime') ) "
            cursor.execute(query)
            query = "select * from push_log;"
            rows = con.cursor().execute(query).fetchall()
            for row in rows:
                print(row)
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














