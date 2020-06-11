import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QSettings

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import Qt

sys.path.append("../../Common")
from Mysql.libmysql import dbConMysql

# duplicate from poemutil
form_class = uic.loadUiType("ThanksDiary.ui")[0]

class Mthx_Thanks_Diary(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setLayout( self.mainLayout ) # this makes attaching layout to main window
        self.connectUI()
        self.initDBMgs()
        self.show()
    def connectUI(self):
        self.btnSave.clicked.connect(self.slotBtnSave)
        self.btnClear.clicked.connect(self.slotBtnClear)
    def initDBMgs(self):
        config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible','raise_on_warnings': True}
        self.db = dbConMysql(config_db)
    #slots
    def slotBtnSave(self):
        strDate = self.txtDate.text()
        strTitle = self.txtTitle.text()
        strComment = self.txtComment.toPlainText()
        strCategory = self.txtCategory.text()
        strWeight = self.txtWeight.text()

        query_insert = 'INSERT '\
        'INTO '\
        'bible.tb_mthx_thanks_diary( '\
        '`date` '\
        ', title '\
        ', comment '\
        ', category ' \
        ', weight ' \
        ')'\
        'VALUES('\
        ',{}'\
        ',"{}"'\
        ',"{}"'\
        ',"{}"' \
        ',{}' \
        ')'.format(strDate, strTitle, strComment, strCategory, strWeight )
        print("slotBtnSave")
        ret = self.db.commitQuery( query_insert )
        print(" save data result : {}".format( query_insert ))
        self.slotBtnClear()
    def slotBtnClear(self):
        self.txtDate.clear()
        self.txtTitle.clear()
        self.txtComment.clear()
        self.txtCategory.clear()
        self.txtWeight.clear()
        print( "slotBtnClear" )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = Mthx_Thanks_Diary()
    app.exec_()
