#dataframe
import pandas as pd
import ast
import numpy as np
from collections import Counter
from collections import defaultdict
from collections import OrderedDict

#visualzier
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
sns.set()  # setting seaborn default for plots

from pandas.plotting import scatter_matrix

class DsFeatureEngineering :

    # Construcutor
    def __init__(self ):
        print("DsFeatureEngineering is created")
        self.isReady = False

    # Data Frame
    def ShowInfoDF(self , df ):
        print("[Information of DataFrame]\n[Dimensional]={0}".format( df.shape))
        for col in df.columns:
            print("\t[{0}]\tType:{1}\tnUni:{2}\tnNull:{3} ".format(col, df[col].dtype, df[col].nunique(), df[col].isnull().sum(axis=0) ))
            if( df[col].dtype != np.object ) :
                print( df[col].describe() )

    def MakeDescTemplateDF( self , df , csv_name : str ):
        listColumn = ["name", "content", "datatype", "convert DataType", "feature", "idea", "nUnique", "Unique" ,  "nNull"]
        listData = []
        for col in df.columns:
            entry = {'name': col, "content": "", "datatype":  df[col].dtype, "feature": "", "idea": "", "nNull": df[col].isnull().sum(axis=0)}
            entry[ "nUnique" ] = df[col].nunique()
            if( entry[ "nUnique" ] < 30 ) : entry[ 'Unique' ] = df[col].unique()
            else : entry[ 'Unique' ] = "number is over 30"
            listData.append( entry )
        df_report = pd.DataFrame( columns = listColumn, data = listData)
        if(  csv_name.lower().find(".csv") == False ) :
            csv_name =  csv_name + ".csv"
        df_report.to_csv( csv_name , encoding = "UTF-8", index = False)

    # Bar Chart
    def bar_chart_withDict(self , df, col, colTar, dict_class):
        listClass = []
        listValue = []
        for k, v in dict_class.items():
            listClass.append(k)
            listValue.append(v)
        listValCnt = [df[df[colTar] == elem][col].value_counts() for elem in listValue]
        df_viz = pd.DataFrame(listValCnt)
        df_viz.index = listClass
        df_viz.plot(kind='bar', stacked=True, figsize=(10, 5), title=col)

    #Binning / Converting Numerical Value to Categorical Variable
    def binning(self , df , column, listTargets ):
        prevVal = 0
        for i,value in enumerate( listTargets ) :
            if( i == 0 ) :
                df.loc [ df[column] <= value , column] = i
            elif ( i == (len(listTargets)-1) ) :
                df.loc[(df[column] > prevVal) & (df[column] <= value), column] = i
                df.loc [ df[column] > value , column] = i + 1
            else :
                df.loc[ (df[column] > prevVal) & (df[column] <= value) , column] = i
            prevVal = value
        return df[column]

df = pd.read_csv( "train.csv" )
fe =  DsFeatureEngineering( )
dict_class = { 'Dead':0,'Survived':1 }

#check shape of df
if False :
    fe.ShowInfoDF( df )

#check null . datatype , unique elements
if False :
    fe.MakeDescTemplateDF( df , "DataDescription.csv")

#Bar chart
if False :
    list_compare = ['Sex','Pclass','SibSp','Parch','Embarked']
    for idx in list_compare :
        fe.bar_chart_withDict( df ,idx , "Survived" , dict_class )
    plt.show()

#Feature Engineering
    #Name->NameTitleLabel
        #Extract Pattern
print(  df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False).value_counts() )
# 여기서 키 값을 반영하려면, 누적값을 알아야 한다.
dictNameLabel = {'Mr':0,'Miss':1,'Mrs':2,'Master':3,'Dr':3,'Rev':3,'Col':3,'Major':3,'Mlle':3,'Lady':3,'Ms':3,'Sir':3,'Capt':3,'Countess':3,'Mme':3,'Don':3,'Jonkheer':3,'Dona':3 }
df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
df['Title_L'] = df['Title'].map( dictNameLabel )

if False :
    fe.bar_chart_withDict( df ,"Title_L" , "Survived" , dict_class )
    plt.show()


    #Labeling Sex
dictSex = { 'male':0  ,'female':1 }
df['Sex_L'] = df['Sex'].map(dictSex)

if False :
    fe.bar_chart_withDict( df ,"Sex_L" , "Survived" , dict_class ) # 바램은 레전드에 Text출력하는 것
    plt.show()

    # Age (Binning
print( "1:null count of Age" , df["Age"].isnull().sum(axis=0) )
df["Age"]  = df["Age"].fillna(df.groupby("Title_L")["Age"].transform("median"))
print( "2:null count of Age" , df["Age"].isnull().sum(axis=0) )

#범위 값을 구획화 하는 것을 Binning이라고 한다.
#이것을 결정하기 위해서는 Visualzier를 이용한 분석이 필요하며, 두 그래프의 교차점을 주로 사용하는 듯 하다.

listAgeBinning = [16,26,36,62]
df['Age_L'] = fe.binning( df, "Age" , listAgeBinning ).astype('int32')
print( df['Age_L'])

# PClass 와 Embark 사이의 연관관계를 보기
print( df['Embarked'].value_counts() )
df['Embarked'].fillna('S' , inplace = True)

dictEmbark = { 'S':0 , 'C':1, 'Q':2 }
df['Embarked_L'] = df['Embarked'].map(dictEmbark )
