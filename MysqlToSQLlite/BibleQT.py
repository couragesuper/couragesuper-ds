import sys
sys.path.append("../Common")
from Mysql.libmysql import dbConMysql

import json
import re
import sys

# generates bible qt data

config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
             'raise_on_warnings': True}
db = dbConMysql(config_db)
db2 = dbConMysql(config_db)
ret = db.selectQueryWithRet("select * from tBibleQtCont")

#pattern check
    # pat: [] / string: [창1]
    # pat: [-] / string: [창9-10]
    # pat: [:-] / string: [눅1:1-38]
    # pat: [:-:] / string: [출11:1-12:28]
    # {'', '-', ':-:', ':-'}

def parseSearch( msg ) :
    #print("msg:{}".format(msg))
    pats = ["([가-힣]*)([0-9]*):([0-9]*)(-)([0-9]*)" ,
            "([가-힣]*)([0-9]*):([0-9]*)(-)" ,
            "([가-힣]*)([0-9]*):([0-9]*)" ,
            "([가-힣]*)([0-9]*):" ,
            "([가-힣]*)([0-9]*)-([0-9]*)",
            "([가-힣]*)"]
    listDesc = ["book","chap","no_start","isDash","no_end"]
    dicRet = {}
    for pat in pats :
        parser = re.compile( pat )
        m = parser.match(msg)
        if( m != None ) :
            #print( m.groups() , type(m.groups()))
            ret_tuple = m.groups()
            if( len(ret_tuple) ) :
                dicRet['ret']='ok'
                for i in range(0,len(ret_tuple)) :
                    if( ret_tuple[i] != "" ) :
                        if( listDesc[i] in ['chap','no_start','no_end'] ) : dicRet[listDesc[i]] = int(ret_tuple[i])
                        else : dicRet[listDesc[i]] = ret_tuple[i]
    return dicRet

if( True ) :
    setPats = set([])
    for elem in ret['data'] :
        str = elem['bibltqt_content']
        arr = str.split(",")
        for elemInArr in arr :
            strPat = ""
            for ch in elemInArr :
                #print(ch)
                if( ch == ":") : strPat = strPat + ch
                if (ch == "-") : strPat = strPat + ch
            #print( strPat)
            if( strPat not in setPats ) :
                #print( "pat: [{}] / string: [{}] ".format(strPat,elemInArr) )
                setPats.add(strPat)

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
            #print("msg ={} , pat={}".format( msg, pat['type']))
            query = 'select biblebook_seq from tBibleBook where biblebook_krsumnm = "{}"'.format(m.groups()[0])
            #print( query )
            ret = db2.selectQueryWithRet(query)
            #print(ret)
            bookseq = ret['data'][0]['biblebook_seq']
            #print( "bookseq{}".format(bookseq) )
            if( pat['type'] == 1 ):
                return { "type":1 , "bookseq":bookseq, "bible_sunnm" : m.groups()[0] , "chap_start" : m.groups()[1] ,  "verse_start" : m.groups()[2] , "chap_end" : m.groups()[3] ,  "verse_end" : m.groups()[4]  }
            elif (pat['type'] == 2):
                return { "type":2 , "bookseq":bookseq, "bible_sunnm": m.groups()[0], "chap_start": m.groups()[1], "verse_start": m.groups()[2],"verse_end": m.groups()[3]}
            elif (pat['type'] == 3):
                return { "type":3 , "bookseq":bookseq, "bible_sunnm": m.groups()[0], "chap_start": m.groups()[1], "verse_start": m.groups()[2] }
            elif (pat['type'] == 4):
                return { "type":4 , "bookseq":bookseq, "bible_sunnm": m.groups()[0], "chap_start": m.groups()[1] }
            elif (pat['type'] == 5):
                return {"type": 5, "bookseq": bookseq, "bible_sunnm": m.groups()[0], "chap_start": m.groups()[1], "chap_end": m.groups()[3] }
            else :
                return None
                #print("msg ={} is mismatched".format(msg))

for elem in ret['data'] :
    #print( elem )
    str = elem['bibltqt_content']
    arr = str.split(",")
    retVal = []
    for elemInArr in arr :
        ret = parseSearchEx( elemInArr )
        #print( ret )
        #dict to json
        #json_Data =json.dumps( ret , ensure_ascii = False )
        #print( json_Data )
        retVal.append( ret )
    json_data_all = json.dumps( retVal , ensure_ascii = False )
    print( json_data_all )
    query = 'update tBibleQtCont set bibleqt_data="{json} " where bibleqt_seq = {bibleqt_seq} and bibleqt_type = {bibleqt_type} and bibleqt_day = {bibleqt_day} and bibleqt_mon = {bibleqt_mon} ;'.format(
        json = json_data_all.replace('"','""'),
        bibleqt_seq = elem['bibleqt_seq'],
        bibleqt_type = elem['bibleqt_type'],
        bibleqt_day = elem['bibleqt_day'],
        bibleqt_mon= elem['bibleqt_mon'])
    db.commitQuery( query )
print("finished")


