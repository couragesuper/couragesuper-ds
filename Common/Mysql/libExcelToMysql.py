import pandas as pd
# import mysql library
import sys
import openpyxl
from pathlib import Path
sys.path.append("../../Common")
sys.path.append("../Common")
from Mysql.libmysql import dbConMysql

class ExcelToMysql :
    def __init__(self , excelName ):
        print("ExcelToMysql __init__ :selected FileName :{}".format(excelName))
        self.excelName = str(excelName)
        self.resetMembes()
        if (Path(self.excelName).exists() == False):
            self.lastError = 1

    def resetMembes(self):
        self.lastError = 0
        self.sheetList = []
        self.sheetName = ""
        self.fieldPKArr = []
        self.autoColumn = 0

    def getSheetNames( self ):
        print("ExcelToMysql getSheetNames")
        if( self.lastError == 0 ) :
            wb = openpyxl.load_workbook(self.excelName)
            for i in wb.get_sheet_names():
                self.sheetList.append(i)
            return 0
        else:
            return 1

    def setSheetName(self , sheetName ):
        self.resetMembes()
        if( self.lastError == 0 ):
            self.sheetName = sheetName
            return 0
        else:
            return 2

    def initDB(self , config_db = {'user': 'root', 'password': 'karisma*3%7*4', 'host': 'mthx.cafe24.com', 'database': 'bible',
                     'raise_on_warnings': True} ):
        print( "initDB : {}".format( config_db ))
        self.config_db = config_db
        self.db = dbConMysql( self.config_db )
        print( self.db )
    def makeDbSchema(self) :
        self.df_data = pd.read_excel(self.excelName, sheet_name=self.sheetName)  # 대소문자 구분된다.
        # 3.make column dict for pandas
        self.mapIdxCol = {column: int(list(self.df_data).index(column)) for column in self.df_data.columns}
        self.mapDbSchema = {}
        #print(df_data)
        for field in self.df_data.columns:
            # print( df_data.iloc[ 0 , mapIdxCol[field] ] )
            col_id = self.mapIdxCol[field]
            if (field not in self.mapDbSchema): self.mapDbSchema[field] = {}
            self.mapDbSchema[field]['datatype'] = self.df_data.iloc[1, col_id]
            self.mapDbSchema[field]['isnull'] = self.df_data.iloc[2, col_id]
            if (self.df_data.iloc[0, col_id] == "PK"):
                print("PK is this field :" + field)
                self.mapDbSchema[field]['ispk'] = True
                self.fieldPKArr.append( field )
            else:
                self.mapDbSchema[field]['ispk'] = False
        print(self.mapDbSchema)

        if( len( self.fieldPKArr ) == 0 ) :
            print("PK isn't exist")
            return 3
        return 0
    def createDbSchema(self) :
        if ((self.lastError != 0) or self.sheetName == ""):
            return 4
        self.create_query_state = "CREATE TABLE `{table_name}` ( \n".format(table_name=self.sheetName )
        for key, val in self.mapDbSchema.items():
            print(val)
            null_str = "NOT NULL"
            if (val['isnull'] == False): null_str = "NULL"
            query_elem_row = "`{field_name}` {data_type} {isnull} ".format(field_name=key, data_type=val['datatype'], isnull=null_str)
            if (key in self.fieldPKArr and (self.autoColumn == 0) ) :
                query_elem_row += " AUTO_INCREMENT,\n"
                self.autoColumn = self.autoColumn + 1
            else:
                query_elem_row += ",\n"
            self.create_query_state += query_elem_row
        self.create_query_state += "PRIMARY KEY ("
        isFirst = True
        for elem in self.fieldPKArr :
            if( isFirst ) : isFirst = False
            else : self.create_query_state += ","
            self.create_query_state += "`{}`".format( elem )
        self.create_query_state +=")\n ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"
        print(self.create_query_state)
        self.db.commitQuery("drop table {table_name};".format( table_name=self.sheetName ))
        self.db.commitQuery( self.create_query_state )
    def pushDbData(self):
        if (self.lastError != 0):
            return 5
        loop = 3
        lenIndex = len(self.df_data.index)
        cnt = 0
        query_stat = "insert into bible.{}(".format(self.sheetName)
        for key, val in self.mapDbSchema.items():
            if (cnt > 0): query_stat += ","
            query_stat += key
            cnt = cnt + 1
        query_stat += ") values ("
        loop = 3
        lenIndex = len(self.df_data.index)
        print(query_stat)
        while (True):
            query_stat_cp = query_stat
            if (loop == lenIndex):
                break
            cnt = 0
            for key, val in self.mapDbSchema.items():
                if (cnt > 0): query_stat_cp += ","
                if ("varchar" in val['datatype']): query_stat_cp += '"'
                cnt = cnt + 1
                query_stat_cp += "{}".format(self.df_data.iloc[loop, self.mapIdxCol[key]])
                if ("varchar" in val['datatype']): query_stat_cp += '"'
            query_stat_cp += ");"
            ret = self.db.commitQuery(query_stat_cp)
            print("{} : {}".format(query_stat_cp, ret))
            loop = loop + 1

if __name__ == "__main__":
    excel2Mysql = ExcelToMysql("CreateTable.xlsx")
    if( excel2Mysql.getSheetNames() == 0 ):
        print( excel2Mysql.sheetList )
        excel2Mysql.initDB()
        excel2Mysql.getSheetNames()
        print( excel2Mysql.sheetList )
        excel2Mysql.setSheetName("praise")
        print("step..1")
        excel2Mysql.makeDbSchema()
        print("step..2")
        excel2Mysql.createDbSchema()
        print("step..3")
        excel2Mysql.pushDbData()
        print("step..4")
    else:
        print("to open excel is failed.")

