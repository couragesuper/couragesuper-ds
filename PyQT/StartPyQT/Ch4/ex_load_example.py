import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("QPushButtonDialog.ui")[0]

class MyWindow(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn1.clicked.connect( self.slotBtn1 )
        self.btn2.clicked.connect( self.slotBtn2 )

    def slotBtn1(self):
        QMessageBox.about(self, "message", "clicked")

    def slotBtn2(self):
        QMessageBox.about(self, "message", "clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()