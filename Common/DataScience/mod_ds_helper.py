import pandas as pd
import ast
import numpy as np

from collections import Counter
from collections import defaultdict
from collections import OrderedDict

class mod_ds_helper :
    def __init__(self,  df ):
        print("ver 1.1")
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
    def info_unique(self):
        for col in self.df.columns:
            try :
                print("{}={}".format(col,self.df[col].unique()))
            except:
                continue
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

    def _list_to_entry(self,x):
        if (isinstance(x, list)):
            for i in x:
                if( i not in self._tmp_dict.keys() ) :
                    nElem = len( self._tmp_dict )
                    self._tmp_dict[ i ] = nElem
    def get_entryDict_from_listField(self, listField):
        self._tmp_dict = defaultdict(lambda: 0)
        self.df[listField].apply(self._list_to_entry)
        return self._tmp_dict

    def _field_to_entry(self,x):
        if( x not in self._tmp_dict.keys() ) :
            nElem = len( self._tmp_dict )
            self._tmp_dict[ x ] = nElem

    def get_entryDict_from_Field(self,Field):
        self._tmp_dict = defaultdict(lambda: 0)
        self.df[Field].apply(self._field_to_entry)
        return self._tmp_dict

    #
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

    def _cvtKtoV(self,x):
        if (isinstance(x, list)):
            new_list = []
            for i in x:
                new_list.append( int(self._tmp_dict[i]) )
            return new_list
        return []

    def cvt_klistTovlist(self,srcField,tarField,dicKV):
        self._tmp_dict = dicKV
        self.df[tarField] = self.df[srcField].apply( self._cvtKtoV )

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
        # 소숫점이 되네 ....
        if False :
            temp = self.df[column].apply(pd.Series)
            print( "apply Series={}".format(temp) )
            print( temp.dtypes)
            temp2 = temp.stack()
            print( "stack ={}".format(temp2) )
            return pd.get_dummies(temp2).sum(level=0)
        elif True :
            dataframe = pd.get_dummies(self.df[column].apply(pd.Series).stack()).sum(level=0)
            #컬럼의 소숫점 네이밍을 제거해 보겠다.
            columns = dataframe.columns
            dictCol = defaultdict( lambda : 0 )
            for k in columns:
                dictCol[str(k)] = str(int(k))
            dataframe.rename(columns=lambda x: int(x), inplace=True)
            return dataframe
        else :
            return pd.get_dummies(self.df[column])

