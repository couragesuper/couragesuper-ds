import sys
import time
import pprint
sys.path.append("../Common/Crawler")
sys.path.append("../Common/Util")
sys.path.append("../Common/NLP")

from komoran.komoran3py  import Komoran
from mod_crawler_base import craw_file_reader as txt_reader
from mod_crawler_base import craw_history_logger as logger

#1.komoran test
komoran = Komoran()
komoran.set_user_dictionary('../Data/KomoranDic/user_dictionary.txt')

result = komoran.getTokensList('청하는아이오아이멤버입니다')
pprint.pprint( result )class

#2.txt_reader
#iterate with column
    # handle to writecolumn
txtreader = txt_reader("../Data/Text/Joins/Sasul.txt", False )
list_words = []
for i,doc in enumerate( txtreader ):
    #if( i == 10 ) : break
    if False :
        print( doc.split("\t")[0])
        print( doc.split("\t")[1])
        print( doc.split("\t")[2])
        print( doc.split("\t")[3])
        print( doc.split("\t")[4])
        doc_text = doc.split("\t")[4]
        pprint.pprint( doc_text.split(".") )
    else :
        doc_text  = doc.split("\t")[4]
        list_Sent = doc_text.split(".")
        for i,sents in enumerate( list_Sent ):
            try :
                if( sents != "" ) :
                    for words in komoran.getNounList( sents ) :
                        list_words.append(words)
            except :
                print( "except with = {}",sents )
print( list_words )


from collections import Counter
counter = Counter(list_words )
print( counter)






