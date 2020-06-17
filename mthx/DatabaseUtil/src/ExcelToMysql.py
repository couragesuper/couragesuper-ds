import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QSettings

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem
from PyQt5.QtGui import *


import openpyxl

sys.path.append("../../../Common")
from Mysql.libmysql import dbConMysql

form_class = uic.loadUiType("../ui/DLG_ExcelToDB.ui")[0]

class Dialog_ExcelToMysql(QWidget, form_class):

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
        print("Dialog_ExcelToMysql::initUI")
        self.setLayout( self.mainLayout )
        self.mainLayout.setContentsMargins(16,16,16,16)
        if( False ) :
            resource_path ="../res/icon_backup.png"
            pixmap = QtGui.QPixmap( ":/{}".format( resource_path ))
            icon = QtGui.QIcon( pixmap )
            self.setWindowIconText( icon )

    def initTreeView(self):
        print("Dialog_ExcelToMysql::initTreeView")

    def connectUI(self):
        print("Dialog_ExcelToMysql::connectUI")
        self.btnSelect.clicked.connect(self.slotBtnSelect)
        self.btnInput.clicked.connect(self.slotBtnInput)

    def slotBtnInput(self):
        print("Dialog_ExcelToMysql::slotBtnInput")

    def slotBtnSelect(self):
        print("Dialog_ExcelToMysql::slotBtnSelect")
        filename = QFileDialog.getOpenFileName(self, 'Select Directory', '*.xlsx')
        self.filepath = str(filename[0])
        self.txtFilePath.setText(self.filepath)
        print( "selected file:{}".format( self.filepath ) )
        self.sheetList = []
        wb = openpyxl.load_workbook(self.filepath)
        for i in wb.get_sheet_names():
            self.sheetList.append(i)
            self.cmbExcelSheets.addItem( i )
        print( self.sheetList )
        # TO do combo box and sheet selector


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_ExcelToMysql = Dialog_ExcelToMysql()
    app.exec_()
