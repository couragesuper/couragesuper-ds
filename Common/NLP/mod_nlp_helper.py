import os
import sys
import pandas as pd
import numpy as np


# 점진적인 접근이 필요하다.
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

isTest = False
if isTest :
    nlp_helper = mod_nlp_helper()


