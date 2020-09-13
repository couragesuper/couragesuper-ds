import sys

sys.path.append("../Common")
from Mysql.libmysql import dbConMysql
import sqlite3

# convertor mysql to sqlite
# 20200707 : (mthx_2nd)
    # bible , qt , poem , sermon , iword
# 20200714 : (mthx_3nd)
    # add paragraph title to biblecont
# 20200715: (mthx_4th)
    # add word for praise

isTestBible = False
isTestWordForPray = False
isTestIWordQt = False
isTestSermon = False
isTestAppLog = True

dbName = "mthx_7th.db"
con = sqlite3.connect( dbName )
with con:
    # primary select query test
    if isTestBible :
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

    if isTestWordForPray:
        query = "select * from tWordForPray"
        cursor = con.cursor().execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    # query for biblebook list test
    if isTestIWordQt :
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
    if isTestSermon :
        #query = "select * from tUccSermon where sdate like '%2012%' "
        query = "select * from tUccSermon order by idx desc"
        cursor = con.cursor().execute(query)
        rows = cursor.fetchall()
        print("size{}".format( len(rows) ))
        for row in rows:
            print(row)
    if isTestAppLog :
        dictArg = [{ "log_lvl" : 10 , "cdate":"20200725" , "log":"dfdfdfsfdsdfsdfasdfasdf"} ,
                   { "log_lvl" : 20 , "cdate": "20200725", "log":"dfdfdfsfdsdfsdfasdfasdf"} ,
                   { "log_lvl" : 30 ,"cdate": "20200725", "log":"dfdfdfsfdsdfsdfasdfasdf"}]

        for insert in dictArg :
            #"create": 'CREATE TABLE tAppLog ( log_seq integer primary key AUTOINCREMENT , cdate text , log_lvl int , log text )',
            insert_query = 'insert into tAppLog (cdate, log_lvl , log) values ( {cdate}  , {log_lvl}  , "{log}"  )'.format( **insert )
            cursor = con.cursor().execute(insert_query)

        query = "select * from tAppLog"
        cursor = con.cursor().execute(query)
        rows = cursor.fetchall()
        print("size{}".format(len(rows)))
        for row in rows:
            print(row)










