import sklearn.datasets as dataset
import pandas as pd



listDS = []
listDS.append(  dataset.load_boston() )
listDS.append(  dataset.load_breast_cancer() )

listName = [ "boston", "cancer" ]
listDataFrame = []

if False :
    print( boston.feature_names )
    print( boston.target )
    print( type(boston) )
    print( boston.keys() )
    print( boston.DESCR )

for i, elem in enumerate( listDS ) :
    print( elem.DESCR )
    listDataFrame.append( pd.DataFrame( data = elem.data  , columns = elem.feature_names ) )
    listDataFrame[i]['target'] = elem.target
    print( listDataFrame[i].info() )
    listDataFrame[i].to_csv( "Data/sklearn/" + listName[i] + ".csv" , encoding="UTF-8" )








