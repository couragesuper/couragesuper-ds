import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QSettings

sys.path.append("../../Common")
from Mysql.libmysql import dbConMysql

import codecs

form_class = uic.loadUiType("PoemUtil.ui")[0]

class MyWindow(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnSave.clicked.connect( self.slotBtnSave )
        self.btnClear.clicked.connect( self.slotBtnClear )
        self.btnOpen.clicked.connect( self.slotBtnOpen )
        setting = QSettings("myorg" , "dbutil")
        self.dir = setting.value("savedir")
        if( self.dir != None ) : self.editDir.setText( self.dir )

        self.editRev.setText('5')
        self.chkSaveAndClear.setChecked(True)

    def createDatabase(self):
        config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
                     'raise_on_warnings': True}
        self.db = dbConMysql(config_db)
        # implement whether db is ok

    def slotBtnSave(self):

        strIndex = self.editNo.text()
        strTitle = self.editTitle.text()
        strDate = self.editDate.text()
        strRev = self.editRev.text()
        strContent = self.editContent.toPlainText()
        strComment = self.editComment.toPlainText()

        strContent = strContent.replace("\r\n\r\n\r\n" , "\r\n\r\n")
        strContent = strContent.replace("\n\n\n", "\n\n")

        strComment = strComment.replace("\r\n\r\n\r\n", "\r\n\r\n")
        strComment = strComment.replace("\n\n\n", "\n\n")

        print( strIndex.isdigit() )
        print( strRev.isdigit() )
        print( strDate.isdigit() )

        # database query

        strQueryHead = 'insert \n'\
        'into \n'\
        '`tb_mthx_poem_data` \n'\
        '( \n'\
            '`idx_mthx_poem` \n'\
            ',`title` \n'\
            ',`content` \n' \
            ',`revision` \n'

        if( (strComment != None) ) : strQueryHead += ', `comment` \n'
        if( strDate != None ) : strQueryHead += ', `cdate` \n'

        strQueryMid = ') \n'\
        'VALUES \n'\
        '( \n'

        #strQueryValues = '2, \n'\  '"사랑이 진리이어서", \n'\ '"사랑이 진리입니다.", \n'\ '"코멘트", \n'\ '4 \n'

        strQueryValues = strIndex + ', \n'
        strQueryValues += '"' + strTitle + '", \n'
        strQueryValues += '"' + strContent + '", \n'
        strQueryValues += '"' + strRev + '" \n'

        if ((strComment != None)): strQueryValues += ',"' + strComment + '"\n'
        if (strDate != None): strQueryValues += ',' + strDate + '\n'
        strQueryEnd = ');'

        strQuery = strQueryHead + strQueryMid + strQueryValues + strQueryEnd
        print( strQuery )
        isOK = self.db.commitQuery( strQuery )

        print( isOK )
        if( isOK ) :
            # file write
            filename = self.dir + "\\mtxpoem_" + strIndex + "_Rev" + strRev + ".txt"
            f = open(filename, "wt", encoding="utf-8")
            f.write("*no:" + strIndex + "\r\n")
            f.write("*title:" + strTitle + "\r\n")
            f.write("*date:" + strDate + "\r\n")
            f.write("*revision:" + strRev + "\r\n")
            f.write("*content:\r\n" + strContent + "\r\n")
            f.write("*comment:\r\n" + strComment + "\r\n")
            f.close()
            if (self.chkSaveAndClear.isChecked()): self.slotBtnClear()

    def slotBtnClear(self):
        print("clear button")
        strIndex = self.editNo.clear()
        strTitle = self.editTitle.clear()
        strDate = self.editDate.clear()
        strRev = self.editRev.setText("5")
        strContent = self.editContent.clear()
        strComment = self.editComment.clear()

    def slotBtnOpen(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Directory', './')
        self.dir = str(path)
        print( self.dir )
        self.editDir.setText( self.dir )
        setting = QSettings("myorg" , "dbutil")
        setting.setValue("savedir" , self.dir )
        setting.sync()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    print("44")
    myWindow.createDatabase()
    print("55")
    myWindow.show()
    app.exec_()