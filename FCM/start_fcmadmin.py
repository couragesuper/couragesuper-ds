#https://dgkim5360.tistory.com/entry/python-requests

isRequest = True

if( isRequest ) :
    #득정 사이트에서 request 를 수행하는 코드
    import requests

    URL = 'http://www.ucc.or.kr/'
    response = requests.get(URL)
    print( response.status_code )
    print( response.text )

    params = {'param1': 'value1', 'param2': 'value'}
    res = requests.get(URL, params=params)
else:
    #g하단은 어떻게 처리해야 하는지 모르겠음
    import requests, json
    data = {'outer': {'inner': 'value'}}
    res = requests.post(URL, data=json.dumps(data))

    headers = {'Content-Type': 'application/json; charset=utf-8'}
    cookies = {'session_id': 'sorryidontcare'}
    res = requests.get(URL, headers=headers, cookies=cookies)


import requests

URL_template = "https://fcm.googleapis.com/v1/{parent=projects/*}/messages:send"
URL_template2 = "https://fcm.googleapis.com/v1/{parent=mthx-app-v1/*}/messages:send"

requests.get( URL_template2 )

#https://console.firebase.google.com/project/mthx-app-v1/notification











































