import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import sklearn.datasets

#for ml
from sklearn.model_selection import train_test_split

def get_iris_df() :
    global ds
    ds = sklearn.datasets.load_iris()
    df_iris = pd.DataFrame( ds['data'] , columns = ds['feature_names'] )
    code_species_map = dict(zip(range(3),ds['target_names']))
    df_iris['species'] = [code_species_map[c] for c in ds['target']]
    return df_iris

#Draw scatter with columns x columns

def DrawScatterMatrix( df , binsval , szval ) :
    pd.plotting.scatter_matrix( df,  figsize=(15, 15), marker='o', hist_kwds={"bins": binsval}, s=szval, alpha=0.8)

if True :
    #load iris data
    df_iris = get_iris_df()

    for key in ds.keys() :
        print( "{0}={1}".format( key, ds[key] ) )
    print( "data shape" , ds['data'].shape )

    #split train data
    X_train, X_test, y_train, y_test = train_test_split( ds['data'] , ds['target'] , random_state = 0 )
    print( y_train )
    # Visualization Helper
    #1.scatter_matrix
    df_iris_train = pd.DataFrame( X_train , columns = ds['feature_names'])

if False :
    pd.plotting.scatter_matrix( df_iris_train , c = y_train , figsize = (15,15) , marker='o' , hist_kwds={"bins" : 20 }, s = 60, alpha = 0.8 ) # target을 넣으면, ROW별로 색깔을 줄수가 있다.
    #DrawScatterMatrix( df_iris_train , 20, 10 )
    # 2.PieChart
elif False :

    #draw pie graph
    df_sum = df_iris.groupby('species').sum()
    var = df_sum.columns[0]
    df_sum[ var ].plot(kind='pie', fontsize = 20)
    plt.title("categorized with " + var, fontsize=25)
    plt.ylabel( var, horizontalalignment ='left')
    plt.show()
elif False :

    #draw pie graph with subplot
    graph_kind = 'pie'
    df_sum = df_iris.groupby('species').sum()
    #df_sum.plot(kind= graph_kind , fontsize=10 , figsize=(15,15) , subplots = True, layout=(2,2) , legend=False , autopct='%.2f')
    df_sum.plot(kind=graph_kind, fontsize=10, figsize=(15, 15), subplots=True, layout=(2, 2), legend=False )
    plt.title("measurement by species" , fontsize=5)
    plt.show()
elif False :

    #draw bar graph
    df_sum = df_iris.groupby('species').sum()
    if True :
        df_sum.plot(kind="bar", fontsize=10, figsize=(15, 15), subplots=True, layout=(2, 2) , rot = 30)
    else :
        df_sum.plot.bar()
    plt.show()
elif False  :

    #make time data
    ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    ts = ts.cumsum()
    ts.plot()
    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
    df = df.cumsum()
    plt.figure()
    df.plot()
    plt.show()
elif False :
    df = pd.DataFrame(np.random.rand(10, 5), columns=['A', 'B', 'C', 'D', 'E'])
    df.plot.box()
    plt.show()
elif False :
    #draw histogram with iris dataframe
    if True :
        print( df_iris.columns )
        print( df_iris['species'].unique() )
        #df_iris.plot(kind="hist", subplots=True, layout=(2,2), figsize=(16,8) , bins = 50)

        #plt.figure()
        df_iris[ df_iris['species'] == 'setosa' ].plot(kind="hist", subplots=True, figsize=(16,8) , bins = 50)
        #plt.figure()
        df_iris[df_iris['species'] == 'versicolor'].plot(kind="hist", subplots=True, figsize=(16,8) , bins = 50)
        #plt.figure()
        df_iris[df_iris['species'] == 'virginica'].plot(kind="hist", subplots=True, figsize=(16,8) , bins = 50)
        # batch를 해야 비교가 되지 .. 배치의 기술은 연마가 필요하다.
    else :
        df_iris[ df_iris.columns[0] ].plot(kind="hist", subplots=True, bins = len( df_iris.index )  )
    plt.show()
elif False :
    for column in df_iris.columns:
        if( column != 'species') :
            plt.figure()
            for spec in df_iris['species'].unique() :
                forspec = df_iris[df_iris['species'] == spec]
                forspec[ column ].plot( kind = 'hist' , alpha = 0.4, label= spec, bins = 20 )
                plt.title( column )
            plt.legend( loc = 'upper right' )
    plt.show()
elif False :
    # box plot
    col = df_iris.columns[0]
    df_iris['ind'] = pd.Series( df_iris.index ).apply( lambda i :i % 50)
    df_iris.pivot( 'ind', 'species')[col].plot(kind='box')
    plt.title(  )
    plt.show()
elif False :
    print( df_iris[df_iris.columns[0]].corr(df_iris[df_iris.columns[1]]) )
    print( df_iris[df_iris.columns[0]].corr(df_iris[df_iris.columns[1]], method='pearson') )
    print( df_iris[df_iris.columns[0]].corr(df_iris[df_iris.columns[1]],method='spearman') )
    print( df_iris[df_iris.columns[0]].corr(df_iris[df_iris.columns[1]],method='spearman') )
elif True :
    import statsmodels.api as sm
    dta = sm.datasets.co2.load_pandas()
    dta.plot()
    plt.title("density of sugar")
    plt.ylabel('PPM')
    plt.show()



