import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QSettings

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem

sys.path.append("../../Common")
from Mysql.libmysql import dbConMysql

# duplicate from poemutil
form_class = uic.loadUiType("PoemUtil.ui")[0]

class Model( QStandardItemModel ) :

    def __init__(self, data):
        self.data = data
        QStandardItemModel.__init__(self)
        # 아이템을 한개씩 만들어서 추가하는 식으로 보임.
        if( False ) :

            d = data[0]  # Fruit
            item = QStandardItem(d["type"])
            child = QStandardItem(d["objects"][0])  # Apple
            item.appendRow(child)
            child = QStandardItem(d["objects"][1])  # Banana
            item.appendRow(child)
            self.setItem(0, 0, item)

            d = data[1]  # Vegetable
            item = QStandardItem(d["type"])
            child = QStandardItem(d["objects"][0])  # Carrot
            item.appendRow(child)
            child = QStandardItem(d["objects"][1])  # Tomato
            item.appendRow(child)
            self.setItem(1, 0, item)
        else :
            rev = 0
            idx = 0
            insertCnt = 0
            childCnt = 0
            item = None
            child = None

            for row in data :
                print( row )
                if( row['idx_mthx_poem'] != idx ) :
                    if( item != None ) :
                        string_name = "{}_{} ({})".format(idx, curtitle , childCnt )
                        item.setText(string_name)
                        item_2 = QStandardItem("{}".format(idx))
                        item_3 = QStandardItem("{}".format(rev))
                        self.setItem(insertCnt, 0, item )
                        insertCnt = insertCnt + 1
                        childCnt = 0
                    string_name = "{}_{}".format(row['idx_mthx_poem'], row['curTitle'])
                    item = QStandardItem(string_name)
                    idx = row['idx_mthx_poem']
                    curtitle = row['curTitle']
                print("2")
                string_name = "{}_{}_rev{}".format(row['idx_mthx_poem'], row['curTitle'], row['revision'] )
                child_1 = QStandardItem( string_name )
                rev = row['revision']
                child_2 = QStandardItem( "{}".format(idx) )
                child_3 = QStandardItem( "{}".format(rev) )
                item.appendRow( [child_1 , child_2, child_3] )
                childCnt = childCnt + 1
    def findQueryData(self, index ):
        for row in self.data :
            print( row )
            if( row['idx_mthx_poem'] == index ) :
                print( "matching row: {}".format(row))
                ret =  {"idx":row['idx_mthx_poem'] , "rev":row['maxrev'] }
                return ret;
        print("not mathced...")
        return {"idx":None , "rev":None}


