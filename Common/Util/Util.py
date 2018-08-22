import time 

class stopWatch() :
    def reset(self) :
        self.start_time = time.time()
    def diff(self):
        print( "difference : %d sec " % (time.time() - self.start_time) )        

