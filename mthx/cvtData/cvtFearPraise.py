import sys
import json
import re
import sys

# fear excel -> json

sys.path.append("../../Common")
from Mysql.libmysql import dbConMysql
import pandas as pd

# open db
def openDB() :
    config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
                 'raise_on_warnings': True}
    return dbConMysql(config_db)

db = openDB()
db2 = openDB()

# get bibleQuery
ret = db.selectQuery("select biblebook_seq as seq , biblebook_krnm as name , biblebook_krsumnm as sumnm from tBibleBook")
print( ret )


mapBibleSumnmToIdx = {}
for elem in ret :
    mapBibleSumnmToIdx[ elem['sumnm']] = elem['seq']
print( mapBibleSumnmToIdx )



df_data = pd.read_excel("..\data\CreateTable.xlsx", sheet_name="fear")
print ( df_data )
mapIdxCol = {column: int(list(df_data).index(column)) for column in df_data.columns}

def parseSearchEx( msg ) :
    #print("msg:{}".format(msg))
    pats = [{"pat": "([가-힣]*)([0-9]*)(-)([0-9]*)", "type": 5},
            {"pat": "([가-힣]*)([0-9]*):([0-9]*)-([0-9]*):([0-9]*)", "type": 1},
            {"pat": "([가-힣]*)([0-9]*):([0-9]*)-([0-9]*)", "type": 2},
            {"pat": "([가-힣]*)([0-9]*):([0-9]*)", "type": 3},
            {"pat": "([가-힣]*)([0-9]*)" , "type":4 }]
    for pat in pats :
        parser = re.compile( pat['pat'] )
        m = parser.match(msg)
        if( m != None ) :
            query = 'select biblebook_seq from tBibleBook where biblebook_krsumnm = "{}"'.format(m.groups()[0])
            ret = db2.selectQueryWithRet(query)
            bookseq = ret['data'][0]['biblebook_seq']
            if( pat['type'] == 1 ):
                return { "type":1 , "bookseq":bookseq, "bible_sunnm" : m.groups()[0] , "chap_start" : m.groups()[1] ,  "verse_start" : m.groups()[2] , "chap_end" : m.groups()[3] ,  "verse_end" : m.groups()[4]  }
            elif (pat['type'] == 2):
                return { "type":2 , "bookseq":bookseq, "bible_sunnm": m.groups()[0], "chap_start": m.groups()[1], "verse_start": m.groups()[2],"verse_end": m.groups()[3] , "chap_end" : 0 }
            elif (pat['type'] == 3):
                return { "type":3 , "bookseq":bookseq, "bible_sunnm": m.groups()[0], "chap_start": m.groups()[1], "verse_start": m.groups()[2] ,"chap_end" : 0 , "verse_end":0 }
            elif (pat['type'] == 4):
                return { "type":4 , "bookseq":bookseq, "bible_sunnm": m.groups()[0], "chap_start": m.groups()[1] , "verse_start":0 , "chap_end":0 , "verse_end":}
            elif (pat['type'] == 5):
                return {"type": 5, "bookseq": bookseq, "bible_sunnm": m.groups()[0], "chap_start": m.groups()[1], "chap_end": m.groups()[3] }
            else :
                return None
                #print("msg ={} is mismatched".format(msg))

loop = 0
lenIdx = len( df_data.index )
setType = set()

while( True ) :
    if ( lenIdx == loop ) : break;
    if ( loop > 3 ) :
        content = df_data.iloc[loop, mapIdxCol['content']]
        ret = parseSearchEx( content.replace(" " ,""))
        json_data_all = json.dumps( ret , ensure_ascii=False)
        print( ret )
    loop = loop + 1

print( setType )
