class Mthx_Poem_DB_Util(QWidget, form_class):

    def __init__(self):
        super().__init__()
        self.initConfig()
        self.setupUi(self)
        self.connectUI()
        self.initDBMgs()
        self.initTreeView()
        self.initUI()
        self.show()

    def initConfig(self):
        self.defaultRevision = 5

    def initDBMgs(self):
        config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
                     'raise_on_warnings': True}
        self.db = dbConMysql(config_db)

    def initUI(self):
        setting = QSettings("mthx" , "poemdbutil")
        self.dir = setting.value("savedir")
        if (self.dir != None): self.editDir.setText(self.dir)
        self.editRev.setText(str(self.defaultRevision))
        self.dir = setting.value("savedir")
        self.chkSaveAndClear.setChecked(True)

    def initTreeView(self):
        # 데이터를 이렇게 만들어야 하는가.
        # QTreeView 생성 및 설정

        queryPoemList = 'select \n'\
        '   idx_mthx_poem,\n'\
        '   revision,\n'\
        '   maxrev,\n'\
        '   title,\n'\
        '   (select\n'\
        '       title from tb_mthx_poem_data as A where A.idx_mthx_poem  = B.idx_mthx_poem and A.revision  = B.revision) as curTitle\n'\
        'from\n'\
        '   (select\n'\
        '       idx_mthx_poem, revision, title, MAX(revision) as maxrev\n'\
        '   from\n'\
        '       tb_mthx_poem_data\n'\
        'group by\n'\
        '   idx_mthx_poem, revision) as B;'\

        QueryRet = self.db.selectQuery( queryPoemList )
        print( "initTree view " )
        print( QueryRet )


        #make header for treeitem
        self.treePoems.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.model = Model( QueryRet )

        if (True) :
            self.model.setHorizontalHeaderLabels( ['title' ,'id' ,'rev'] )

        self.treePoems.setModel(self.model)
        self.treePoems.header().setSectionResizeMode( QHeaderView.ResizeToContents )

    def connectUI(self):
        self.btnSave.clicked.connect(self.slotBtnSave)
        self.btnClear.clicked.connect(self.slotBtnClear)
        self.btnOpen.clicked.connect(self.slotBtnOpen)
        self.treePoems.clicked.connect(self.slotPoemTree)

        #self.treePoems.selectionModel().selectedChanged.connect( self.slotPoemTree )

    def slotBtnSave(self):
        # get and check datatype
        strIndex = self.editNo.text()
        strTitle = self.editTitle.text()
        strDate = self.editDate.text()
        strRev = self.editRev.text()
        strContent = self.editContent.toPlainText()
        strComment = self.editComment.toPlainText()

        # remove 2 line return chars
        strContent = strContent.replace("\r\n\r\n\r\n" , "\r\n\r\n")
        strContent = strContent.replace("\n\n\n", "\n\n")
        strComment = strComment.replace("\r\n\r\n\r\n", "\r\n\r\n")
        strComment = strComment.replace("\n\n\n", "\n\n")

        # propiling
        print( strIndex.isdigit() )
        print( strRev.isdigit() )
        print( strDate.isdigit() )

        # database query
        # insert Query
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

        # DB OK -> file writing
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
        strIndex = self.editNo.clear()
        strTitle = self.editTitle.clear()
        strDate = self.editDate.clear()
        strRev = self.editRev.setText("5")
        strContent = self.editContent.clear()
        strComment = self.editComment.clear()

    # changes save dir1
    def slotBtnOpen(self):
        path = QFileDialog.getExistingDirectory(self, 'Select Directory', './')
        self.dir = str(path)
        self.editDir.setText( self.dir )
        setting = QSettings("mthx" , "poemdbutil")
        setting.setValue("savedir" , self.dir )
        setting.sync()

    def displayPoemWithParentItem( self, index ):
        print( "displayPoemWithParentItem , {}".format( index ) )
        ret = self.model.findQueryData( index )
        query_select = "select * from tb_mthx_poem_data where idx_mthx_poem = {} and revision = {}".format( ret['idx'] , ret['rev'])
        query_ret = self.db.selectQuery( query_select )
        print( query_ret )
        self.editNo.setText( str(query_ret[0]['idx_mthx_poem']) )
        self.editTitle.setText( query_ret[0]['title'] )
        self.editDate.setText( str(query_ret[0]['cdate']) )
        self.editRev.setText( str(query_ret[0]['revision']) )
        self.editContent.setText( query_ret[0]['content'] )
        self.editComment.setText( query_ret[0]['comment'] )

    def displayPoemWithChildItem( self , index , rev):
        query_select = "select * from tb_mthx_poem_data where idx_mthx_poem = {} and revision = {}".format(index,rev)
        query_ret = self.db.selectQuery(query_select)
        print(query_ret)
        self.editNo.setText(str(query_ret[0]['idx_mthx_poem']))
        self.editTitle.setText(query_ret[0]['title'])
        self.editDate.setText(str(query_ret[0]['cdate']))
        self.editRev.setText(str(query_ret[0]['revision']))
        self.editContent.setText(query_ret[0]['content'])
        self.editComment.setText(query_ret[0]['comment'])


    def slotPoemTree(self, index):
        print("\n\nslotPoemTree index{}".format(index))
        print("row:{},col:{},".format(index.row() , index.column() ))
        print( self.treePoems.selectedIndexes()  )

        selectedIndexData = [None,None,None]

        if( True ) :
            cnt = 0
            for ix in self.treePoems.selectedIndexes() :
                selectedIndexData[ cnt ] = ix.data()
                cnt = cnt + 1

        # I dont know why .... like this ?
        if( (selectedIndexData[1] == None) and (selectedIndexData[2] == None) ) :
            print("1111111111111")
            title = selectedIndexData[0]
            targetIdx = int( title.split("_")[0] )
            self.displayPoemWithParentItem( targetIdx )
        elif( (selectedIndexData[1] != None) and (selectedIndexData[2] != None) ) :
            self.displayPoemWithChildItem( int(selectedIndexData[1]) , int(selectedIndexData[2]) )
        else :
            print("3333333333333")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    mthx_db_util = Mthx_Poem_DB_Util()
    app.exec_()