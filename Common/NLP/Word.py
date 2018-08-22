from collections import defaultdict
import sys
import numpy as np

from TxtReader import TxtReader_Dir

class CohesionProbability_Dir:
    
    def __init__(self, dirpath, max_l_length=10):
        self.max_l_length = max_l_length
        self.dirpath = dirpath
        self.L = {}
        
    def train_old(self, sents):
        for num_sent, sent in enumerate(sents):
            if num_sent % 5000 == 0:
                sys.stdout.write('\rinserting %d sents... ' % num_sent)
            for token in sent.split():
                for e in range(1, min(self.max_l_length, len(token)) + 1):
                    subword = token[:e]
                    self.L[subword] = self.L.get(subword,0) + 1
        print('\rinserting subwords into L: done')
        print('num subword = %d' % len(self.L))
    
    def train(self):
        
        
        for num_sent, sent in enumerate(sents):
            if num_sent % 5000 == 0:
                sys.stdout.write('\rinserting %d sents... ' % num_sent)
            for token in sent.split():
                for e in range(1, min(self.max_l_length, len(token)) + 1):
                    subword = token[:e]
                    self.L[subword] = self.L.get(subword,0) + 1
        print('\rinserting subwords into L: done')
        print('num subword = %d' % len(self.L))
    
    def get_cohesion(self, word):

        # 글자가 아니거나 공백, 혹은 희귀한 단어인 경우
        if (not word) or ((word in self.L) == False): 
            return 0.0

        if len(word) == 1:
            return 1.0

        word_freq = self.L.get(word, 0)
        base_freq = self.L.get(word[:1], 0)

        if base_freq == 0:
            return 0.0
        else:
            return np.power((word_freq / base_freq), 1 / (len(word) - 1))
        
    def make_cohesion_score(self,word ) : 
        cohesion_score = {}
        for word, count in self.L.items():
            if count < 10 or len(word) < 2:
                continue
            cohesion_score[word] = get_cohesion(word)
        return cohesion_score