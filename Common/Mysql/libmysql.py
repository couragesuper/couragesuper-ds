import mysql.connector

class dbConMysql:
    def __init__(self , dictConfig ) :
        self.con = mysql.connector.connect( **dictConfig )
    def commitQuery(self, szQry):
        try : 
            self.cursor = self.con.cursor(buffered = True)
            self.cursor.execute(szQry) 
            self.cursor.close()        
            self.con.commit()
        except:
            print(szQry)
    def selectQuery(self,szQry):
        try:
            self.cursor = self.con.cursor(buffered = True)
            self.cursor.execute(szQry)
            listRet = [ { self.cursor.description[i][0]:elem  for i,elem in enumerate(row)} for row in self.cursor ]
            self.cursor.close()
        except:
            print(szQry)
        return listRet        