import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QSettings

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import Qt

sys.path.append("../../../Common")
from Mysql.libmysql import dbConMysql

# utility for manager poem database
# duplicate from poemutil
form_class = uic.loadUiType("../ui/Mthx_DatabaseUtil.ui")[0]
release_version ="20200722"

class LogModel ( QStandardItemModel ) :
    def __init__(self):
        QStandardItemModel.__init__(self)

    def addLog(self , strLevel, strCate, strMessage ):
        cntRow = self.rowCount()
        item1 = QStandardItem(str(int(cntRow)))
        item2 = QStandardItem(strLevel)
        item3 = QStandardItem(strCate)
        item4 = QStandardItem(strMessage)
        self.setItem(cntRow, 0, item1)
        self.setItem(cntRow, 1, item2)
        self.setItem(cntRow, 2, item3)
        self.setItem(cntRow, 3, item4)

class Mthx_Database_Manager(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setLayout(self.mainLayout)  # this makes attaching layout to main window
        self.connectUI()
        self.show()

    def initDBMgs(self):
        config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible','raise_on_warnings': True}
        self.db = dbConMysql(config_db)
        if( self.db != None ) : self.addLog("I" , "DB" ,"Init OK")
        else : self.addLog("E" , "DB" ,"Init Fail")

        # widgets
    #cmbDBFunc
    #btnSelDBFunc
    #txtSrc1
    #btnSelSrc1
    #txtSrc2
    #btnSelSrc2
    #txtSrc3
    #btnSelTar
    #btnRun
    #tabViewLog
    #btnEnd

    def slotEnd(self):
        print("slotEnd")

    def slotSelDBFunc(self):
        print("slotDBFunc")

    def slotSelSrc1(self):
        print("slotDBFunc")

    def slotSelSrc2(self):
        print("slotDBFunc")

    def slotSelTarget(self):
        print("slotDBFunc")

    def connectUI(self):
        self.btnEnd.clicked.connect(self.slotEnd)
        self.btnSelDBFunc.clicked.connect(self.slotSelDBFunc)
        self.btnSelSrc1.clicked.connect(self.slotSelSrc1)
        self.btnSelSrc2.clicked.connect(self.slotSelSrc2)
        self.btnSelTar.clicked.connect(self.slotSelTarget)

if __name__ == "__main__":
    print("starting application..1")
    app = QApplication(sys.argv)
    mthx_db_util = Mthx_Database_Manager()
    app.exec_()
    print("starting application..2")

