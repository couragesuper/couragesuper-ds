import os
import jpype
from .jvm import init_jvm

class Komoran:

    def __init__(self):

        init_jvm()
        package = jpype.JPackage('kr.co.shineware.nlp.komoran.core')
        model_path = os.path.dirname(os.path.realpath(__file__)) + '/models/'
        print( model_path )
        self._komoran = package.Komoran(model_path)

    def set_user_dictionary(self, path):
        """
        Arguments
        ---------
        path : str
            dictionary file path
        """
        self._komoran.setUserDic(path)

    def pos(self, sent):
        
        tokens = self._komoran.analyze(sent).getTokenList()
        #tokens = [(token.getMorph(), token.getPos()) for token in tokens]
        #return tokens
        listRet = []
        nElem = len(tokens)
        for i in range(0,nElem) :
            elem = tokens[i]
            listRet.append( (elem.getMorph(),elem.getPos()))
            #dictToken = { "morph":elem.morph , "pos":elem.pos , "beginIndex":elem.beginIndex, "endIndex":elem.endIndex }
        return listRet;