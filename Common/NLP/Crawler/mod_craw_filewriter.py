class crawler_filewriter :
    def __init__(self, fileName ):
        self.fobj = open( fileName , "a+", encoding='utf-8')
    def close(self):
        self.fobj.close()
    def setFeatures(self, listFeat ):
        self.listFeat = listFeat
        for feat in listFeat :
            self.fobj.write( feat )
            self.fobj.write( "\t")
        self.fobj.write("\n")
    def write(self, entry):
        self.fobj.write(entry)
        self.fobj.write("\t")
    def writeLast(self, entry):
        self.fobj.write(entry)
        self.fobj.write("\n")