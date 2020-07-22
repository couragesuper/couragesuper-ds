# convertor
    # converting excel for(word for praise) to db (mytable)

import sys
import pandas as pd

# import common library
sys.path.append("../../Common")
from Mysql.libmysql import dbConMysql
from Util.Util import stopWatch


# initalize stopwatch and database manager
sw = stopWatch()
config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible','raise_on_warnings': True}
db = dbConMysql(config_db)

#1. open excel with pandas
df_data = pd.read_excel("WordForPray.xlsx" )

#2. count of rows
cntRow = len( df_data.index )
print( "data to input:{}".format( cntRow ) )

#3. indexer map for columds
mapIdxCol = {column: int(list(df_data).index(column)) for column in df_data.columns}
print( "all index of column {}".format( mapIdxCol ))

#4. routine for cleaning data about name field
if False :
    setName = list( df_data['name'].unique() )
    print( len( setName ) )
    print( type( setName) )
    #print( len( setName) ) : 149

    setName.sort()
    print(  setName  )

    exit(0)

mapDebugOn = {
    "row" : True,
    "query" : False,
    "typecheck" : False,
    "actQuery" : True
}

# preprocessing for nan data
df_data['category1'] = "기도1"
df_data['category2'] = "기도2"

#5. input datas to mysql database
for idx in range( 0, cntRow ) :
    #print( "{}={}".format( idx, df.iloc[idx]) )
    mapData = {}
    mapData["seq"] = df_data.iloc[idx ,mapIdxCol['idx']]
    mapData["name"] = df_data.iloc[idx ,mapIdxCol['name']]
    mapData["word"] = df_data.iloc[idx ,mapIdxCol['word']]

    mapData["category1"] = df_data.iloc[idx, mapIdxCol['category1']]
    mapData["category2"] = df_data.iloc[idx, mapIdxCol['category2']]

    if( mapDebugOn['row'] ) : print( "insert data {} .  data = {}".format( mapData["seq"] , mapData ))
    # handle "
    for key in mapData.keys() :
        if( type( mapData[key] ) == 'str' ) :
            mapData[key] = mapData[key].replace( '"' ,'""' )
        else  :
            if( mapDebugOn['typecheck'] ) : print( type( mapData[key] ) )

    query = 'INSERT INTO tWordForPray ( name , word , category1 , category2 ) VALUES ( "{name}" , "{word}." , "{category1}" ,"{category2}" )'.format( **mapData )
    if(mapDebugOn['query']): print("query : {}".format(query))
    if(mapDebugOn[ "actQuery"]) :db.commitQuery ( query )
