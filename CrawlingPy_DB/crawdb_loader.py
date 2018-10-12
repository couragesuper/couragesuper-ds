import sys
import time
sys.path.append("../Common/Mysql")

from libmysql import dbConMysql

class crawdata :
    def __init__ ( self, contentID ) :
        self.db = dbConMysql()
    def setContentID( self ) :








