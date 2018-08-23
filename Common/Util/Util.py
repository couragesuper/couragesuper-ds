import time 
import platform
from   matplotlib import font_manager, rc

class stopWatch() :
    def reset(self) :
        self.start_time = time.time()
    def diff(self):
        print( "difference : %d sec " % (time.time() - self.start_time) )        

class helpPlatform() :
    def __init__(self):
        if platform.system() == 'Linux' :
            self.platform = "linux"
        elif platform.system() == 'Darwin' :
            self.platform = "apple"
        elif platform.system() == "Windows" :
            self.platform = "win"
        else :
            self.platform = "unknown"

