import sys
import json
sys.path.append("../Common")
from Mysql.libmysql import dbConMysql


config_bot = {
          'user': 'root',
          'password': 'karisma*3%7*4',
          'host': 'mthx.cafe24.com',
          'database': 'chatbot',
          'raise_on_warnings': True }

db      = dbConMysql(config_bot)
qry     = "select * from tUserChatStatJson where userkey='U9A9agpChomm'; "
listRet = db.selectQuery( qry )
jsonStr = listRet[0]['jsondata']
ret     = json.loads(jsonStr)

print( ret )











