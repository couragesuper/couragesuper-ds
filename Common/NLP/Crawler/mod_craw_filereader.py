class cTxtReader:
    def __init__(self, corpus_fname, onlySentence, mapform):
        self.corpus_fname = corpus_fname
        self.fobj = open(self.corpus_fname, 'r', encoding='utf-8')
        # read first line
        line = self.fobj.readline()
        listCols = line.replace("\n", "").split("\t")
        # print(listCols)
        self.isSentence = onlySentence
        self.mapform = mapform

    def test(self):
        with open(self.corpus_fname, 'r', encoding='utf-8') as fp:
            for line in fp:
                print(line)

    def test2(self):
        line = self.fobj.readline()
        while (line):
            print(line)
            line = self.fobj.readline()

    def __iter__(self):
        line = self.fobj.readline()
        while (line):
            listLine = line.split("\t")
            if (len(listLine) == 5):
                if (self.isSentence):
                    for i, sent in enumerate(listLine[4].split("  ")):
                        for sent_l2 in sent.split("."):
                            if (sent_l2 != ""): yield sent_l2
                else:
                    # doc
                    yield listLine[4]
            else:
                continue
            line = self.fobj.readline()
