#import mysql library
import sys
import json
sys.path.append("../Common")
from Mysql.libmysql import dbConMysql

config_db = {'user': 'root',          'password': 'karisma*3%7*4',          'host': 'mthx.cafe24.com',          'database': 'bible',          'raise_on_warnings': True }
db      = dbConMysql(config_db)

# 성경목록 얻기

#1. select query is retrives with list consist of dict
query_biblelist  = "select * from tBible"
listRet = db.selectQuery( query_biblelist )
print( len(listRet) )
print( listRet[0] )
print( listRet[0].keys() )

#2. list of old statement
query_newstat_list = "select biblebook_seq, biblebook_krnm , biblebook_krsumnm from tBibleBook where biblebook_type = 'O';"
listRet = db.selectQuery( query_newstat_list )
print( len(listRet) )
print( listRet[0] )
print( listRet[0].keys() )

#3. quote and multi line string
query_countof_chapInbook = 'select ' \
 'book_seq, ' \
 '(select biblebook_krnm from tBibleBook where biblebook_seq = book_seq) as booknm, '\
 'count(*) as cnt '\
 'from tBibleCont '\
 'where bible_seq = (select bibleseq from tBible where bibleType="KN") '\
 'group by book_seq, bible_seq'

print( query_countof_chapInbook )
listRet = db.selectQuery( query_countof_chapInbook )
cntLen = len(listRet)
print( cntLen )
if( cntLen > 0 ) :
    print( listRet[0] )
    print( listRet[0].keys() )

#4. 이것을 FLASK로 전달해보려고 합니다.

