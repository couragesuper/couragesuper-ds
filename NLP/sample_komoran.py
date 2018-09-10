import sys
import time
import pprint
sys.path.append("../Common/Crawler")
sys.path.append("../Common/Util")
sys.path.append("../Common/NLP")

from komoran.komoran3py  import Komoran

komoran = Komoran()
komoran.set_user_dictionary('../Data/KomoranDic/user_dictionary.txt')
result = komoran.getTokensList('청하는아이오아이멤버입니다')
pprint.pprint( result )

Sentence = "사냥과 채집을 하던 시절에 공간을 기억하는 능력은 생존과 직결되었다."
result = komoran.getTokensList(Sentence)
pprint.pprint( result )

Sentence = "운동은 신체의 건강 유지는 물론 전두엽이 담당하는 기억과 학습 능력의 향상을 위해서도 매우 중요한 생활 습관이다"
result = komoran.getTokensList(Sentence)
pprint.pprint( result )

Sentence = "빛의자녀들교회는하나님을사랑하는교회입니다."
result = komoran.getTokensList(Sentence)
pprint.pprint( result )

# add new word to library
    # adding 한 단어가 적용되는지를 테스트.
f = open( '../Data/KomoranDic/user_dictionary.txt' ,"a+" , encoding="UTF-8")
f.write("\n%s\t%s" % ("빛의자녀들교회","NNP") )
f.close()

komoran_2 = Komoran()
komoran_2.set_user_dictionary('../Data/KomoranDic/user_dictionary.txt')

Sentence  = "빛의자녀들교회는 우리 교회입니다. "
dicTokens = komoran_2.getTokensList(Sentence)
pprint.pprint( dicTokens )

Sentence  = "VOA는 45개 언어(방송국 2500개)로 2억3680만 시청 및 청취자들에게 라디오·TV·인터넷으로 미국의 정책을 중심에 둔 각종 콘텐트를 제공하고 있다"
dicTokens = komoran_2.getTokensList(Sentence)
pprint.pprint( dicTokens )

dicTokens = komoran_2.getNounList(Sentence)
pprint.pprint( dicTokens )

# pickling test
import pickle

with open("dicTokens.pkl" ,"wb") as f:
    pickle.dump( dicTokens , f )

with open("dicTokens.pkl","rb") as f:
    dicLoad = pickle.load(f)

print( dicLoad )
print( type( dicLoad ))

