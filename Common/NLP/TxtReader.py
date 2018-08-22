import os
import sys

# 점진적인 접근이 필요하다.
# Sentences List를 한번에 받아내자, 메모리가 서버에서 터졌다. 

class TxtReader:    
    def __init__(self, corpus_fname, iter_sent = False):
        self.corpus_fname = corpus_fname
        self.iter_sent = iter_sent
        self.sent_length = 0
        self.doc_length = 0        
    def __iter__(self):
        with open(self.corpus_fname, encoding='utf-8') as f:
            for doc_idx, doc in enumerate(f):
                if not self.iter_sent:
                    yield doc
                    continue
                for sent in doc.split('  '):                    
                    sent = sent.strip()
                    if not sent: continue
                    yield sent
                    
    def __len__(self):
            if self.iter_sent:
                if self.sent_length == 0:
                    with open(self.corpus_fname, encoding='utf-8') as f:
                        for doc in f:
                            self.sent_length += len(doc.strip().split('  '))
                return self.sent_length
            else:
                if self.doc_length == 0:
                    with open(self.corpus_fname, encoding='utf-8') as f:
                        for num_doc, doc in enumerate(f):
                            continue
                        self.doc_length = (num_doc + 1)
                return self.doc_length
    
    def getSents(self):
        sents = []
        with open(self.corpus_fname, encoding='utf-8') as f:
            for doc_idx, doc in enumerate(f):                
                for sent in doc.split('  '):                    
                    sent = sent.strip()
                    if not sent: continue
                    else : sents.append( sent )
        return sents
    
class TxtReader_Dir:    
    def __init__(self, dirpath, iter_sent = False):
        self.dirpath = dirpath
        self.iter_sent = iter_sent
        self.sent_length = 0
        self.doc_length = 0        
    def __iter__(self):        
        if( os._exists('c:/sdf') ) :
            listdir = os.listdir( self.dirpath )
            listdir = [ file for file in listdir if file.lower().find('.txt') != -1 ]
            for filename in listdir :                
                with open( filename , encoding='utf-8') as f:
                    for doc_idx, doc in enumerate(f):
                        if not self.iter_sent:
                            yield doc
                            continue
                        for sent in doc.split('  '):                    
                            sent = sent.strip()
                            if not sent: continue
                            yield sent            
    def __len__(self):
            if self.iter_sent:
                if self.sent_length == 0:
                    if( os._exists(self.dirpath) ):
                        listdir = os.listdir( self.dirpath )
                        for filename in listdir : 
                            with open(filename, encoding='utf-8') as f:
                                for doc in f:
                                    self.sent_length += len(doc.strip().split('  '))
                return self.sent_length
            else:
                if self.doc_length == 0:
                    if( os._exists(self.dirpath) ):
                        listdir = os.listdir( self.dirpath )
                        for filename in listdir : 
                            with open(self.corpus_fname, encoding='utf-8') as f:
                                for num_doc, doc in enumerate(f):
                                    continue
                                self.doc_length = (num_doc + 1)
                return self.doc_length       