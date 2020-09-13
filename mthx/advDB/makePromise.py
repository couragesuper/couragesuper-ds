import sys

sys.path.append("../../Common")
from Mysql.libmysql import dbConMysql

config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'mthx_app',
             'raise_on_warnings': True}

db = dbConMysql(config_db)

listContent=[ "사 60:1",
"단 12:3",
"사 54:2-3",
"말 4:6",
"살전 5:16-18",
"롬 8:1-2,21",
"시 57:8-9",
"엡 5:8-9",
"벧전 4:8",
"엡 3:2",
"렘 31:3-4",
"창 26:4" ]

qry_insert = "insert into tBibleIWordContAdv ( iw_cateid , iw_seq , iw_subseq , iw_content , iw_bookseq , iw_chapseq , iw_verse_begin , iw_verse_end ) "\
    "values ( {iw_cateid} , {iw_seq} , {iw_subseq} , '{iw_content}' , {iw_bookseq} , {iw_chapseq} , {iw_verse_begin} , {iw_verse_end} ) "

dicData = {}
dicDataRev = {}

if True :
    query = "select * from tBibleBook"
    ret = db.selectQueryWithRet(query)
    if( ret['ret'] == False ) : print("False")
    for row in ret['data'] :
        dicData[row['biblebook_seq']] = row['biblebook_krsumnm']
        dicDataRev[row['biblebook_krsumnm']] = row['biblebook_seq']
    print( dicData )

idx = 1
for row in listContent :
    dicInsData = { "iw_cateid" : 6 , "iw_seq" : idx , "iw_subseq" : 1 , 'iw_content' : row , 'iw_bookseq' : 0 , 'iw_chapseq' : 0 , 'iw_verse_begin' : 0 , 'iw_verse_end' : 0 }
    arr_sep = row.split("/")
    for sep in arr_sep :
        tok_booknm = sep.split(" ")[0]
        tok_chapnum = 0
        tok_versestart = 0
        tok_verseend = 0
        arr_comma = sep.split(" ")[1].split(",")
        sub_seq = 1
        for comma in arr_comma :

            if( ":" in comma ) : # not share chap
                arr_colon = comma.split(":")
                tok_chapnum = arr_colon[0]
                if( "-" in arr_colon[1] ) :
                    arr_minus = arr_colon[1].split("-")
                    tok_versestart = arr_minus[0]
                    tok_verseend = arr_minus[1]
                else :
                    tok_versestart = arr_colon[1]
                    tok_verseend = arr_colon[1]
            else :
                if( tok_chapnum == 0 ) : print("error")
                else:
                    if ("-" in comma):
                        arr_minus = comma.split("-")
                        tok_versestart = arr_minus[0]
                        tok_verseend = arr_minus[1]
                    else:
                        tok_versestart = comma
                        tok_verseend = comma
            sub_seq = sub_seq + 1

            print( "cont : {cont} , booknm : {tok_booknm} , seq : {seq} , tok_chapnum: {tok_chapnum} , tok_versestart:{tok_versestart}, tok_verseend:{tok_verseend} ".
                   format(cont = row ,
                          tok_booknm= tok_booknm ,
                          seq = dicDataRev[tok_booknm],
                          tok_chapnum = tok_chapnum ,
                          tok_versestart = tok_versestart ,
                          tok_verseend = tok_verseend) )
            dicInsData['iw_bookseq'] = dicDataRev[tok_booknm]
            dicInsData['iw_chapseq'] = tok_chapnum
            dicInsData['iw_verse_begin'] = tok_versestart
            dicInsData['iw_verse_end'] = tok_verseend
            act_query = qry_insert.format(**dicInsData)
            print( act_query )
            db.commitQuery( act_query )
        idx = idx + 1
