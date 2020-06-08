import sys
from PyQt5.QtWidgets import QApplication
from startPyQT import MyApp

class MyApp2(MyApp):
    def __init__(self , configFileName ):
        super().__init__(configFileName)

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = MyApp2( "config\\UIConfig.xml")
    if( 0 == ex.initUI() ) : sys.exit(app.exec_())
    else : print("initalize framework is error")