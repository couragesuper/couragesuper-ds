import sys
import time
import pprint
import pandas as pd
import numpy as np
import pickle as pk
from collections import defaultdict

sys.path.append("../NLP")
sys.path.append("../Mysql")
sys.path.append("../")

from libmysql import dbConMysql
from DataScience import mod_ds_helper  as dp
from mod_nlp_helper import komoHelper

from sklearn.naive_bayes import GaussianNB
from komoran.komoran3py  import Komoran

class mod_chatbot_dialog :
    def __init__(self ,  incTags = ['NN', 'NR', 'NP', 'VA', 'VV', 'SF', "MA", "MD", "XS"] , dbConfig = { 'user': 'root','password': 'karisma*3%7*4','host': 'mthx.cafe24.com','database': 'chatbot','raise_on_warnings': True } ,  isLogOut = True ):
        self.isLogOut = isLogOut
        if( self.isLogOut ) : print( "[Chatbot mod] created" )
        self.lIncTags = incTags
        self.db_config = dbConfig
        self.db = dbConMysql(self.db_config)
        if (self.isLogOut): print("[Chatbot mod] db is created.")
        self.komohelper = komoHelper()
        self.komohelper.UpdateTextFile("userDict.txt")
        self.komoran = Komoran()
        self.komoran.set_user_dictionary("userDict.txt")
        self.state = 0

    def learning(self):
        self.lTokens_tagged = []
        self.db_ret =  self.db.selectQuery("select * from tDlgTest")
        if( len( self.db_ret ) == 0 ) :
            print("[Chatbot mod] Dialog Data is empty.")
            return

        self.df = pd.DataFrame( self.db_ret )
        self.ds = dp.mod_ds_helper( self.df )

        nShape = self.df.shape[0]
        lWordTags = []
        for i in range(0, nShape):
            sent = self.df.loc[i, 'sentence']
            lWordTags.append( self._cvtSentToWordTagList(sent))
        self.df['Tags'] = lWordTags

        # listField -> counter -> Dict
        dicTags = self.ds.get_cntDict_from_listField("Tags")
        self.dicEntry = self.ds.get_entryDict_from_listField("Tags")  ## this is used to
        self.ds.cvt_klistTovlist("Tags", "TagsVal", self.dicEntry)

        self.train = self.ds.get_onehotcoding_df('TagsVal')
        dicIntent = self.ds.get_entryDict_from_Field("sentID")
        self.ds.cvtWithMap("sentID", "sentID", dicIntent)
        self.target = self.ds.df['sentID']

        self.clf = GaussianNB()
        self.clf.fit(self.train, self.target)
        self.state = 1

    # "명사" -> "명사_NN"
    def _cvtSentToWordTagList( self, sent) :
        listWordTag = []
        komo_ret = self.komoran.getTokensList(sent)
        for i,elem in enumerate( komo_ret ):
            tag = elem['pos'][:2]
            if( tag in self.lIncTags ) :
                word = elem['morph'] + "_" + tag
                listWordTag.append( word )
        return listWordTag

    def _sentToVector( self, sent ):
        listWordTag = self._cvtSentToWordTagList( sent )
        dict_df = defaultdict(lambda: 0)
        for k, v in self.dicEntry.items():
            dict_df[v] = 0
        for i in listWordTag:
            # print( "{}".format( i ) )
            if (i in self.dicEntry.keys()):
                dict_df[self.dicEntry[i]] = 1
        list_dict_df = [dict_df]
        tmp_df = pd.DataFrame(list_dict_df)
        return tmp_df

    def reply(self ,sent ):
        ret_df = self._sentToVector(sent)
        class_id = int(self.clf.predict(ret_df))
        #print( "class_id {}".format( class_id ))
        inner_product = np.inner(self.train.loc[class_id], ret_df)
        #print( "train = {}".format( self.train ))
        #print( inner_product )
        #result = np.sum(self.train.loc[class_id], axis=1)
        if (inner_product[0] != 0):
            print("%s" % (self.db_ret[int(class_id)]['reply']))
        else:
            print("언젠가는 네가 무슨 말을 하는지 알수 있겠지?")

    def dump(self):
        with open('chatbot_clf.pkl', 'wb') as f:
            pk.dump(self.clf, f)
        if False :
            with open('chatbot_dicEntry.pkl', 'wb') as f:
                pk.dump(self.dicEntry, f)
            with open('chatbot_lncTags.pkl', 'wb') as f:
                pk.dump(self.lIncTags, f)

chatbot = mod_chatbot_dialog()
chatbot.learning()
#chatbot.dump()

sent = input()
while sent != "quit" :
    chatbot.reply( sent )
    sent = input()

chatbot_load = pk.load("chatbot.pkl")
chatbot_load.load()













