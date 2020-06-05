#conda install -c anaconda flask

from flask import Flask
from flask import Response
from flask import request
from flask_restful import Resource
from flask_restful import Api
#from flaskext.mysql import MySQL
from functools import wraps
import json
import re
import sys
sys.path.append("../Common")
from Mysql.libmysql import dbConMysql

#helper functions
def dictToJson(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')
    return decorated_function

#global variables
app = Flask(__name__)
api = Api(app)

config_db = {'user': 'root',          'password': 'karisma*3%7*4',          'host': 'mthx.cafe24.com',          'database': 'bible',          'raise_on_warnings': True }
db      = dbConMysql(config_db)


@app.route("/")
def hello() :
    print(request)
    return "hello"

@app.route("/keyboard", methods=["GET","POST"])
def keyboard() :
    print(request)
    print(request.args)
    print(request.args.get('a'))
    print(request.args.get('b'))
    return "{\"type\":\"text\"}"

@app.route("/querytest", methods=["GET","POST"])
@dictToJson
def modtest():
    return {"a":"한글" , "b":"영어" , "c":"중문"}

@app.route("/query", methods=["GET","POST"])
@dictToJson
def query():
    query_countof_chapInbook = 'select ' \
     'book_seq, ' \
     '(select biblebook_krnm from tBibleBook where biblebook_seq = book_seq) as booknm, '\
     'count(*) as cnt '\
     'from tBibleCont '\
     'where bible_seq = (select bibleseq from tBible where bibleType="KN") '\
     'group by book_seq, bible_seq'
    print( query_countof_chapInbook )
    listRet = db.selectQuery( query_countof_chapInbook )
    cntLen = len(listRet)
    print( cntLen )
    if( cntLen > 0 ) :
        print( listRet[0] )
        print( listRet[0].keys() )
        return listRet;


@app.route("/command", methods=["GET","POST"])
@dictToJson
def command():
    print("command a:{0},b:{1}".format( request.args.get("a") , request.args.get("b") ))
    query_countof_chapInbook = ""
    if( int(request.args.get("a")) == 1 and int(request.args.get("b")) == 1 ) :
        query_countof_chapInbook = 'select ' \
                'book_seq, ' \
                '(select biblebook_krnm from tBibleBook where biblebook_seq = book_seq) as booknm, ' \
                'count(*) as cnt ' \
                'from tBibleCont ' \
                'where bible_seq = (select bibleseq from tBible where bibleType="KN") ' \
                'group by book_seq, bible_seq'
    else :
        query_countof_chapInbook = 'select ' \
            'book_seq, ' \
            '(select biblebook_krnm from tBibleBook where biblebook_seq = book_seq) as booknm, ' \
            'count(*) as cnt ' \
            'from tBibleCont ' \
            'where bible_seq = (select bibleseq from tBible where bibleType="KO") ' \
            'group by book_seq, bible_seq'

    print( query_countof_chapInbook )
    listRet = db.selectQuery( query_countof_chapInbook )
    cntLen = len(listRet)
    print( cntLen )
    if( cntLen > 0 ) :
        print( listRet[0] )
        print( listRet[0].keys() )
        return listRet;


if __name__ == '__main__':
    if False :
        app.run(debug=True , host='0.0.0.0')
    else : #jupyer
        from werkzeug.serving import run_simple
        run_simple('0.0.0.0', 5005, app)