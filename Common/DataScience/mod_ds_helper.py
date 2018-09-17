import pandas as pd
import ast
import numpy as np

from collections import Counter
from collections import defaultdict
from collections import OrderedDict



class mod_ds_helper :

    def __init__(self,  df ):
        self.isReady = False
        if isinstance(df, pd.DataFrame):
            self.df = df
            self.isReady = True
        else :
            print("this is not dataFrame")
    def info(self):
        print("[Information of DataFrame]\n[Dimensional]={0}".format(self.df.shape))
        for col in self.df.columns:
            print("\t[{0}]\tType:{1}\tnUni:{2}\tnNull:{3} ".format(col, self.df[col].dtype, self.df[col].nunique(), self.df[col].isnull().sum(axis=0) ))
            if( self.df[col].dtype != np.object ) :
                print( self.df[col].describe() )
    def cvtWithMap(self,srcCol,tarCol,dicMap):
        self.df[tarCol] = self.df[srcCol].map(dicMap)
    def cvtPunctWord(self,srcCol, tarCol):
        self.df[tarCol] = self.df[srcCol].str.extract(' ([A-Za-z]+)\.', expand=False)
    def binning(self , column, listTargets ):
        prevVal = 0
        for i,value in enumerate( listTargets ) :
            if( i == 0 ) :
                self.df.loc [ self.df[column] <= value , column] = i
            elif ( i == (len(listTargets)-1) ) :
                self.df.loc[(self.df[column] > prevVal) & (self.df[column] <= value), column] = i
                self.df.loc [ self.df[column] > value , column] = i + 1
            else :
                self.df.loc[ (self.df[column] > prevVal) & (self.df[column] <= value) , column] = i
            prevVal = value
        #self.df[column] = self.df[column].astype(str).astype(int)
    def fillnaWithMedian(self, colGroup, colTar ):
        self.df[colTar].fillna(self.df.groupby(colGroup)[colTar].transform("median"), inplace=True)
    def dropColumn(self,tarcol):
        self.df.drop(tarcol,axis=1,inplace=True)

    # this funtions process the json field
        # _internal function
    def _json_get_field(self,x):
        return [ i[ self._json_field_name ] for i in x ] if isinstance(x, list) else []
        # json to list with single field
    def json_to_list_withField(self,colSrc,colTar,field):
        self._json_field_name = field
        self.df[colTar] = self.df[colSrc].fillna('[]').apply(ast.literal_eval).apply(self._json_get_field)
    def get_cntDict_from_listField(self, listField):
        cnt_tmp = Counter()
        self.df[listField].apply(cnt_tmp.update)
        return dict( cnt_tmp )
    def _json_kv_pairing(self , x):
        if( isinstance( x,list) ) :
            for i in x :
                cur_key = i[self._tmp_key]
                cur_val = i[self._tmp_val]
                if (i[self._tmp_key] not in self._tmp_dict.keys()):
                    self._tmp_dict[ cur_key ] = cur_val
    def get_kvDict_from_listField(self, jsoncolumn, kfield, vfield ):
        self._tmp_dict = {}
        self._tmp_key  = kfield
        self._tmp_val  = vfield
        self.df[jsoncolumn].fillna('[]').apply(ast.literal_eval).apply(self._json_kv_pairing)
        return self._tmp_dict
    def get_cntDicItem(self,dicCnt,isSort):
        ddic = defaultdict(lambda: 0)
        for k, v in dicCnt.items():
            int_v = int(v)
            ddic[int_v] = ddic[int_v] + 1
        if ( isSort ) :
            return OrderedDict(sorted(ddic.items()))
        else :
            return ddic

    def _list_to_max(self, x):
        max_key = ""
        if( isinstance( x,list ) ) :
            for elem in x :
                if( max_key == "" ) : max_key = elem
                else :
                    if( self._tmp_dict[ elem ] > self._tmp_dict[ max_key] ) : max_key = elem
            return [max_key]
        else :
            return []
    def set_listfield_maxvalue_withDict(self, srcCol, tarCol, dictMap ):
        self._tmp_dict = dictMap
        self.df[tarCol] = self.df[srcCol].apply(self._list_to_max)
        self._tmp_dict = {}

    def _list_to_filter_minval(self, x):
        if( isinstance( x,list ) ) :
            for elem in x :
                if( self._tmp_dict[ elem ] > self._minval ) : max_key = elem
            return [max_key]
        else :
            return []
    def set_listfield_filtered_withDict(self, srcCol, tarCol, minval , dictMap ):
        self._tmp_dict = dictMap
        self.df[tarCol] = self.df[srcCol].apply(self._list_to_filter_minval)
        self._tmp_dict = {}

    def get_onehotcoding_df(self,column):
        return pd.get_dummies(self.df[column].apply(pd.Series).stack()).sum(level=0)