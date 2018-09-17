import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.append("../../Common")
from Visualizer import mod_viz_helper as viz
from DataScience import mod_ds_helper as dp

# movie recommend engine .. codes
    # with simialrity
#https://www.kaggle.com/fabiendaniel/film-recommendation-engine/notebook
    #
#https://www.kaggle.com/sirpunch/exploring-the-movies-dataset/data

df_movie = pd.read_csv( "tmdb_5000_movies.csv" )
df_cred  = pd.read_csv( "tmdb_5000_credits.csv" )

ds_movie = dp.mod_ds_helper(df_movie)
ds_cred  = dp.mod_ds_helper(df_cred)

ds_movie.info()
ds_cred.info()

ds_movie.json_to_list_withField("genres","gen_name","name")
ds_movie.json_to_list_withField("genres","gen_id","id")

if False : # this is works well
    print( ds_movie.df['gen_name'] )
    print( ds_movie.df['gen_id'] )

# extract counter
dicCntGenres = ds_movie.get_cntDict_from_listField("gen_name")
print( "count of Genres = {}".format(dicCntGenres) )

dicGenres = ds_movie.get_kvDict_from_listField("genres","id","name")
print( "dicGenres = {}".format(dicGenres) )

#histogram
listHistColumn = ['budget','popularity','revenue','runtime','vote_average','vote_count']
if False :
    for column in listHistColumn :
        viz.hist_df_column( ds_movie.df , column)
        plt.show()
else :
    viz.hist_df( ds_movie.df , 50 , (20,15) )
    plt.show()

# make company name and company id
    # company id to onehot coding
ds_movie.json_to_list_withField("production_companies","company_name","name")
ds_movie.json_to_list_withField("production_companies","company_id","id")

dicCntComp = ds_movie.get_cntDict_from_listField("company_name")
print( dicCntComp )
print( "len of cntCmop = {} , {}".format( len (dicCntComp), dicCntComp ))

ds_movie.set_listfield_maxvalue_withDict( "company_name" , "company_maxcnt_name" , dicCntComp )
print( ds_movie.df['company_maxcnt_name'] )

dicCountry = ds_movie.get_kvDict_from_listField("production_countries","iso_3166_1","name" )
print( dicCountry )

# one hot coding
df = ds_movie.get_onehotcoding_df( 'company_maxcnt_name' )
print( df )
if False :
    df.to_csv("company_name.csv")

viz.scattermatrix( ds_movie.df, listHistColumn, (12,8) )
plt.show()




