

import sys
import time
import os

#sys.path.append("../../Common")
sys.path.append("/root/Python/couragesuper-ds/Common")
from Mysql.libmysql import dbConMysql


config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'mthx_app',
             'raise_on_warnings': True}
db = dbConMysql(config_db)

query = "insert into tLog ( message, user ,datetime ) values ( '{message}' , '{user}' , NOW() );"
msg = { "message" : "abc" , "user" : "def"}

realquery = query.format( **msg )
db.commitQuery( realquery )



