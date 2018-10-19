import os
import sys
import pandas as pd
import numpy as np

sys.path.append( "../Mysql" )
from libmysql import dbConMysql

# Sentences List를 한번에 받아내자, 메모리가 서버에서 터졌다.
class mod_nlp_helper:
    def __init__(self  ):
        self.name = "mod_nlp_helper"
    def _makeWordsColumn(self, words):
        listColumns = []
        listColumns.append('word')
        for elem in list(words.values())[0]._fields:
            listColumns.append(elem)
        return listColumns
    def cvtWordDicToExcel(self, dictWords , excelName ):
        # make column
        listColumn = self._makeWordsColumn(dictWords)
        index      = 0
        listDatas  = []
        isFirst = True
        # make dict to list
        for key, val in dictWords.items():
            # if( index > 10 ) : break
            index = index + 1
            listDatas.append(key)
            for elem in val:
                listDatas.append(elem)
        nparr = np.array(listDatas)
        nparr = nparr.reshape(int(len(listDatas) / 9), 9)
        # make pandas
        df = pd.DataFrame(data=nparr, columns=listColumn)
        for i in range(1, len(df.columns)):
            df[df.columns[i]] = df[df.columns[i]].astype(float)
        # write excel file
        writer = pd.ExcelWriter(excelName + '.xlsx')
        df.to_excel(writer, "sheet1")
        writer.save()

print("[loaded][nlp_helper_loader]....")



class komoHelper :
    def __init__ ( self ) :
        self.config =  {
          'user': 'root',
          'password': 'karisma*3%7*4',
          'host': 'mthx.cafe24.com',
          'database': 'chatbot',
          'raise_on_warnings': True
        }
        self.db = dbConMysql( self.config )
    def AddNewWord(self , word , morph ):
        # insert into tKomoDict (word,morph)values( "안녕","NNG")
        query = "insert into tKomoDict (word,morph)values( '%s','%s')" % (word,morph)
        self.db.commitQuery( query )
    def GetKomoList(self):
        qry = "select * from tKomoDict;"
        return self.db.selectQuery(qry)
    def UpdateTextFile(self , filePathName ):
        import codecs
        fo = codecs.open( filePathName , "w", "utf-8")
        listRet = self.GetKomoList()
        for word in listRet:
            fo.write("%s	%s\n" % (word['word'], word['morph']))
        fo.close()

if True :
    komohelper = komoHelper()
    if False :
        komohelper.AddNewWord("빛의자녀들교회","NNP")
        komohelper.AddNewWord("빛의자녀교회","NNP")
        komohelper.AddNewWord("아이오아이","NNP")
        komohelper.AddNewWord("빛자녀교회", "NNP")
        komohelper.AddNewWord("대학연합교회", "NNP")
        komohelper.AddNewWord("안녕", "NNG")
    if False :
        print( komohelper.GetKomoList() )
    if True :
        komohelper.UpdateTextFile("komo.txt")

if False :
    nlp_helper = mod_nlp_helper()


