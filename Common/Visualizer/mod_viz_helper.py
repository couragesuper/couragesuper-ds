import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import seaborn as sns
sns.set() # setting seaborn default for plots

from pandas.plotting import scatter_matrix

# function bar_chart
    # dataframe
    # column to compare
    # target
def bar_chart(df,col,target,class_index, listClass ):
    listValCnt = [df[df[target]==elem][col].value_counts() for elem in listClass]
    df = pd.DataFrame(listValCnt)
    df.index = class_index
    df.plot(kind='bar',stacked=True, figsize=(10,5),title=col)

def bar_chart_withDict(df, col, colTar, dict_class):
    listClass = []
    listValue = []
    for k,v in dict_class.items() :
        listClass.append(k)
        listValue.append(v)
    listValCnt = [df[df[colTar]==elem][col].value_counts() for elem in listValue]
    df = pd.DataFrame(listValCnt)
    df.index = listClass
    df.plot(kind='bar',stacked=True, figsize=(10,5),title=col)

def sns_facegrid( df, col, hue, min, max ) :
    facet = sns.FacetGrid(df, hue=hue, aspect=4)
    facet.map(sns.kdeplot, col, shade=True)
    facet.set(xlim=(min,max))
    facet.add_legend()

def hist_df_column( df, col ) :
    plt.title(col)
    df[col].hist(bins=df[col].nunique())

def hist_df( df , n_bin , sz = (20,15)) :
    df.hist(bins=n_bin , figsize = sz)

def corrHeatMat( df ):
    num_cols = list( df.select_dtypes( exclude=['object']).columns )
    corr = df[num_cols].corr()
    mask = np.zeros_like(corr,dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f,ax = plt.subplots(figsize=(12,9))
    cmap = sns.diverging_palette(220,10,as_cmap=True)
    sns.heatmap( corr, mask=mask, cmap=cmap, vmax=1., vmin=-1., center=0, square=True, linewidths=.5, cbar_kws={"shrink":.5} , annot=True, fmt="0.2f")
    plt.show()

def scattermatrix ( df , columns , sz):
    scatter_matrix( df[columns] , figsize = sz)

def pltshow() :
    plt.show()
