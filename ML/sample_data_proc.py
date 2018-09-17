import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.path.append("../Common")
from Visualizer import mod_viz_helper as viz
from DataScience import mod_ds_helper as dp

data_root = "Data\\"

train = pd.read_csv(data_root + 'train.csv')
test  = pd.read_csv(data_root + 'test.csv')

isChecker = False;
ds_train = dp.mod_ds_helper(train)
ds_test = dp.mod_ds_helper(test)

def part_checker() :
    if isChecker :
        input()
    print("\n\n")

# 1. print info
ds_train.info()
ds_test.info()
list_columns = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp','Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']

# Target vs Column : Bar Stack
target_column = 'Survived'
dict_class = { 'Dead':0,'Survived':1 }
dict_pclass = { '1st class':1 , '2nd class':2, '3rd class':3 }
list_compare = ['Sex','Pclass','SibSp','Parch','Embarked']

mapTitle = {'Mr':0,'Miss':1,'Mrs':2,'Master':3,'Dr':3,'Rev':3,'Col':3,'Major':3,'Mlle':3,'Lady':3,'Ms':3,'Sir':3,'Capt':3,'Countess':3,'Mme':3,'Don':3,'Jonkheer':3,'Dona':3}
mapSex = {"male":0, "female":1}
mapEmbarked = {"S":0, "C":1 ,"Q":2}
mapCabin = {"A": 0, "B": 0.4, "C": 0.8, "D": 1.2, "E": 1.6, "F": 2, "G": 2.4, "T": 2.8}

mapFamily = {1: 0, 2: 0.4, 3: 0.8, 4: 1.2, 5: 1.6, 6: 2, 7: 2.4, 8: 2.8, 9: 3.2, 10: 3.6, 11: 4}


if False :
    for index in list_compare :
        viz.bar_chart_withDict(ds_train.df, index, target_column, dict_class)

# Feature Engineering
    # 1.Name to Title
ds_train.cvtPunctWord("Name","Title")
ds_test.cvtPunctWord("Name","Title")

ds_train.cvtWithMap( 'Title', 'Title',mapTitle  )
ds_test.cvtWithMap( 'Title', 'Title',mapTitle )

ds_train.dropColumn('Name')
ds_test.dropColumn('Name')

print( train['Title'].value_counts() )

if False : #ok
    viz.bar_chart_withDict(ds_train.df, 'Title', target_column, dict_class)
    plt.show()
    input()

    # Sex
ds_train.cvtWithMap('Sex','Sex',mapSex)
ds_test.cvtWithMap('Sex','Sex',mapSex)

if False : #ok
    viz.bar_chart_withDict(ds_train.df, 'Sex', target_column, dict_class)
    plt.show()
    input()

    # Age
ds_train.fillnaWithMedian( 'Title' , 'Age' )
ds_test.fillnaWithMedian( 'Title' , 'Age' )

listAgeBinning = [16,26,36,62]
ds_train.binning( 'Age', listAgeBinning )
ds_test.binning(  'Age', listAgeBinning )

print( ds_train.df['Age'])
print( ds_train.df['Age'].value_counts() )

if False : #ok
    viz.bar_chart_withDict(ds_train.df, 'Age', target_column, dict_class)
    plt.show()
    input()


    # Embarked
if False :
    viz.bar_chart_withDict(ds_train.df, 'Embarked', 'Pclass', dict_pclass)
    plt.show()
    input()

ds_train.df['Embarked'].fillna('S',inplace=True)
ds_test.df['Embarked'].fillna('S',inplace=True)

ds_train.cvtWithMap('Embarked','Embarked',mapEmbarked)
ds_test.cvtWithMap('Embarked','Embarked',mapEmbarked)

    # Fare .. median with Pclass
ds_train.fillnaWithMedian( 'Pclass' , 'Fare' )
ds_test.fillnaWithMedian( 'Pclass' , 'Fare' )

listFareBinning = [17,30,100]
ds_train.binning( 'Fare', listFareBinning )
ds_test.binning( 'Fare', listFareBinning )

ds_train.df['Cabin'] = ds_train.df['Cabin'].str[:1]
ds_test.df['Cabin'] = ds_test.df['Cabin'].str[:1]

if False :
    viz.bar_chart_withDict(ds_train.df, 'Cabin', 'Pclass', dict_pclass)
    plt.show()
    input()

    # Cabin
ds_train.cvtWithMap('Cabin','Cabin',mapCabin)
ds_test.cvtWithMap('Cabin','Cabin',mapCabin)

ds_train.fillnaWithMedian( 'Pclass' , 'Cabin' )
ds_test.fillnaWithMedian( 'Pclass' , 'Cabin' )

    # Family Size
ds_train.df['FamilySize'] = ds_train.df['SibSp'] + ds_train.df['Parch'] + 1
ds_test.df['FamilySize'] = ds_test.df['SibSp'] + ds_test.df['Parch'] + 1

if False:
    viz.sns_facegrid (ds_train.df, 'FamilySize', 'Survived',0,ds_train.df['FamilySize'].max())
    plt.show()

ds_train.cvtWithMap('FamilySize','FamilySize',mapFamily)
ds_test.cvtWithMap('FamilySize','FamilySize',mapFamily)

# drop the columns

ds_train.dropColumn( "Ticket" )
ds_test.dropColumn( "Ticket" )

ds_train.dropColumn( "SibSp" )
ds_test.dropColumn( "SibSp" )

ds_train.dropColumn( "Parch" )
ds_test.dropColumn( "Parch" )

ds_train.dropColumn( "PassengerId" )

df_train_data = ds_train.df.drop('Survived', axis = 1)
target = ds_train.df['Survived']

# this is satisfied
viz.corrHeatMat( ds_train.df )

# Modeling
# Importing Classifier Modules
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

import numpy as np


#machine learning
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
k_fold = KFold(n_splits=10, shuffle=True, random_state=0)

clf = KNeighborsClassifier(n_neighbors = 13)
scoring = 'accuracy'
score = cross_val_score(clf, df_train_data , target, cv=k_fold, n_jobs=1, scoring=scoring)
print(score)
print( round(np.mean(score)*100, 2) )

clf = DecisionTreeClassifier()
scoring = 'accuracy'
score = cross_val_score(clf, df_train_data, target, cv=k_fold, n_jobs=1, scoring=scoring)
print(score)
print( round(np.mean(score)*100, 2) )

clf = RandomForestClassifier(n_estimators=13)
scoring = 'accuracy'
score = cross_val_score(clf, df_train_data, target, cv=k_fold, n_jobs=1, scoring=scoring)
print(score)
print( round(np.mean(score)*100, 2) )

clf = GaussianNB()
scoring = 'accuracy'
score = cross_val_score(clf, df_train_data, target, cv=k_fold, n_jobs=1, scoring=scoring)
print(score)
print( round(np.mean(score)*100, 2) )

clf = SVC()
scoring = 'accuracy'
score = cross_val_score(clf, df_train_data, target, cv=k_fold, n_jobs=1, scoring=scoring)
print(score)
print( round(np.mean(score)*100, 2) )

#prediction

clf = SVC()
clf.fit( df_train_data , target )

test_data = ds_test.df.drop("PassengerId" , axis = 1 ).copy()
prediction = clf.predict( test_data )

submission = pd.DataFrame({"PassengerId":ds_test.df['PassengerId'], 'Survived':prediction})
submission.to_csv("sub.csv", index = False )

submission_reload = pd.read_csv("sub.csv")
print( submission_reload )

