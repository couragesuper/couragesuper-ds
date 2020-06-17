import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QSettings

from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem

sys.path.append("../../../Common")
from Mysql.libmysql import dbConMysql

# duplicate from poemutil
form_class = uic.loadUiType("../ui/PoemUtil.ui")[0]

# Model clss for TreeView
class Model( QStandardItemModel ) :
    def __init__(self, data):
        QStandardItemModel.__init__(self)
        self.data = data
        self.makeItems()

    def makeItems(self) :
        # 아이템을 한개씩 만들어서 추가하는 식으로 보임.
        item = None
        rev = 0
        cur_poem_idx = 0
        cur_poem_title = ""
        self.inserted_cnt = 0
        childCnt = 0

        for row in self.data:
            print("{}, poem_idx{} , idx:{}".format( row , row['idx_mthx_poem'] , cur_poem_idx ))
            # changing of index (new poem)
            if (row['idx_mthx_poem'] != cur_poem_idx):
                cur_poem_idx = row['idx_mthx_poem']
                cur_poem_title = row['curTitle']
                string_name = "{}_{}".format(cur_poem_idx, cur_poem_title)
                item = QStandardItem(string_name)
                childCnt = 0
                self.setItem(self.inserted_cnt, 0, item)
                self.inserted_cnt = self.inserted_cnt + 1
                print( "setItem CntItem:{} {}".format(self.inserted_cnt, cur_poem_title))
                # string_name = "{}_{} ({})".format(cur_poem_idx, curtitle, childCnt)
                # item.setText(string_name)

            # add child-item
            rev = row['revision']
            string_child_name = "{}_{}_rev{}".format(row['idx_mthx_poem'], row['curTitle'], rev )
            child_1 = QStandardItem(string_child_name)
            child_2 = QStandardItem("{}".format(cur_poem_idx))
            child_3 = QStandardItem("{}".format(rev))
            item.appendRow([child_1, child_2, child_3])
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

        self.query_ret = None

        self.initConfig()
        self.setupUi(self)
        self.setLayout( self.mainHLayout ) # this makes attaching layout to main window

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

        if( self.query_ret == None ) :
            print("[Info] insert new data ")
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
        else :
            print("[Info] Update Data ")

            strIndex = self.editNo.text()
            strTitle = self.editTitle.text()
            strDate = self.editDate.text()
            strRev = self.editRev.text()
            strContent = self.editContent.toPlainText()
            strComment = self.editComment.toPlainText()

            isChangedIndex = False
            isChangedTitle = False
            isChangedDate = False
            isChangedRev = False
            isChangedContent = False
            isChangedComment = False

            print(self.query_ret)

            if ( int(strIndex) != self.query_ret[0]['idx_mthx_poem'] ) : isChangedIndex = True;
            if ( strTitle != self.query_ret[0]['title']): isChangedTitle = True;
            if ( strDate != self.query_ret[0]['cdate']): isChangedDate = True;
            if ( int(strRev) != self.query_ret[0]['revision']): isChangedRev = True;
            if ( strContent != self.query_ret[0]['content']): isChangedContent = True;
            if ( strComment != self.query_ret[0]['comment']): isChangedComment = True;
            if ( isChangedRev or isChangedIndex ) :
                print("[Error] Update Data ... Changing Revision is wrong case ")
            else :
                if( isChangedContent == True ) :
                    print( "[INFO] work to do" )
                else :
                    print( "[INFO] update database")
                    query_stat_update = 'UPDATE \n' \
                    ' bible.tb_mthx_poem_data \n' \
                    'SET  \n' \
                    ' title = "{}"  \n' \
                    ', comment = "{}"  \n' \
                    ', cdate = "{}"  \n' \
                    'WHERE  \n' \
                    ' idx_mthx_poem = {}   \n' \
                    '  AND \n' \
                    ' revision = {}   \n'.format( strTitle , strComment, strDate , int(strIndex) , int(strRev))
                    print("we try to update database with query \n {} ".format( query_stat_update ))
                    self.db.commitQuery( query_stat_update )
            #self.UpdateTreeView()

    def UpdateTreeView(self):
        print("update tree view")

    def slotBtnClear(self):
        try :
            print("1")
            strIndex = self.editNo.clear()
            strTitle = self.editTitle.clear()
            strDate = self.editDate.clear()
            strRev = self.editRev.setText("5")
            strContent = self.editContent.clear()
            strComment = self.editComment.clear()
            print("2")
            if ( None != self.query_ret ) :
                self.query_ret = None
            print("3")
        except Exception as  e :
            print('except {}'.format(e))


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
        self.query_ret = self.db.selectQuery( query_select )
        print( self.query_ret )
        self.editNo.setText( str(self.query_ret[0]['idx_mthx_poem']) )
        self.editTitle.setText( self.query_ret[0]['title'] )

        dateobj = self.query_ret[0]['cdate']
        strDate = "%4d" % dateobj.year + "%02d" % dateobj.month + "%02d" % dateobj.day
        self.editDate.setText( strDate )
        self.editRev.setText( str(self.query_ret[0]['revision']) )
        self.editContent.setText( self.query_ret[0]['content'] )
        self.editComment.setText( self.query_ret[0]['comment'] )

    def displayPoemWithChildItem( self , index , rev):
        query_select = "select * from tb_mthx_poem_data where idx_mthx_poem = {} and revision = {}".format(index,rev)
        self.query_ret = self.db.selectQuery(query_select)
        print( self.query_ret )
        self.editNo.setText(str(self.query_ret[0]['idx_mthx_poem']))
        self.editTitle.setText(self.query_ret[0]['title'])

        dateobj = self.query_ret[0]['cdate']
        strDate = "%4d" % dateobj.year + "%02d" % dateobj.month + "%02d" % dateobj.day
        self.editDate.setText(strDate)
        self.editRev.setText(str(self.query_ret[0]['revision']))
        self.editContent.setText(self.query_ret[0]['content'])
        self.editComment.setText(self.query_ret[0]['comment'])

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
            title = selectedIndexData[0]
            targetIdx = int( title.split("_")[0] )
            self.displayPoemWithParentItem( targetIdx )
        elif( (selectedIndexData[1] != None) and (selectedIndexData[2] != None) ) :
            self.displayPoemWithChildItem( int(selectedIndexData[1]) , int(selectedIndexData[2]) )
        else :
            print("Error")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    mthx_db_util = Mthx_Poem_DB_Util()
    app.exec_()