import sys

sys.path.append("../../Common")
from Mysql.libmysql import dbConMysql


config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'mthx_app',
             'raise_on_warnings': True}

db = dbConMysql(config_db)

#1. fill `tBibleIWordAdv`
if True : # Done
    query = "select * from tBibleIWord"
    ins_query = "insert into tBibleIWordAdv( iw_cateid , iw_catenm , iw_catedesc_desc ) values ( {bibleiword_seq} , '{bibleiword_nm}' , '{bibleiword_desc}' )"
    ret = db.selectQueryWithRet( query )
    for row in ret['data'] :
        print( row )
        act_query = ins_query.format(**row)
        print( act_query )
        ret = db.commitQuery(act_query)

if True :


dicData = {}

if False :
    query = "select * from tBibleBook"
    ret = db.selectQueryWithRet(query)
    if( ret['ret'] == False ) : print("False")
    for row in ret['data'] :
        dicData[row['biblebook_seq']] = row['biblebook_krsumnm']
    print( dicData )

if False :
    query = "select * from tBibleIWordCont"
    ret = db.selectQueryWithRet(query)
    ins_query = "insert into tBibleIWordContAdv (iw_cateid,iw_seq,iw_subseq,iw_content,iw_bookseq,iw_chapseq,iw_verse_begin,iw_verse_end) values "\
        "({bibleiword_seq} , {bibleiword_subseq} , 1 , '{content}' , {bibleiword_bookseq} , {bibleiword_chapseq} , {bibleiword_verse_begin} , {bibleiword_verse_end}  )"
    for row in ret['data'] :
        szContent = dicData[row['bibleiword_bookseq']] + " " + str(row['bibleiword_chapseq']) + ":"
        if( row['bibleiword_verse_begin'] == row['bibleiword_verse_end']) : szContent = szContent + str(row['bibleiword_verse_begin'])
        else : szContent = szContent + str(row['bibleiword_verse_begin']) + "-" + str(row['bibleiword_verse_end'])
        row['content'] = szContent
        act_query = ins_query.format(**row)
        db.commitQuery(act_query)



