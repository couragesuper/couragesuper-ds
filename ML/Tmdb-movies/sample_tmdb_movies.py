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

# 1. Load CSV
df_movie = pd.read_csv( "tmdb_5000_movies.csv" )
df_cred  = pd.read_csv( "tmdb_5000_credits.csv" )

ds_movie = dp.mod_ds_helper(df_movie)
ds_cred  = dp.mod_ds_helper(df_cred)

# 2. Show Information
ds_movie.info()
ds_cred.info()

# processing JSON Field
# 3. convert json field to list [Genres]
ds_movie.json_to_list_withField("genres","gen_name","name")
ds_movie.json_to_list_withField("genres","gen_id","id")

if False : # checked
    print( ds_movie.df['gen_name'] )
    print( ds_movie.df['gen_id'] )

# 4. make counter dictionary
dicCntGenres = ds_movie.get_cntDict_from_listField("gen_name")
print( "count of Genres = {}".format(dicCntGenres) )

# 5. make K-v dictionary
dicGenres = ds_movie.get_kvDict_from_listField("genres","id","name")
print( "dicGenres = {}".format(dicGenres) )

# 6. Visualization
listHistColumn = ['budget','popularity','revenue','runtime','vote_average','vote_count']
if False :
    for column in listHistColumn :
        viz.hist_df_column( ds_movie.df , column)
        plt.show()
elif False :
    viz.hist_df( ds_movie.df , 50 , (20,15) )
    plt.show()

# processing JSON Field
# 7. convert json field to list [companry]

#json -> name list -> maxcnt_name ,
ds_movie.json_to_list_withField("production_companies","company_name","name")
ds_movie.json_to_list_withField("production_companies","company_id","id")

dicCntComp = ds_movie.get_cntDict_from_listField("company_name")
print( dicCntComp )
print( "len of cntCmop = {} , {}".format( len (dicCntComp), dicCntComp ))

# 회사의 값 중에서, 메이저 회사를 따르기 위해서, 그러니까 4803개가 된다.
ds_movie.set_listfield_maxvalue_withDict( "company_name" , "company_maxcnt_name" , dicCntComp )
print( ds_movie.df['company_maxcnt_name'] )

dicCountry = ds_movie.get_kvDict_from_listField("production_countries","iso_3166_1","name" )
print( dicCountry )

#OrderedDict([(1, 3545), (2, 630), (3, 240), (4, 142), (5, 94), (6, 55), (7, 57), (8, 37), (9, 29), (10, 25), (11, 12), (12, 33), (13, 15), (14, 9), (15, 5), (16, 10),
#  (17, 5), (18, 2), (19, 3), (20, 3), (21, 1), (22, 5), (23, 2), (24, 2), (25, 1), (26, 2), (27, 1), (28, 1), (29, 3), (30, 1), (31, 1), (32, 2), (33, 1), (34, 5), (36, 4),
# (37, 1), (38, 2), (39, 1), (40, 2), (41, 1), (42, 1), (49, 1), (52, 1), (53, 1), (54, 1), (55, 2), (56, 1), (59, 1), (64, 1), (69, 1), (75, 2), (79, 1), (81, 1), (94, 1),
#  (96, 1), (102, 1), (114, 1), (118, 1), (122, 1), (165, 1), (201, 1), (222, 1), (285, 1), (311, 1), (319, 1)])

# 319부터, Named 회사라고 생각하였다.
# 4808개 회사 중에 319개로 갈수록 누적되는 비율을 보아서, 적당한 구간을 자르고 싶다.
# 그런데 아직은 아이디어가 없다. ~~ @_@

# bokeh로 확축소가 되는 그래프를 그릴 수 없을까?



dicOrderedComp = ds_movie.get_cntDicItem(dicCntComp,True)

print( dicOrderedComp )

exit(0)

# one hot coding
df = ds_movie.get_onehotcoding_df( 'company_maxcnt_name' )
print( df )
if False :
    df.to_csv("company_name.csv")

if False :
    viz.scattermatrix( ds_movie.df, listHistColumn, (12,8) )
    plt.show()

if True :
    print( ds_movie.df.index )
    ds_filtered = ds_movie.df[ ds_movie.df.budget > 3.800000e+08  ]
    print( ds_filtered )

# drop intermediate columns
ds_movie.dropColumn( 'genres' )
ds_movie.dropColumn( 'gen_name' )
ds_movie.dropColumn( 'gen_id' )
ds_movie.dropColumn( 'company_name' )
ds_movie.dropColumn( 'company_id' )
ds_movie.dropColumn( 'homepage' )