class mod_ds_helper_v2 :
    def __init__(self,  df ):
        print("ver 1.1")
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
    def info_unique(self):
        for col in self.df.columns:
            try :
                print("{}={}".format(col,self.df[col].unique()))
            except:
                continue

    # Categorized
    def cvtWithMap(self,srcCol,tarCol,dicMap):
        self.df[tarCol] = self.df[srcCol].map(dicMap)

    # NLP
    def cvtPunctWord(self,srcCol, tarCol):
        self.df[tarCol] = self.df[srcCol].str.extract(' ([A-Za-z]+)\.', expand=False)

    # Binning
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

    # process NA field
    def fillnaWithMedian(self, colGroup, colTar ):
        self.df[colTar].fillna(self.df.groupby(colGroup)[colTar].transform("median"), inplace=True)

    # Dropping
    def dropColumn(self,tarcol):
        self.df.drop(tarcol,axis=1,inplace=True)

    # JSON field -> List field
    def JsonToList(self,colSrc,colTar,field ):
        self.df[colTar] = self.df[colSrc].fillna('[]').apply(ast.literal_eval).apply(self._JsonToList , field = field)
    def _JsonToList(self,x, field ):
        return [ i[ field  ] for i in x ] if isinstance(x, list) else []
        # json to list with single field

    # Get CntDict from List
    def getCntDictfromList(self, listField):
        cnt_tmp = Counter()
        self.df[listField].apply(cnt_tmp.update)
        return dict( cnt_tmp )

    # Get Dict from JSONList
    def _getDictFromJsonList(self , jsonlist , kfield, vfield ):
        if( isinstance( jsonlist,list) ) :
            for json in jsonlist :
                cur_key = json[kfield]
                cur_val = json[vfield]
                if ( json[ kfield ] not in self._tmp_dict.keys()):
                    self._tmp_dict[ cur_key ] = cur_val
    def getDictFromJsonList(self, jsoncolumn, kfield, vfield ):
        self._tmp_dict = {}
        self.df[jsoncolumn].fillna('[]').apply(ast.literal_eval).apply(self._getDictFromJsonList , kfield = kfield, vfield = vfield )
        return self._tmp_dict

    # Multi Elem List ->  Single Max Elem (with count dictionary)
    def _ListToMaxVal(self, listField , dictCnt ):
        max_key = ""
        if( isinstance( listField,list ) ) :
            for elem in listField :
                if( max_key == "" ) : max_key = elem
                else :
                    if( dictCnt[ elem ] > dictCnt[ max_key] ) : max_key = elem
            return [max_key]
        else :
            return []
    def ListToMaxVal(self, srcCol, tarCol, dictCntMap ):
        self.df[tarCol] = self.df[srcCol].apply(self._ListToMaxVal, dictCnt = dictCntMap )

    # K - Count -> K-Count (same count) : Count
    def cvtDictToValueCounts(self, dicCnt, isSort):
        ddic = defaultdict(lambda: 0)
        for k, v in dicCnt.items():
            int_v = int(v)
            ddic[int_v] = ddic[int_v] + 1
        if (isSort):
            return OrderedDict(sorted(ddic.items()))
        else:
            return ddic
    #


    # -----------------------------------------------------------------------------------

    def _list_to_entry(self,x):
        if (isinstance(x, list)):
            for i in x:
                if( i not in self._tmp_dict.keys() ) :
                    nElem = len( self._tmp_dict )
                    self._tmp_dict[ i ] = nElem
    def get_entryDict_from_listField(self, listField):
        self._tmp_dict = defaultdict(lambda: 0)
        self.df[listField].apply(self._list_to_entry)
        return self._tmp_dict

    def _field_to_entry(self,x):
        if( x not in self._tmp_dict.keys() ) :
            nElem = len( self._tmp_dict )
            self._tmp_dict[ x ] = nElem

    def get_entryDict_from_Field(self,Field):
        self._tmp_dict = defaultdict(lambda: 0)
        self.df[Field].apply(self._field_to_entry)
        return self._tmp_dict

    def _cvtKtoV(self,x):
        if (isinstance(x, list)):
            new_list = []
            for i in x:
                new_list.append( int(self._tmp_dict[i]) )
            return new_list
        return []

    def cvt_klistTovlist(self,srcField,tarField,dicKV):
        self._tmp_dict = dicKV
        self.df[tarField] = self.df[srcField].apply( self._cvtKtoV )



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
        # 소숫점이 되네 ....
        if True :
            temp = self.df[column].apply(pd.Series)
            temp2 = temp.stack()
            #print( "stack ={}".format(temp2) )
            return pd.get_dummies(temp2).sum(level=0)
        elif False :
            dataframe = pd.get_dummies(self.df[column].apply(pd.Series).stack()).sum(level=0)
            #컬럼의 소숫점 네이밍을 제거해 보겠다.
            columns = dataframe.columns
            print( columns )
            dictCol = defaultdict( lambda : 0 )
            for k in columns:
                if( k != "" ) : dictCol[str(k)] = str(int(k))
            dataframe.rename(columns=lambda x: int(x), inplace=True)
            return dataframe
        else :
            return pd.get_dummies(self.df[column])

    def merge_onehotcoding_field(self ,column):
        self.df = pd.merge(left=self.df.reset_index(), right=self.get_onehotcoding_df(column).reset_index(), on="index").set_index("index")
