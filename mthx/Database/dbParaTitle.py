# add paragraph title to bible content db
# tBibleCont -> tBibleContV2

import sys

sys.path.append("../../Common")
from Mysql.libmysql import dbConMysql
from Util.Util import stopWatch

# tBibleCont -> tBibleContV2
sw = stopWatch()

config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible','raise_on_warnings': True}
db = dbConMysql(config_db)



step = 1
cnt = 0
def printErr( ):
    print( "error with step : {}".format( step ) )
    exit(0)

sw.reset()
ret = db.selectQueryWithRet( "select * from tBibleCont")
sw.diffWithTag( "DB Select Query")

if( ret['ret'] ) :
    data = ret['data']
    db.Lock()
    sw.reset()
    for row in data :
        try :
            #print( row )
            #{'bible_seq': 1, 'book_seq': 1, 'book_chap': 1, 'book_verse': 1,'book_content': 'In the beginning God created the heavens and the earth. '}
            row['book_content'] = row['book_content'].replace('"', '""')
            insertQry = 'insert into tBibleContV2 ( bible_seq , book_seq , book_chap , book_verse , book_content ) values ( {bible_seq}, {book_seq}, {book_chap} ,{book_verse} ,"{book_content}" )'.format( **row )
            #db.commitQuery( insertQry )
            db.LockQuery(insertQry)
        except Exception as ex:
            print(ex)
            db.unLock()

        cnt = cnt + 1
        if( (cnt != 0) and ((cnt % 100) == 0 ) ) :
            #print( "in progressing step : {}".format( cnt ) )
            sw.diffWithTag("insert cnt:{}".format(cnt))
            db.unLock()
            db.Lock()
    db.unLock()
else :
    printErr()




