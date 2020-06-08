import sys
# for checking whether path is exist
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction , qApp , QPushButton, QToolTip, QDesktopWidget
from PyQt5.QtGui import QIcon , QFont
from PyQt5.QtCore import Qt, QDate

# for XML
from xml.etree import ElementTree as ET

class MyApp(QMainWindow):
    def __init__(self , configFileName ):
        super().__init__()
        # check file is exist.
        self.configFileName = configFileName

    def makeMenuAndToolBar(self):
        # Action
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        self.mapActions = {}
        self.mapMenuItem = {}
        self.mapToolbar = {}

        if( False ) :
            exitAction = QAction(QIcon('image/exit.png'), 'Exit', self)
            exitAction.setShortcut('Ctrl+Q')
            exitAction.setStatusTip('Exit application')
            exitAction.triggered.connect(qApp.quit)

            filemenu = menubar.addMenu('&File')
            filemenu.addAction(exitAction)
        else :
            xmltree = ET.parse( self.configFileName )
            # access top xml node
            xmlroot = xmltree.getroot()
            if (xmlroot == None):
                print("[Error] SQT Configuration file doesn't have not root.")
                return 1
            #print("---")
            for menus in xmlroot:
                # Menus
                nameMenus = menus.attrib['name']
                self.mapMenuItem[ nameMenus ] = menubar.addMenu( nameMenus )
                self.mapToolbar[nameMenus] = self.addToolBar(nameMenus)
                #print("{}".format(menus.attrib))
                for menu in menus:
                    #make action & add menus
                    nameMenu = menu.attrib['name']
                    self.mapActions[ nameMenu ] = QAction(QIcon( "image\\" + menu.attrib['resource'] ), menu.attrib['name_short'], self)
                    self.mapActions[ nameMenu ].setShortcut( menu.attrib['shortcut'] )
                    self.mapActions[ nameMenu ].setStatusTip( menu.attrib['desc'])
                    self.mapMenuItem[nameMenus].addAction( self.mapActions[ nameMenu ] )
                    #add toolbar
                    self.mapToolbar[nameMenus].addAction( self.mapActions[ nameMenu ] )
                    #print("\t{}".format(menu.attrib))
    def makeWindowFrame(self):
        # Positioning
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('image/web.png'))
        self.setGeometry(300, 300, 800, 600)
        self.centerWindow()

    def centerWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def showStatusBar(self):
        self.statusBar()
        self.date = QDate.currentDate()
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))

    def connectUI(self):
        print("connectUI")

    def initUI(self):
        if ( Path( self.configFileName ).exists() == False ) :
            print("[Error] Configuration File isn't exists")
            return 1

        # Tooltip
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        # PushButton
        if( False ) :
            btn = QPushButton('Button', self)
            btn.setToolTip('This is a <b>QPushButton</b> widget')
            btn.move(50, 50)
            btn.resize(btn.sizeHint())

        self.makeMenuAndToolBar()
        self.makeWindowFrame()
        self.showStatusBar()
        self.connectUI()

        self.show()
        return 0


class MyApp2(MyApp):
    def __init__(self , configFileName ):
        super().__init__(configFileName)


if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = MyApp2( "config\\UIConfig.xml")
    if( 0 == ex.initUI() ) : sys.exit(app.exec_())
    else : print("initalize framework is error")