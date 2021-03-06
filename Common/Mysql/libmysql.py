import mysql.connector

class dbConMysql:
    def __init__(self , dictConfig ) :
        try :
            self.con = mysql.connector.connect( **dictConfig )
            print( "[dbConMysql] initalized ... = {}".format(  self.con ) )
        except Exception as e :
            print("[dbConMysql] initalized is excepted  = {}".format(e))
    def __del__(self):
        try :
            self.con.close()
            print("[dbConMysql] closed ... = {}".format(self.con))
        except Exception as e:
            print("[dbConMysql] closed is excepted  = {}".format(e))
    def commitQuery(self, szQry):
        try : 
            self.cursor = self.con.cursor(buffered = True)
            self.cursor.execute(szQry) 
            self.cursor.close()        
            self.con.commit()
            return True
        except Exception as e:
            print("[dbConMysql] commitquery = {},e:{}".format( szQry , e ) )
            return False

    def Lock(self):
        try:
            self.cursorCommit = self.con.cursor(buffered=True)
            return True
        except Exception as e:
            print("[dbConMysql] Lock e:{}".format( e))
            return False

    def LockQuery(self,szQry):
        if (self.cursorCommit != None) :
            try:
                self.cursorCommit.execute(szQry)
            except Exception as e:
                print("[dbConMysql] LockQuery e:{}".format( e))
                return False
        else :
            return False
        return True

    def unLock(self):
        try:
            self.cursorCommit.close()
            self.cursorCommit = None
            self.con.commit()
            return True
        except Exception as e:
            print("[dbConMysql] unLock e:{}".format( e))
            return False

    def selectQuery(self,szQry):
        try:
            self.cursor = self.con.cursor(buffered = True)
            self.cursor.execute(szQry)
            listRet = [ { self.cursor.description[i][0]:elem  for i,elem in enumerate(row)} for row in self.cursor ]
            self.cursor.close()
            return listRet
        except Exception as e:
            print("[dbConMysql] selectQuery exception with={}:query:{} ".format(e,szQry))
            return []
    def selectQueryWithRet(self, szQry):
        try:
            self.cursor = self.con.cursor(buffered=True)
            self.cursor.execute(szQry)
            listRet = [{self.cursor.description[i][0]: elem for i, elem in enumerate(row)} for row in self.cursor]
            self.cursor.close()
            return { "ret":True, "data":listRet }
        except Exception as e:
            print("[dbConMysql] selectQuery exception with={}:query:{} ".format(e, szQry))
            return { "ret":False, "data":[] }


isTest = False
if( isTest ) :
    config = { 'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'Crawling', 'raise_on_warnings': True }
    db = dbConMysql( config )
    qry = "SELECT * from TB_CRAWLER_TEXTDATA LIMIT 1,30"
    retSelect = db.selectQuery( qry )
    for row in retSelect :
        print( row )


