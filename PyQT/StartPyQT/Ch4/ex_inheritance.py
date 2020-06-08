#inheritance QMainWindow

import sys
from PyQt5.QtWidgets import *
from common_main import MyApp
from ex_load_example import MyWindow

class MyApp2(MyApp):
    def __init__(self , configFileName ):
        super().__init__(configFileName)

    def connectUI(self):
        self.mapActions['VLX'].triggered.connect(self.slotVLX)

    def slotVLX(self):
        print("----")
        QMessageBox.about(self, "message", "clicked")
        self.dialog = MyWindow()
        self.dialog.show()

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = MyApp2( "config\\UIConfig.xml")
    if( 0 == ex.initUI() ) : sys.exit(app.exec_())
    else : print("initalize framework is error")

