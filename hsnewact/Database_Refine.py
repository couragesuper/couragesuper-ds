import sys

sys.path.append("../Common")
from Mysql.libmysql import dbConMysql

# init database manager
config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'hs_newacts',
             'raise_on_warnings': True}
db = dbConMysql(config_db)

# select query test
query = "select * from tHsNewActsNews";
ret = db.selectQueryWithRet( query );
print( ret )

#

