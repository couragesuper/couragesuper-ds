class LTokenizer:
    
    def __init__(self, scores=None, default_score=0.0):
        self.scores = scores if scores else {}
        self.ds = default_score
        
    def tokenize(self, sentence, tolerance=0.0, flatten=True, remove_r=False):
        tokens = [self._eojeol_to_lr(token, tolerance) for token in sentence.split()]        
        if remove_r:
            tokens = [token[0] for token in tokens]        
        if (flatten) and (remove_r == False):
            tokens = [subtoken for token in tokens for subtoken in token if subtoken]        
        return tokens
    
    def _eojeol_to_lr(self, token, tolerance=0.0):
        n = len(token)
        if n <= 2:
            return (token, '')
        
        candidates = [(token[:e], token[e:]) for e in range(2, n + 1)]
        candidates = [(self.scores.get(t[0], self.ds), t[0], t[1]) for t in candidates]
        
        if tolerance > 0:
            max_score = max([c[0] for c in candidates])
            candidates = [c for c in candidates if (max_score - c[0]) <= tolerance]
            best = sorted(candidates, key=lambda x:len(x[1]), reverse=True)[0]
        else:
            best = sorted(candidates, key=lambda x:(x[0], len(x[1])), reverse=True)[0]
            
        return (best[1], best[2])