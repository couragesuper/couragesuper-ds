import pandas as pd
# import mysql library
import sys
import json
sys.path.append("../Common")
from Mysql.libmysql import dbConMysql


# Python Tips
    # pandas
    # (i.j) access of datafraem
    # df.iloc[ loop , mapIdxCol['offset']

    # pandas
    # mapIdxCol = {column: int(list( df_data ).index(column)) for column in df_data.columns}

#1.open excel
excel_name = "CreateTable.xlsx"
sheet_name = "poem"

#2.read excel
df_data = pd.read_excel( excel_name , sheet_name = sheet_name )  #대소문자 구분된다.

#3.make column dict for pandas
mapIdxCol = {column: int(list( df_data ).index(column)) for column in df_data.columns}
fieldPK = ""

#4.fieldName :
#    map { isNull , datatype , comment }
mapDbSchema = {}
print( df_data )

#5.first line
    # iterative columns
for field in df_data.columns :
    #print( df_data.iloc[ 0 , mapIdxCol[field] ] )
    col_id = mapIdxCol[field]

    if( field not in mapDbSchema ) : mapDbSchema[field] = {}
    mapDbSchema[field]['datatype'] = df_data.iloc[1, col_id ]
    mapDbSchema[field]['isnull'] = df_data.iloc[2, col_id ]

    if (df_data.iloc[0, col_id] == "PK"):
        print("PK is this field :" + field)
        mapDbSchema[field]['ispk'] = True
        fieldPK = field
    else :
        mapDbSchema[field]['ispk'] = False

#6.show map schema
print ( mapDbSchema )

#7.check whether pk is exist
if( fieldPK == "" ) :
    print("PK isn't exist")
    exit(0)

#8.mysql connect with common library
#config_bot = {'user': 'root',          'password': 'karisma*3%7*4',          'host': 'mthx.cafe24.com',          'database': 'chatbot',          'raise_on_warnings': True }
#db      = dbConMysql(config_bot)
#qry     = "select * from tUserChatStatJson where userkey='U9A9agpChomm'; "
#listRet = db.selectQuery( qry )
#jsonStr = listRet[0]['jsondata']
#ret     = json.loads(jsonStr)
#print( ret )

config_db = {'user': 'root',          'password': 'karisma*3%7*4',          'host': 'mthx.cafe24.com',          'database': 'freedata',          'raise_on_warnings': True }
db      = dbConMysql(config_db)

create_query_state = "CREATE TABLE `{table_name}` ( \n".format( table_name = sheet_name , )
for key,val in mapDbSchema.items() :
    print( val )
    null_str = "NOT NULL"
    if( val['isnull'] == False ) : null_str = "NULL"
    query_elem_row = "`{field_name}` {data_type} {isnull} ".format(field_name=key , data_type=val['datatype'] , isnull = null_str)
    if( key == fieldPK ) : query_elem_row += " AUTO_INCREMENT,\n"
    else : query_elem_row += ",\n"
    create_query_state += query_elem_row

create_query_state += "PRIMARY KEY (`{fieldPK}`)\n ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;".format(fieldPK=fieldPK )

db.commitQuery( "drop table poem;")
db.commitQuery( create_query_state )
print( create_query_state )

loop = 3
lenIndex = len(df_data.index)
while (True):
    if (loop == lenIndex):
        break
    poem_id = df_data.iloc[loop , mapIdxCol['poem_id']]
    poem_title =  df_data.iloc[loop , mapIdxCol['poem_title']]
    poem_content = df_data.iloc[loop, mapIdxCol['poem_content']]
    insert_query = "INSERT \n INTO\n freedata.poem(\n poem_id\n, poem_title\n , poem_content\n, poem_createdate\n, poem_registdate\n, poem_updatedate\n, poem_revision\n) VALUES ( \n"
    insert_query += " {poem_id} , \"{poem_title}\" , \"{poem_content}\" , CURRENT_TIME() , CURRENT_TIME() , CURRENT_TIME() , 100 );".format(poem_id = poem_id , poem_title=poem_title , poem_content=poem_content)
    #print( insert_query )
    db.commitQuery(insert_query)
    loop = loop + 1

# 시가 입력이 잘 되었는지를 체크 , 개행까지 잘 저장된 것을 확인
if( False ) :
    listRet = db.selectQuery( "select poem_id, poem_content from poem" )
    for elem in listRet :
        print( elem['poem_content'])














