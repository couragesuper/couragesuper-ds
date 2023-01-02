import pandas as pd

# 유튜브 채널 전체에서 가져온 동영상을 정리

df = pd.read_excel("hsnewacts_movie.xlsx")
df = df.fillna( value = "" )
print( df)

dictSermon = df.to_dict("records")

print( dictSermon )

idx = 1
listOutput = []

if False :
    for elem in dictSermon :
        if( elem['cate1'] == "설교" ) :
            data = {}
            print( elem )

            data['idx'] = idx
            data['youtubeid'] = elem['link'].split("=")[1]
            data['youtube_index'] = idx
            idx = idx + 1

            data['title_cate'] = '홀새 설교'
            data['date'] = "reserved"
            data['title'] = elem['edit']
            data['person'] = elem['cate2']
            listOutput.append(data)

    print( listOutput )

    df_ret = pd.DataFrame( listOutput )
    df_ret.to_excel( "hsnewact_sermon_sat.xlsx" )

if False :
    for elem in dictSermon :
        if( elem['cate1'] == "뉴액츠" ) :
            data = {}
            print( elem )

            data['idx'] = idx
            data['youtubeid'] = elem['link'].split("=")[1]
            data['youtube_index'] = idx
            idx = idx + 1

            data['title_cate'] = '뉴액츠'
            data['date'] = "reserved"
            data['title'] = elem['edit']
            data['person'] = elem['cate2']
            listOutput.append(data)

    print( listOutput )

    df_ret = pd.DataFrame( listOutput )
    df_ret.to_excel( "hsnewact_intro.xlsx" )

if False :
    for elem in dictSermon :
        if( elem['cate1'] == "워크샵" ) :
            data = {}
            print( elem )

            data['idx'] = idx
            data['youtubeid'] = elem['link'].split("=")[1]
            data['youtube_index'] = idx
            idx = idx + 1

            data['title_cate'] = 'workshop'
            data['date'] = "reserved"
            data['title'] = elem['edit']
            data['person'] = elem['cate2']
            listOutput.append(data)

    print( listOutput )

    df_ret = pd.DataFrame( listOutput )
    df_ret.to_excel( "hsnewact_workshop.xlsx" )

if False:
    for elem in dictSermon:
        if (elem['cate1'] == "찬양"):
            data = {}
            print(elem)

            data['idx'] = idx
            data['date'] = "reserved"
            data['singer'] = elem['cate2']
            data['youtubeid'] = elem['link'].split("=")[1]

            idx = idx + 1
            data['song1'] = elem['edit']
            if( len (  elem['Song'] ) != 0  ) :
                data['song_search'] = elem['Song']

            listOutput.append(data)

    print(listOutput)

    df_ret = pd.DataFrame(listOutput)
    df_ret.to_excel("hsnewact_song_sat.xlsx")



if False :
    for elem in dictSermon :
        if( elem['cate1'] == "GBS" ) :
            data = {}
            print( elem )

            data['idx'] = idx
            data['youtubeid'] = elem['link'].split("=")[1]
            data['youtube_index'] = idx
            idx = idx + 1

            data['title_cate'] = 'GBS'
            data['date'] = "reserved"
            data['title'] = elem['edit']
            data['person'] = elem['cate2']
            listOutput.append(data)

    print( listOutput )

    df_ret = pd.DataFrame( listOutput )
    df_ret.to_excel( "hsnewact_gbs.xlsx" )


if True :
    for elem in dictSermon :
        if( elem['cate1'] == "뉴액츠스토리" ) :
            data = {}
            print( elem )

            data['idx'] = idx
            data['youtubeid'] = elem['link'].split("=")[1]
            data['youtube_index'] = idx
            idx = idx + 1

            data['title_cate'] = '뉴액츠스토리'
            data['date'] = "reserved"
            data['title'] = elem['edit']
            data['person'] = elem['cate2']
            listOutput.append(data)

    print( listOutput )

    df_ret = pd.DataFrame( listOutput )
    df_ret.to_excel( "hsnewact_story.xlsx" )