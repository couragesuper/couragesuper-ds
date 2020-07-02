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
from Mysql.libExcelToMysql import ExcelToMysql

form_class = uic.loadUiType("../ui/DLG_ExcelToDB.ui")[0]


class Dialog_ExcelToMysql(QWidget, form_class):

    def __init__(self):
        super().__init__()
        self.initConfig()
        self.setupUi(self)
        self.connectUI()
        self.initTreeView()
        self.initUI()
        #self.initDBMgs()
        self.show()

    def initConfig(self):
        self.defaultRevision = 5

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
        self.btnConvert.clicked.connect(self.slotBtnConvert)

    def slotBtnInput(self):
        print("Dialog_ExcelToMysql::slotBtnInput")
        try :
            text = self.cmbExcelSheets.currentText()
            self.excel2Mysql.setSheetName(text)
            self.excel2Mysql.makeDbSchema()
            self.excel2Mysql.createDbSchema()
            self.excel2Mysql.pushDbData()
        except Exception as e:
            print("{}".format(e))

    def slotBtnConvert(self):
        print("slotBtnConvert")

    def slotBtnSelect(self):
        filename = QFileDialog.getOpenFileName(self, 'Select Directory', '*.xlsx')
        self.filepath = str(filename[0])
        self.txtFilePath.setText(self.filepath)
        if False : # raw code not using excel to mysql wrapper
            print("Dialog_ExcelToMysql::slotBtnSelect")

            print( "selected file:{}".format( self.filepath ) )
            self.sheetList = []
            wb = openpyxl.load_workbook(self.filepath)
            for i in wb.get_sheet_names():
                self.sheetList.append(i)
                self.cmbExcelSheets.addItem( i )
            print( self.sheetList )
            # TO do combo box and sheet selector
        else :
            self.excel2Mysql = ExcelToMysql( self.filepath )
            self.excel2Mysql.initDB()
            self.excel2Mysql.getSheetNames()
            for  elem in self.excel2Mysql.sheetList  :
                self.cmbExcelSheets.addItem(elem)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui_ExcelToMysql = Dialog_ExcelToMysql()
    app.exec_()
