# conda install -c anaconda flask

from flask import Flask
from flask import Response
from flask import request
from flask_restful import Resource
from flask_restful import Api
# from flaskext.mysql import MySQL
from functools import wraps
import json
import re
import sys

sys.path.append("../Common")
from Mysql.libmysql import dbConMysql

#helper
def dictToJson(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')
    return decorated_function

def func_query(  api_name , isDebug, query , listArg = []):
    if( len( listArg ) > 0 ) : tquery = query % tuple( listArg )
    else : tquery = query
    print("api_command:{} query:{}".format( api_name , tquery ))
    Ret = db.selectQueryWithRet(tquery)
    if( Ret["ret"] == False ) :
        if( isDebug ) : print("api_command:{} query:{} is FAIL".format( api_name , query ))
        return {"ret": False , "cnt": 0 , "data": []}
    else:
        if (isDebug): print("api_command:{} query:{} is OK".format(api_name, query))
        return {"ret": True , "cnt": 0 , "data": Ret['data']}

def func_query_dict(  api_name , isDebug, query , requestarg , list_args = [] ):
    if( len( list_args ) > 0 ) :
        dictArgs = requestarg.to_dict(flat=True )
        cntNotContain = 0
        for elem in list_args  :
            if( elem not in dictArgs.keys() ) : cntNotContain = cntNotContain + 1
        if( cntNotContain > 0 ) :
            return {"ret": False, "code":1 , "msg":"invalid args", "cnt": 0, "data": []} # code 0 -- arg invali
        print( dictArgs )
        tquery = query.format(**dictArgs)
    else : tquery = query

    print("api_command:{} query:{}".format( api_name , tquery ))
    Ret = db.selectQueryWithRet(tquery)
    if( Ret["ret"] == False ) :
        if( isDebug ) : print("api_command:{} query:{} is FAIL".format( api_name , query ))
        return {"ret": False , "code": 2 , "msg":"query fail", "cnt": 0 , "data": []}
    else:
        if (isDebug): print("api_command:{} query:{} is OK".format(api_name, query))
        return {"ret": True , "code":0 , "msg":"ok" , "cnt": len(Ret) , "data": Ret['data']}

# global variables
app = Flask(__name__)
api = Api(app)
config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'mthx_app',
             'raise_on_warnings': True}
db = dbConMysql(config_db)
db2 = dbConMysql(config_db)

@app.route("/")
def hello():
    print(request)
    return "this is mthx flask server"

@app.route("/posttest", methods=["GET", "POST"])
def keyboard():
    print(request)
    print(request.args)
    print(request.args.get('a'))
    print(request.args.get('b'))
    return "{\"type\":\"text\"}"

@app.route("/koreantest", methods=["GET", "POST"])
@dictToJson
def modtest():
    return {"a": "한글", "b": "영어", "c": "중문"}

@app.route("/querytest", methods=["GET", "POST"])
@dictToJson
def query():
    query_countof_chapInbook = 'select ' \
                               'book_seq, ' \
                               '(select biblebook_krnm from tBibleBook where biblebook_seq = book_seq) as booknm, ' \
                               'count(*) as cnt ' \
                               'from tBibleCont ' \
                               'where bible_seq = (select bibleseq from tBible where bibleType="KN") ' \
                               'group by book_seq, bible_seq'
    return func_query( "query" ,True , query_countof_chapInbook , [] )


api_data = { "poemdata" : {"query" : 'select' \
                     ' idx_mthx_poem as idx, title, content, revision as rev' \
                     ' from' \
                     ' tb_mthx_poem_data' \
                     ' where' \
                     ' idx_mthx_poem = {idx} and revision = {rev};' , "args" : ["cmd","rev","idx"] } ,
             "praise_rhema" : {"query" : 'select * from praise' , "args" : [] },
             "poemlist" : {"query" : 'select A.idx_mthx_poem as idx, A.title as title , A.revision as rev' \
                 ' from' \
                 ' tb_mthx_poem_data as A,' \
                 ' (select idx_mthx_poem , max(revision) as MaxRev from tb_mthx_poem_data group by idx_mthx_poem) as tMaxRev' \
                 ' where' \
                 ' A.idx_mthx_poem = tMaxRev.idx_mthx_poem' \
                 ' and A.revision = tMaxRev.MaxRev;' , "args" : [] },
             "biblelist": { "query" : 'select biblebook_seq as seq , biblebook_type as type , biblebook_krnm as kname , biblebook_engnm as ename , biblebook_krsumnm as sumnm' \
                                      ' from tBibleBook' \
                                      ' where biblebook_type  = "{bible_type}";' , "args" : ["bible_type"] },
             "bible_chapcnt_with_bookseq": {"query" : 'select book_seq, max(book_chap) as cntChap from tBibleCont where book_seq = {bookseq}' , "args" : ["bookseq"] },
             "bible_view_o" : { "query" : 'select bible_seq as bibleseq , book_seq as bookseq, book_chap as bookchap, book_verse as verseseq, book_content as content from tBibleCont'\
                                        ' where book_seq = {bookseq} and book_chap = {chapseq} and bible_seq = 3' , "args" : ["bookseq" ,"chapseq"]},
             "bible_view_n" : { "query" : 'select bible_seq as bibleseq , book_seq as bookseq, book_chap as bookchap, book_verse as verseseq, book_content as content from tBibleCont'\
                                        ' where book_seq = {bookseq} and book_chap = {chapseq} and bible_seq = 4' , "args" : ["bookseq" ,"chapseq"]},
            "swinfo" : { "query" : 'select app_version, bible_version, summon_version, extra1_version , extra2_version,  extra3_version , description from tVersionInfo order by idx desc limit 1;' , "args" : [] }
             }

@app.route("/api", methods=["GET", "POST"])
@dictToJson
def api_command():
    api_command = request.args.get("cmd")
    if ( api_command in api_data.keys() ):
        return func_query_dict( api_command , True, api_data[ api_command]["query"] , request.args , api_data[api_command]['args'] )
    else :
        return {"ret": False , "code":3 , "msg":"Not supported api" , "cnt": 0 , "data": []}

@app.route("/swinfo", methods=["GET", "POST"])
@dictToJson
def swinfo():
    db_local = dbConMysql(config_db)
    query_appver = "select attrname , attrvalue from tSetting where attrname = 'appver'"
    ret_appdbver = db_local.selectQueryWithRet( query_appver )

    query_biblever = "select attrname , attrvalue from tSetting where attrname = 'bibledbver'"
    ret_bibledbver = db_local.selectQueryWithRet(query_biblever)

    query_contentver = "select attrname , attrvalue from tSetting where attrname = 'contentdbver'"
    ret_contentver = db_local.selectQueryWithRet(query_contentver)

    print( ret_appdbver['data'][0]['attrvalue'] )
    print(ret_bibledbver['data'][0]['attrvalue'])
    print(ret_contentver['data'][0]['attrvalue'])

    dicSwinfo = {"appver": ret_appdbver['data'][0]['attrvalue'], "bibledbver": ret_bibledbver['data'][0]['attrvalue'],
     "contentdbver": ret_contentver['data'][0]['attrvalue']}

    return dicSwinfo


if __name__ == '__main__':
    if False :
        app.run(debug=True , host='0.0.0.0')
    else : #jupyer
        query = "insert into tLog ( message, user ,datetime ) values ( '{message}' , '{user}' , NOW() );"
        msg = { "message" : "new server start" , "user" : "flask"}
        realquery = query.format( **msg )
        db2.commitQuery( realquery )
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 5005, app)
