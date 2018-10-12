import sys
import json
sys.path.append("../Common")
from libmysql import dbConMysql

class modelChatbot :     
    def __init__(self) :
        self.config_bible = {
          'user': 'root',
          'password': 'karisma*3%7*4',
          'host': 'mthx.cafe24.com',
          'database': 'bible',
          'raise_on_warnings': True,
        }
        self.config_bot = {
          'user': 'root',
          'password': 'karisma*3%7*4',
          'host': 'mthx.cafe24.com',
          'database': 'chatbot',
          'raise_on_warnings': True,
        }
        self.dbBible = dbConMysql( self.config_bible )
        self.dbBot   = dbConMysql( self.config_bot )
        
    def isExistUsr(self,usrID) :
        query = "select * from tUserChatState where userkey = '%s'" % (usrID)
        ret = self.dbBot.selectQuery( query )
        if( len(ret) > 0 ): return True
        else:  return False
        
    def addUser(self,usrID) :
        qry = "insert into tUserChatState(userkey,statel1,statel2,statel3 ) values ('%s',0,0,0);" % (usrID);        
        ret = self.dbBot.commitQuery( qry )
        
    def updateUserStat(self,usrID,stat1,stat2,stat3):
        qry = "update tUserChatState set statel1 = %d, statel2 = %d, statel3 = %d where userkey = '%s'" % (stat1,stat2,stat3,usrID);
        print(qry)
        ret = self.dbBot.commitQuery( qry )
        
    def getUserStat(self,usrID):
        qry = "select * from tUserChatState where userkey='%s';" % (usrID);
        return self.dbBot.selectQuery( qry )    
    
    def addUserJSON(self,usrID) :
        qry = "insert into tUserChatStatJson(userkey,jsondata ) values (\"%s\",\"{'mode':'기본메뉴'}\");" % (usrID);        
        ret = self.dbBot.commitQuery( qry )
    
    def isExistUsrJSON(self,usrID) :
        qry = "SELECT userkey, jsondata FROM tUserChatStatJson WHERE userkey = '%s';" % (usrID)
        ret = self.dbBot.selectQuery( qry )
        if( len(ret) > 0 ): return True
        else : return False 
        
    def getUserJSON(self,usrID) :
        qry = "SELECT userkey, jsondata FROM tUserChatStatJson WHERE userkey= '%s';" % (usrID)
        ret = self.dbBot.selectQuery( qry )
        return ret[ 0 ]
    
    def updateUserStateJSON( self, usrID, szJsonData ):
        try : 
            qry = "UPDATE tUserChatStatJson SET jsondata = '%s' WHERE userkey = '%s'"  % ( szJsonData, usrID )        
            print( qry )
            self.dbBot.commitQuery( qry )        
        except:
            print( qry )
    
    def searchBibleKey( self, key ) :
        qry = "SELECT "\
            " (SELECT BOOK_KOR_SUMNM FROM TB_BIBLE_BOOK WHERE BOOK_SEQNO = A.BOOK_SEQNO) AS BOOK_SUMNM, "\
            " BOOK_SEQNO, "\
            " BOOK_CHAP_NO, "\
            " BOOK_NO, "\
            " BOOK_CONTENT "\
            " from TB_BIBLE_BOOK_DATA A WHERE BIBLE_SEQNO in (3,4) and BOOK_CONTENT like '%%%s%%'" % (key)
        ret = self.dbBible.selectQuery( qry )
        szOutput =""
        if( len(ret) > 0 ) :                            
            prev_book_seq = ret[0]['BOOK_SEQNO']
            for row in ret :
                #szOutput += "(%s:%d:%d) %s\n" % (row['BOOK_SUMNM'],row['BOOK_CHAP_NO'],row['BOOK_NO'],row['BOOK_CONTENT'])            
                szOutput += "(%s:%d:%d) \n" % (row['BOOK_SUMNM'],row['BOOK_CHAP_NO'],row['BOOK_NO'])            
                if( prev_book_seq != row['BOOK_SEQNO'] ) : szOutput += "\n"
                prev_book_seq = row['BOOK_SEQNO']
            return {"ret":"ok", "msg":szOutput}
        else :                
            return {"ret":"fail", "msg":"없는 키워드인데유"}
        
    def searchBible(self, retParse ):                
        print( retParse.keys() )
        booknm = retParse['book']
        qry = "SELECT BOOK_SEQNO FROM TB_BIBLE_BOOK WHERE BOOK_KOR_SUMNM = '%s'" % (booknm);        
        ret = self.dbBible.selectQuery( qry )        
        
        bookseq = ret[0]['BOOK_SEQNO']        
        qry = "SELECT * from TB_BIBLE_BOOK_DATA WHERE BOOK_SEQNO = %d and BIBLE_SEQNO in (3,4)" % (bookseq)     
        
        if( 'chap' in retParse.keys() ) :
            qry += " and BOOK_CHAP_NO = %d " % (retParse['chap'])
            
        if ( ('no_start' in retParse.keys()) and  ('no_end' in retParse.keys()) ) :
            qry += " and BOOK_NO >= %d and BOOK_NO <= %d " % ( (retParse['no_start']) , (retParse['no_end']) )
        elif ( ('no_start' in retParse.keys()) and  ('isDash' in retParse.keys()) ) :
            qry += " and BOOK_NO >= %d " % ( retParse['no_start'] )
        elif ( ('no_start' in retParse.keys()) ) :
            qry += " and BOOK_NO = %d " % ( retParse['no_start'] )
        
        print(qry)            
        ret = self.dbBible.selectQuery( qry )
        
        szOutput = ""
        if( len(ret) > 0 ) :                            
            for row in ret :
                szOutput += "(%s%d:%d) %s\n" % (booknm,row['BOOK_CHAP_NO'],row['BOOK_NO'],row['BOOK_CONTENT'])            
            return {"ret":"ok", "msg":szOutput}
        else :                
            return {"ret":"fail", "msg":szOutput}