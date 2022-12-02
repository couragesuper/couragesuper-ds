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

form_class = uic.loadUiType("StartUIPyQT.ui")[0]

# >> Network Configuration
    #txtTestorIP
    #txtTestorPort
    #btnConnect

# >> Connection Information
    #lblConnStatus
    #txtConnInfo

# >> UDS Communication
    #txtUDSCommand
    #btnUDSSend

class UIPyQT(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setLayout(self.mainLayout)  # this makes attaching layout to main window
        self.mainLayout.setContentsMargins(16, 16, 16, 16)
        self.connectUI()
        self.show()

    def connectUI(self):
        self.btnConnect.clicked.connect(self.slotConnect)

    # slot for event
    def slotConnect(  self ):
        print("[Event] btnConnect > slotConnect ")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    pyqt = UIPyQT( )
    app.exec_()

