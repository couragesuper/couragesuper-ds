import urllib.request

# Description : Naver Open API를 사용하는 샘플

client_id = "yyFwbIusxKeX0aAEedrq"  # 애플리케이션 등록시 발급 받은 값 입력
client_secret = "_H8bEfsjZv"  # 애플리케이션 등록시 발급 받은 값 입력

#url = "https://openapi.naver.com/v1/search/book?query=" + encText + "&display=3&sort=count"
encText = urllib.parse.quote("김용기")
url = "https://openapi.naver.com/search/" + encText

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if (rescode == 200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)