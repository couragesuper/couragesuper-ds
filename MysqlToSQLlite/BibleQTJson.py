import sys
sys.path.append("../Common")
from Mysql.libmysql import dbConMysql

import json
import re
import sys

config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
             'raise_on_warnings': True}
db = dbConMysql(config_db)
ret = db.selectQueryWithRet("select * from tBibleQtCont")

for elem in ret['data'] :
    dicData = json.loads( elem['bibleqt_data'] )
    print( dicData );
    print( dicData[0] );
    break


