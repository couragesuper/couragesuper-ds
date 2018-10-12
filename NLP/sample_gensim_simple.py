import nltk
from gensim.models.word2vec import Word2Vec
import string

# downloading .. nltk
nltk.download('stopwords')
stop_words = set(nltk.corpus.stopwords.words('english'))

# loading txt contents
with open('./data/news.txt','rt') as f:
    text = f.read()
translator = str.maketrans('', '', string.punctuation)

# each.translate(translator) == 특수문자 제거
# x.lower() == 소문자화
# if x.lower() not in stop_words == 불용어제거
clean = [[x.lower() for x in each.translate(translator).split() if x.lower() not in stop_words] for each in text.split('.\n')]

# alloc word2vec
model = Word2Vec(clean,window = 5,min_count=2,sg=1,iter=10000)

list_vocakeys = list(model.wv.vocab.keys())
len = model.wv.vocab

ret =  model.wv.most_similar("attack")
print( ret )
