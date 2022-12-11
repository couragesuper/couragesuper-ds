import pandas as pd
import datetime

# 183번까지만 데이터가 정형화되어있음.

df = pd.read_excel("hsnewact_sermon.xlsx")
print( df)

dictSermon = df.to_dict("records")
print( dictSermon )

def validate_date(date_text):
	try:
		datetime.datetime.strptime(date_text,"%Y-%m-%d")
		return True
	except ValueError:
		print("Incorrect data format({0}), should be YYYY-MM-DD".format(date_text))
		return False


def validate_date_dot(date_text):
	try:
		datetime.datetime.strptime(date_text,"%Y-%m-%d")
		return True
	except ValueError:
		print("Incorrect data format({0}), should be YYYY-MM-DD".format(date_text))
		return False


def getDate ( str ) :
    str_nospace = str.lstrip().rstrip().replace(' ' , '').replace("." ,"-")

    str_datec_candidate = str_nospace[-11:]
    if (str_datec_candidate[0] == '-'): str_datec_candidate = str_datec_candidate[1:]
    if (str_datec_candidate[len(str_datec_candidate) - 1] == '-'): str_datec_candidate = str_datec_candidate[: len(str_datec_candidate) - 1]

    if( validate_date_dot( str_datec_candidate ) == True ) :
        return { 'ret':True , 'date': str_datec_candidate }
    else :
        return { 'ret':False }

def getLargeBracket ( str ) :
    isStartBr = False
    idxStartBr = 0
    isEndBr = False
    idxEndBr = 0
    for idx in range(0,len(str)) :
        if( str[idx] == "[" ) :
            isStartBr = True
            idxStartBr = idx
            #print("[=>{}".format(str[idx]))
        if( (isStartBr == True) and (str[idx] == "]") ) :
            isEndBr = True
            idxEndBr = idx
            #print("]=>{}".format(str[idx]))
    if( isStartBr and isEndBr ) :
        return { "data": str[idxStartBr + 1:idxEndBr] , "ret":True , "startIdx" : idxStartBr , "endIdx" : idxEndBr }
    else :
        return { "ret" : False }

listSermos = []

for sermon in dictSermon :
    #https://www.youtube.com/watch?v=_MPiDbKMntE&list=PLax91QpCgwn31ascF3Axm29qryugXmZDt&index=1

    #1. youtube_id and index
        # watch 이루를 얻어냄
    arr = sermon['link'].split("/")[3].split("?")[1].split("&")
        # arg의 youtube id와 index를 얻어냄.
    sermon['youtubeid'] = arr[0].split("=")[1]
    sermon['youtube_index'] = arr[2].split("=")[1]

    if( sermon['youtube_index'] == '180') :
        break

    #2. title
        # category
    title = sermon["title"]
    ret = getLargeBracket( title )
    #sermon['title_cate_ret'] = ret['ret']
    if( ret["ret"] == True  ) :
        #print( ret )
        sermon['title_cate'] = ret['data']

        # date
    ret_date = getDate ( title )
    #sermon['date_ret'] = ret_date['ret']
    if( ret_date['ret'] == False ) :
        print( "getDate error == idx:{} data:{} ".format( sermon['index'] , ret_date ) )
    else :
        sermon['date'] = ret_date['date']

    sermon['title_renew'] = title.split("]")[1].split("-")[0].lstrip().rstrip();
    sermon['person'] = "도원욱 담임 목사님"
    listSermos.append( sermon )


df_ret = pd.DataFrame( listSermos )
df_ret.to_excel( "hsnewact_sermon_clean.xlsx" )
