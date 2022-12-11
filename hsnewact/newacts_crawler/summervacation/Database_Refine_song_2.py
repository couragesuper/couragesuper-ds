import pandas as pd
import datetime

# 183번까지만 데이터가 정형화되어있음.

df = pd.read_excel("hsnewact_song_clean.xlsx")
#print( df)

dictSong = df.to_dict("records")
#print( dictSong )

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

def validate_date_raw (date_text) :
    try:
        datetime.datetime.strptime(date_text, "%Y%m%d")
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

listSongs = []
lenSong = len(dictSong)

max_song = 0
for song in dictSong :
    try :
        song_data = {}
        song_data['Id'] = song['Id']
        song_data['date'] = song['date']
        song_data['singer'] = song['singer'].rstrip().lstrip()
        song_data['youtubeid'] = song['youtubeid']
        song_data['song1'] = song['song1']
        song_data['song2'] = song['song2']
        song_data['song3'] = song['song3']
        song_data['song4'] = song['song4']
        song_data['song_search'] = song['song1'].replace(" ","") + str(song['song2']).replace(" ","") + str(song['song3']).replace(" ","") + str(song['song4']).replace(" ","")
        song_data['song_search'] = song_data['song_search'].replace("nan" ,"")
        listSongs.append(song_data)

    except Exception as e :
        print( "[exception] id={} exceoption={}".format( song['Id'] , e))

df_ret = pd.DataFrame(listSongs)
df_ret.to_excel("hsnewact_song_clean2.xlsx")



print("max-song = {}".format( max_song ))
