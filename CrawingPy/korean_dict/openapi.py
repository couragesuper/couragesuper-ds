import urllib.request
from xml.etree import ElementTree as ET

# 한국어 사전 Open API를 사용하는 샘플


if False :
    authkey = "5A0C7461A0E21C7DD7B237BE56922A61"
    encText = urllib.parse.quote("나무")
    url = "https://krdict.korean.go.kr/api/search?key=" + authkey + "&type_search=search&method=WORD_INFO&part=word&q=" + encText +"&sort=dict"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        print(response_body.decode('utf-8'))
        # XML 해석하기
        root = ET.fromstring( response_body )
        print( root.tag )
        for child in root :
            print( child.tag )
            if( child.tag == "item" ) :
                for child_elem in child :
                    print( "elem={}, text={}".format( child_elem.tag , child_elem.text ) )
                    if child_elem.tag == "sense" :
                        for child_elem_elem in child_elem :
                            if child_elem_elem.tag == "definition" :
                                print( "definition={}".format(child_elem_elem.text) )
    else:
        print("Error Code:" + rescode)

def searchWordInDict( korean ) :
    # activation key
    authkey = "5A0C7461A0E21C7DD7B237BE56922A61"

    # make search url
    encText   = urllib.parse.quote( korean )
    searchUrl = "https://krdict.korean.go.kr/api/search?key=" + authkey + "&type_search=search&method=WORD_INFO&part=word&q=" + encText + "&sort=dict"
    request   = urllib.request.Request(searchUrl)

    # get response
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    dicRet = {"word":korean,"pos": "없음" , "뜻":[]}

    if( rescode == 200 ):
        response_body = response.read()
        #print(response_body.decode('utf-8'))
        # XML 해석하기
        root = ET.fromstring(response_body)
        nCntSearch = 0
        for child in root :
            isFound = False
            if( child.tag == "item" ) : # equal
                for ch_ch in child :
                    if( ch_ch.tag == "word" ):
                        if( ch_ch.text == korean ) :
                            dicRet["found"] = True
                            isFound = True
                    if( (isFound == True) and (ch_ch.tag == "pos") ) :
                        dicRet["pos"] = ch_ch.text
                    if( (isFound == True) and (ch_ch.tag == "sense")) :
                        for ch_ch_ch in ch_ch :
                            if( ch_ch_ch.tag == "definition" ):
                                dicRet["뜻"].append( ch_ch_ch.text)

    else:
        print("Error Code:" + rescode)

    return dicRet

dicRet = searchWordInDict( "나무" )
print( dicRet )
dicRet = searchWordInDict( "나무꾼" )
print( dicRet )
dicRet = searchWordInDict( "성경" )
print( dicRet )
dicRet = searchWordInDict( "예수" )
print( dicRet )
dicRet = searchWordInDict( "캄보디아" )
print( dicRet )






