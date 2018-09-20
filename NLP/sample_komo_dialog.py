import sys
import time
import pprint
import pandas as pd
import numpy as np
# Modeling
# Importing Classifier Modules
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import numpy as np
# machine learning
# 회귀나 그런  문제가 아니다. 이것은 딱. .... 딥러닝을 사용해야 할 문제인듯 함.
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from collections import defaultdict

sys.path.append("../Common/Crawler")
sys.path.append("../Common/Util")
sys.path.append("../Common/NLP")
from komoran.komoran3py  import Komoran

sys.path.append("../Common")
from Visualizer  import mod_viz_helper as viz
from DataScience import mod_ds_helper  as dp

# for bigram
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

# Create Tagger with komoran
komoran = Komoran()

# include Tag lists 
listIncTag = ['NN','NR','NP','VA','VV','SF',"MA","MD","XS"]

# komoran test
if False :
    df_dlg = pd.read_csv( "../Data/Dialog/Dialog1.csv" , delimiter="," , encoding="euckr")
    print( df_dlg )
    listDic = []
    # initalize komoran

    def apply_df_komoran( x ):
        result = komoran.getTokensList(x)
        listDic.append( result )

    df_dlg['ASK'].apply( apply_df_komoran )
    for i,elem in enumerate( listDic ):
        print( df_dlg.loc[i,'ASK'] )
        pprint.pprint( elem )


# komoran test with input data
if False :
    while ( True ) :
        text = input("형태소 분석할 데이터를 입력해주세요.")
        if( text != "") :
            result = komoran.getTokensList(text)
            pprint.pprint( result )
        else : print("공백을 입력하지 마십시요.")


if True :
    df_dlg = pd.read_csv("../Data/Dialog/Dialog1.csv", delimiter=",", encoding="euckr")
    # 일단은 매우 간단한 형태로 벡터를 만들어 냅니다.

    nShape = df_dlg.shape[0]
    print( nShape )
    listTokens_s = []

    # komoran data
    def cvtSentToWordTagList( sent , komo_tagger, include_tag ) :
        listWordTag = []
        komo_ret = komo_tagger.getTokensList(sent)
        for i,elem in enumerate( komo_ret ):
            tag = elem['pos'][:2]
            if( tag in listIncTag ) :
                word = elem['morph'] + "_" + tag
                listWordTag.append( word )
        return listWordTag


    for i in range(0, nShape):
        listTokens = []
        sent   = df_dlg.loc[i, 'ASK']
        listTokens_s.append( cvtSentToWordTagList( sent, komoran, listIncTag ) )
    df_dlg['TAGS'] = listTokens_s

    print( df_dlg )
    ds_dialog = dp.mod_ds_helper(df_dlg )
    dicDatas = ds_dialog.get_cntDict_from_listField("TAGS")
    print( dicDatas )

    dicEntry = ds_dialog.get_entryDict_from_listField("TAGS")
    print( dicEntry )

    ds_dialog.cvt_klistTovlist("TAGS","TAGS_V",dicEntry)
    print( ds_dialog.df['TAGS_V'])

    # one hot coding에서 소숫점이 발생해서 없앴어

    train  = ds_dialog.get_onehotcoding_df('TAGS_V')
    print( ds_dialog.df.Intent )

    dicIntent = ds_dialog.get_entryDict_from_Field("Intent")
    print( "dicIntent={}".format(dicIntent))

    ds_dialog.cvtWithMap("Intent","Intent",dicIntent)

    target = ds_dialog.df['Intent']
    # 머신러닝으로 분류기를 만들기
    print( train )
    print( target )



    # 이 문제는 One-hot 코딩으로 만들어진 벡터 사이의 연관성보다는
    # 대화의 용도 분류에 따라서, 사용되는 분류가 제각각이다.
    # 이러한 경우에는 어떻게 학습을 시켜서, 분류기를 만드는 것이 효과적인가?
    listResult = []
    isMidTest = False
    nLoop = 10

    def showResult( clf, train, target ):
        clf.fit(train, target)
        for j in range(0,nLoop):
            listResult = []
            iOk = 0
            for i in range(0,train.shape[0]):
                df_test = train.iloc[i:i+1]
                target_pre = clf.predict(df_test)
                if( isMidTest ) : print("{}={}={}".format(i, df_test, target_pre))
                if( target_pre == target.loc[i])    :
                    listResult.append(True)
                    iOk = iOk + 1
                else :
                    listResult.append(False)
            print( "j=nOK:{},{}".format(iOk,listResult) )

    if False :
        print( "KNeighborsClassifier" )
        clf = KNeighborsClassifier(n_neighbors=8)
        showResult( clf, train, target )
    if False :
        print("RandomForestClassifier")
        clf = RandomForestClassifier( n_estimators = 9 )
        showResult(clf, train, target)
    # 이 one-hot 코딩에 대해서 잘 나왔다.
    if True :
        print("GaussianNB")
        clf = GaussianNB()
        showResult(clf, train, target)
    if False :
        print("SVC")
        clf = SVC()
        showResult(clf, train, target)

    def sentToClassVector( sent , komo_tagger, listIncTag , dicVectorWord ) :
        print(sentToClassVector)
        listWordTag = []
        komo_ret = komo_tagger.getTokensList(sent)
        for i,elem in enumerate( komo_ret ):
            tag = elem['pos'][:2]
            if( tag in listIncTag ) :
                word = elem['morph'] + "_" + tag
                listWordTag.append( word )
        #print( "listWordTag={}".format(listWordTag))
        dict_df = defaultdict(lambda: 0)
        for k,v in dicVectorWord.items() :
            dict_df[v] = 0
        for i in listWordTag :
            #print( "{}".format( i ) )
            if( i in dicVectorWord.keys() ) :
                dict_df[ dicVectorWord[i] ] = 1
        list_dict_df = [dict_df]
        tmp_df = pd.DataFrame( list_dict_df )
        return tmp_df

    listSent= ["안녕하니?","안녕하세요","어떻게 지내나요?","어떻게 지내세요?","어떻게 지낼까요?","어떻게 지내?"]
    for sent in listSent :
        ret_df = sentToClassVector( sent , komoran, listIncTag, dicEntry)
        print( "{}={}".format( sent, clf.predict(ret_df)) )

    listWrong = ["하이","Hello","안늉","어때?"]
    for sent in listWrong:
        ret_df =  sentToClassVector( sent , komoran, listIncTag, dicEntry)
        predict = clf.predict(ret_df)
        print( "{}={}".format( sent, predict ) )
        class_id = predict
        inner_product = np.inner(train.loc[class_id], ret_df)
        result = np.sum( train.loc[class_id] , axis = 1 )
        print( "inner product = {}/{}...??".format( inner_product[0][0], result ))

    # wrong answer인지는 이렇게 구분할 수가 있다.
    # 잘못된 문장에 대해서는 재학습을 수행한다.



















