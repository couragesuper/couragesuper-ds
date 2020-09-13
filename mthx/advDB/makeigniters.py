import sys

sys.path.append("../../Common")
from Mysql.libmysql import dbConMysql

config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'mthx_app',
             'raise_on_warnings': True}

db = dbConMysql(config_db)

listContent=[ "마 4:1-11",
"마 5:14-16",
"삼상 17:29-30",
"행 26:13-18",
"사 60:1",
"창 4:15-17",
"갈 6:14",
"고후 4:6",
"엡 1:3-14",
"삼하 6:21-22",
"살전 5:12-22",
"민 14:7-9",
"창 1:3",
"시 57:7-11",
"시 63:3-7",
"아 2:10-13",
"아 6:3",
"아 6:10",
"갈 2:20",
"시 23:1-6",
"창 45:5-8",
"단 12:3",
"호 6:3",
"미 6:2-8",
"미 7:8",
"갈 3:2",
"신 6:4-7",
"엡 5:8-14",
"고전 13:13",
"창 15:5-6",
"창 18:14-15",
"창 21:5-7",
"창 22:7-8",
"사 40:31",
"사 54:2-3",
"사 54:11-14",
"사 57:19-21",
"사 58:13-14",
"사 61:1-3",
"눅 10:1-11",
"눅 11:5-13",
"눅 11:34-36",
"눅 18:16-17",
"마 6:1-15",
"요 1:1-15",
"요 2:24-25",
"요 3:5-6",
"요 3:19-21",
"요 7:38-39",
"요 11:40",
"요 12:35-36",
"요 12:46",
"요 13:34-35",
"요 14:15",
"요 14:27",
"요 17:16-17",
"요 17:22",
"행 2:1-4",
"행 2:33",
"행 2:43-47",
"행 3:15-16",
"행 6:3-4",
"행 4:8-12",
"행 14:3",
"행 14:22",
"행 18:9-10",
"행 20:23-24",
"롬 4:7-8",
"롬 5:1",
"롬 9:3",
"롬 10:9-11",
"롬 14:17",
"고전 2:1-5",
"고전 2:10",
"요일 2:9-10",
"요일 1:5",
"요일 5:10",
"요일 5:14",
"계 21:23-24",
"수 6:16",
"살전 5:5-6",
"롬 8:1-2",
"막 11:22-25" ]

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
    dicInsData = { "iw_cateid" : 5 , "iw_seq" : idx , "iw_subseq" : 1 , 'iw_content' : row , 'iw_bookseq' : 0 , 'iw_chapseq' : 0 , 'iw_verse_begin' : 0 , 'iw_verse_end' : 0 }
    tok_booknm = row.split(" ")[0]
    tok_chapnum = row.split(" ")[1].split(":")[0]
    tok_versestart = row.split(" ")[1].split(":")[1].split("-")[0]
    if( "-" in row.split(" ")[1].split(":")[1] ) :
        tok_verseend = row.split(" ")[1].split(":")[1].split("-")[1]
    else :
        tok_verseend = tok_versestart
    print( "cont : {cont} , booknm : {tok_booknm} , seq : {seq} , tok_chapnum: {tok_chapnum} , tok_versestart:{tok_versestart}, tok_verseend:{tok_verseend} ".
           format(cont = row ,
                  tok_booknm= tok_booknm ,
                  seq = dicDataRev[tok_booknm],
                  tok_chapnum = tok_chapnum ,
                  tok_versestart = tok_versestart ,
                  tok_verseend = tok_verseend) )
    idx = idx + 1
    dicInsData['iw_bookseq'] = dicDataRev[tok_booknm]
    dicInsData['iw_chapseq'] = tok_chapnum
    dicInsData['iw_verse_begin'] = tok_versestart
    dicInsData['iw_verse_end'] = tok_verseend
    act_query = qry_insert.format(**dicInsData)
    db.commitQuery( act_query )

