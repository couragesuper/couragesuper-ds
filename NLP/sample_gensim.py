import gensim
print('Gensim version = {}'.format(gensim.__version__))
import soynlp
import pprint

#유사한 단어를 찾아낼 수 있다.

relative_path = "../Data/NLP_LEC/"

corpus_fname           = relative_path + 'comments_172movies//merged_comments.txt'
tokenized_corpus_fname = relative_path + 'comments_172movies/merged_comments_tokenized.txt'

TRAIN_WORD2VEC = False
word2vec_fname = relative_path + 'comments_172movies/movie_review_word2vec_model_v3.4.pkl'

TRAIN_DOC2VEC = False
doc2vec_fname  = relative_path + 'comments_172movies/movie_review_doc2vec_model_v3.4.pkl'

id2movie_fname = relative_path + 'comments_172movies/id2movie.pkl'
id2actor_fname = relative_path + 'comments_172movies/id2actor.pkl'

def get_text(fname, debug=True):
    with open(fname, encoding='utf-8') as f:
        docs = []
        for i, doc in enumerate(f):
            if debug and i >= 1000:
                break
            docs.append(doc.split('\t'))

    idx, texts, scores = zip(*docs)
    return idx, texts, scores


idx, docs, scores = get_text(tokenized_corpus_fname)
print( docs[:5] )

import os

class CommentWord2Vec:

    def __init__(self, fname):
        self.fname = fname
        if not os.path.exists(fname):
            print('File not found: %s' % fname)

    def __iter__(self):
        with open(self.fname, encoding='utf-8') as f:
            for doc in f:
                movie_idx, text, score = doc.split('\t')
                yield text.split()


word2vec_corpus = CommentWord2Vec(tokenized_corpus_fname)

for num_doc, doc in enumerate(word2vec_corpus):
    if num_doc > 5: break
    print(doc)

from gensim.models import Word2Vec
import pickle

if TRAIN_WORD2VEC:
    word2vec_model = Word2Vec(
        word2vec_corpus,
        size=100,
        alpha=0.025,
        window=5,
        min_count=5,
        workers=3,
        sg=0,
        negative=5)
    with open(word2vec_fname, 'wb') as f:
        pickle.dump(word2vec_model, f)

else:
    with open(word2vec_fname, 'rb') as f:
        word2vec_model = pickle.load(f)

pprint.pprint(  word2vec_model.wv.most_similar('영화', topn=30) )


