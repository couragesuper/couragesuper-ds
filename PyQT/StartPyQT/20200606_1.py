import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction , qApp , QPushButton, QToolTip
from PyQt5.QtGui import QIcon , QFont


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def makeToolbar(self):
        print("----")

    def makeMenuBar(self):
        # Action
        exitAction = QAction(QIcon('image/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

    def makeWindowFrame(self):
        # Positioning
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('image/web.png'))
        self.setGeometry(300, 300, 300, 200)


    def initUI(self):
        # Tooltip
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget</b> widget')

        # PushButton
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.move(50, 50)
        btn.resize(btn.sizeHint())

        self.statusBar()
        self.makeToolbar()

        #
        self.statusBar().showMessage("hello");
        self.show()

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())