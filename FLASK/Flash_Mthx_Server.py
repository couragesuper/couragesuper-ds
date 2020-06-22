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
config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
             'raise_on_warnings': True}
db = dbConMysql(config_db)

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
                 ' and A.revision = tMaxRev.MaxRev;' , "args" : [] }
             }

@app.route("/api", methods=["GET", "POST"])
@dictToJson
def api_command():
    api_command = request.args.get("cmd")
    if ( api_command in api_data.keys() ):
        return func_query_dict( api_command , True, api_data[ api_command]["query"] , request.args , api_data[api_command]['args'] )
    else :
        return {"ret": False , "code":3 , "msg":"Not supported api" , "cnt": 0 , "data": []}



if __name__ == '__main__':
    if False :
        app.run(debug=True , host='0.0.0.0')
    else : #jupyer
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 5005, app)