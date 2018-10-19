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

sys.path.append("../../Common/Crawler")
sys.path.append("../../Common/Util")
sys.path.append("../../Common/NLP")
sys.path.append("../../Common/Mysql")
sys.path.append("../../Common")

from komoran.komoran3py  import Komoran
from Visualizer  import mod_viz_helper as viz
from DataScience import mod_ds_helper  as dp

from mod_nlp_helper import komoHelper
from libmysql import dbConMysql

komohelper = komoHelper()
komoran = Komoran()

# Include Tag lists
listIncTag = ['NN','NR','NP','VA','VV','SF',"MA","MD","XS"]

config =  {
          'user': 'root',
          'password': 'karisma*3%7*4',
          'host': 'mthx.cafe24.com',
          'database': 'chatbot',
          'raise_on_warnings': True
}

db = dbConMysql( config )
dlg_ret = db.selectQuery( "select * from tDlgTest" )

#print(  dlg_ret[0]['reply'] )
#exit(0)

# 학습하려면 pandas가 있어야 되는 듯한 느낌이다. vector 처리할 거니까..
# 나중엔 다른 방법으로도 할 수 있지만. 일단은 pandas에 써볼까?

# create pandas
df_dlg = pd.DataFrame( dlg_ret )

print( df_dlg )
nShape = df_dlg.shape[0]
print( nShape )
listTokens_s = []

# komoran data
def cvtSentToWordTagList( sent , komo_tagger, include_tag ) :
    listWordTag = []
    komo_ret = komo_tagger.getTokensList(sent)
    for i,elem in enumerate( komo_ret ):
        tag = elem['pos'][:2]
        if( tag in include_tag ) :
            word = elem['morph'] + "_" + tag
            listWordTag.append( word )
    return listWordTag

nLoop      = 10
isMidTest = True


def sentToClassVector(sent, komo_tagger, listIncTag, dicVectorWord):
    print(sentToClassVector)
    listWordTag = []
    komo_ret = komo_tagger.getTokensList(sent)
    for i, elem in enumerate(komo_ret):
        tag = elem['pos'][:2]
        if (tag in listIncTag):
            word = elem['morph'] + "_" + tag
            listWordTag.append(word)
    # print( "listWordTag={}".format(listWordTag))
    dict_df = defaultdict(lambda: 0)
    for k, v in dicVectorWord.items():
        dict_df[v] = 0
    for i in listWordTag:
        # print( "{}".format( i ) )
        if (i in dicVectorWord.keys()):
            dict_df[dicVectorWord[i]] = 1
    list_dict_df = [dict_df]
    tmp_df = pd.DataFrame(list_dict_df)
    return tmp_df


for i in range(0, nShape):
    listTokens = []
    sent   = df_dlg.loc[i, 'sentence']
    listTokens_s.append( cvtSentToWordTagList( sent, komoran, listIncTag ) )

df_dlg['TAGS'] = listTokens_s

print( df_dlg )
ds_dialog = dp.mod_ds_helper(df_dlg )
dicDatas = ds_dialog.get_cntDict_from_listField("TAGS")
print( dicDatas )

dicEntry = ds_dialog.get_entryDict_from_listField("TAGS")
print( dicEntry )

ds_dialog.cvt_klistTovlist("TAGS", "TAGS_V", dicEntry)
print(ds_dialog.df['TAGS_V'])

# one hot coding에서 소숫점이 발생해서 없앴어
train = ds_dialog.get_onehotcoding_df('TAGS_V')
print(ds_dialog.df.sentID)

dicIntent = ds_dialog.get_entryDict_from_Field("sentID")
print("dicIntent={}".format(dicIntent))

ds_dialog.cvtWithMap("sentID", "sentID", dicIntent)
target = ds_dialog.df['sentID']

clf = GaussianNB()
clf.fit(train, target)

sent = input()

# 맞춤법

while sent != "quit" :
    try:
        ret_df = sentToClassVector( sent , komoran, listIncTag, dicEntry )
        #print( "ret=df",ret_df )
        predict = clf.predict(ret_df)
        class_id = predict
        inner_product = np.inner(train.loc[class_id], ret_df)
        #print( inner_product )
        result = np.sum(train.loc[class_id], axis=1)
        #print("class : %d " % ( class_id ) )
        #print( "inner product :{}" , inner_product )
        if( inner_product[0][0] != 0 ) :
            #print( "expected answer:%s" %(dlg_ret[int(class_id)]['reply'] ))
            print("%s" % (dlg_ret[int(class_id)]['reply']))
        else :
            print("언젠가는 네가 무슨 말을 하는지 알수 있겠지?")
        sent = input()
    except :


