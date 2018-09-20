import sys
import time
import pprint
import pickle
sys.path.append("../Common/Crawler")
sys.path.append("../Common/Util")
sys.path.append("../Common/NLP")

from mod_crawler_base import craw_file_reader as txt_reader
from mod_nlp_helper   import mod_nlp_helper as nlp_helper
from soynlp.word      import WordExtractor

# sample for preprocessing
#   1. read txtfile
#   2. word extractor
#   3. make pickle
#   4. load pickle
#   5. convert dict to excel
#   6. crop    data from excel

isSave = False

if isSave :
    txtreader = txt_reader("../Data/Text/Joins/Sasul.txt", False )
    list_words = []
    list_sents = []
    #선택적 한계가 생길 것이다.
    for i,doc in enumerate( txtreader ):
        doc_text = doc.split("\t")[4]
        # splits with sentences
        sents = doc_text.split('.')
        for sent in sents:
            list_sents.append( sent )

    print( "length of list_sents = {}",len(list_sents))
    word_extractor = WordExtractor(
        min_count=100,
        min_cohesion_forward = 0.05,
        min_right_branching_entropy = 0.0)
    word_extractor.train(list_sents) # list of str or like
    words = word_extractor.extract()
    with open("words.pkl" ,"wb") as f:
        pickle.dump( words , f )
else :
    # 통계적인 방법은 반복수가 많아야 하는 기법이다.
    print("Load")
    with open("words.pkl" ,"rb") as f:
        words_dic = pickle.load( f )
    print( type( words_dic) )
    nlphelper = nlp_helper()
    nlphelper.cvtWordDicToExcel( words_dic, "output" )







