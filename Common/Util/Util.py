import time 
import platform
from   matplotlib import font_manager, rc

class stopWatch() :
    def reset(self) :
        self.start_time = time.time()
    def diff(self):
        print( "difference : %d sec " % (time.time() - self.start_time) )
    def diffWithTag(self , tag ):
        print( "[%s] diff = %4.2f sec " % ( tag ,  float(time.time() - self.start_time ) ) )
