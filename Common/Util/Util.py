import time 
import platform
from   matplotlib import font_manager, rc
#for random array
import random

# Utility
    # 1.StopWatch : class to measure between reset() and diff()

# function
    # 2.Array Helper
    # 3.Log helper ??

class stopWatch() :
    def reset(self) :
        self.start_time = time.time()
    def diff(self):
        print( "difference : %d sec " % (time.time() - self.start_time) )
    def diffWithTag(self , tag ):
        print( "[%s] diff = %4.2f sec " % ( tag ,  float(time.time() - self.start_time ) ) )

def makeArray( cnt ) :
    return [ i for i in range(0,cnt) ]

def makeFillArray( cnt , num ) :
    return [ num for i in range(0,cnt)]

def makeRandomArray( cnt , range_begin , range_end ) :
    return [ random.randrange( range_begin , range_end  ) for i in range(0,cnt) ]

def make2Darray( nx, ny , num ):
    return [ [ num for i in range(0,nx)] for i in range(0,ny) ]

if False :
    print( "makeArray = {}".format( makeArray(10)) )
if False :
    print( makeRandomArray(10,1,10) )
if False :
    print( makeFillArray(5,3) )
if True :
    print( make2Darray( 3,3, 3) )









