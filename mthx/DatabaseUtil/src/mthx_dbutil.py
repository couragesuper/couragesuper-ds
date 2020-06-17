import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QSettings

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem

sys.path.append("../../../Common")
from Mysql.libmysql import dbConMysql

import codecs

form_class = uic.loadUiType("../ui/PoemUtil.ui")[0]

class Model( QStandardItemModel ) :
    def __init__(self, data):
        QStandardItemModel.__init__(self)

        d = data[0]  # Fruit
        item = QStandardItem(d["type"])
        child = QStandardItem(d["objects"][0])  # Apple
        item.appendRow(child)
        child = QStandardItem(d["objects"][1])  # Banana
        item.appendRow(child)
        self.setItem(0, 0, item)

        d = data[1]  # Vegetable
        item = QStandardItem(d["type"])
        child = QStandardItem(d["objects"][0])  # Carrot
        item.appendRow(child)
        child = QStandardItem(d["objects"][1])  # Tomato
        item.appendRow(child)
        self.setItem(1, 0, item)


class Mthx_Poem_DB_Util(QWidget, form_class):

    def __init__(self):
        super().__init__()

        self.initConfig()
        self.setupUi(self)
        self.connectUI()
        self.initTreeView()
        self.initUI()
        self.initDBMgs()
        self.show()

    def initConfig(self):
        self.defaultRevision = 5

    def initDBMgs(self):
        config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
                     'raise_on_warnings': True}
        self.db = dbConMysql(config_db)


    def initUI(self):
        setting = QSettings("mthx" , "poemdbutil")
        self.dir = setting.value("savedir")
        if (self.dir != None): self.editDir.setText(self.dir)
        self.editRev.setText(str(self.defaultRevision))
        self.dir = setting.value("savedir")
        self.chkSaveAndClear.setChecked(True)

    def initTreeView(self):
        data = [
            {"type": "Fruit", "objects": ["Apple", "Banana"]},
            {"type": "Vegetable", "objects": ["Carrot", "Tomato"]},
        ]
        # QTreeView 생성 및 설정
        self.treePoems.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.model = Model(data)
        self.treePoems.setModel(self.model)


    def connectUI(self):
        self.btnSave.clicked.connect(self.slotBtnSave)
        self.btnClear.clicked.connect(self.slotBtnClear)
        self.btnOpen.clicked.connect(self.slotBtnOpen)

    def slotBtnSave(self):
        # get and check datatype
        strIndex = self.editNo.text()
        strTitle = self.editTitle.text()
        strDate = self.editDate.text()
        strRev = self.editRev.text()
        strContent = self.editContent.toPlainText()
        strComment = self.editComment.toPlainText()

        # remove 2 line return chars
        strContent = strContent.replace("\r\n\r\n\r\n" , "\r\n\r\n")
        strContent = strContent.replace("\n\n\n", "\n\n")
        strComment = strComment.replace("\r\n\r\n\r\n", "\r\n\r\n")
        strComment = strComment.replace("\n\n\n", "\n\n")

        # propiling
        print( strIndex.isdigit() )
        print( strRev.isdigit() )
        print( strDate.isdigit() )

        # database query
        # insert Query
        strQueryHead = 'insert \n'\
        'into \n'\
        '`tb_mthx_poem_data` \n'\
        '( \n'\
            '`idx_mthx_poem` \n'\
            ',`title` \n'\
            ',`content` \n' \
            ',`revision` \n'

        if( (strComment != None) ) : strQueryHead += ', `comment` \n'
        if( strDate != None ) : strQueryHead += ', `cdate` \n'

        strQueryMid = ') \n'\
        'VALUES \n'\
        '( \n'

        strQueryValues = strIndex + ', \n'
        strQueryValues += '"' + strTitle + '", \n'
        strQueryValues += '"' + strContent + '", \n'
        strQueryValues += '"' + strRev + '" \n'

        if ((strComment != None)): strQueryValues += ',"' + strComment + '"\n'
        if (strDate != None): strQueryValues += ',' + strDate + '\n'
        strQueryEnd = ');'

        strQuery = strQueryHead + strQueryMid + strQueryValues + strQueryEnd
        print( strQuery )
        isOK = self.db.commitQuery( strQuery )

        # DB OK -> file writing
        print( isOK )
        if( isOK ) :
            # file write
            filename = self.dir + "\\mtxpoem_" + strIndex + "_Rev" + strRev + ".txt"
            f = open(filename, "wt", encoding="utf-8")
            f.write("*no:" + strIndex + "\r\n")
            f.write("*title:" + strTitle + "\r\n")
            f.write("*date:" + strDate + "\r\n")
            f.write("*revision:" + strRev + "\r\n")
            f.write("*content:\r\n" + strContent + "\r\n")
            f.write("*comment:\r\n" + strComment + "\r\n")
            f.close()
            if (self.chkSaveAndClear.isChecked()): self.slotBtnClear()

    def slotBtnClear(self):
        strIndex = self.editNo.clear()
        strTitle = self.editTitle.clear()
        strDate = self.editDate.clear()
        strRev = self.editRev.setText("5")
        strContent = self.editContent.clear()
        strComment = self.editComment.clear()

    # changes save dir
    def slotBtnOpen(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Directory', './')
        self.dir = str(path)
        self.editDir.setText( self.dir )
        setting = QSettings("mthx" , "poemdbutil")
        setting.setValue("savedir" , self.dir )
        setting.sync()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mthx_db_util = Mthx_Poem_DB_Util()
    app.exec_()