import random

class Puzzle_Mesa1 :
    def __init__(self , nx , ny ):
        self.reset( nx , ny )

    def reset(self , nx , ny):
        self.nx = nx
        self.ny = ny
        self.board = [["99" for nx in range(0, nx)] for y in range(0, ny)]
        self.boardChar = [["99" for nx in range(0, nx)] for y in range(0, ny)]

    def showBoard(self):
        print( self.board )
        print( self.boardChar )

    def displayBoard(self):
        str = ""
        for y in range( 0 , self.ny ) :
            str = str + "["
            for x in range( 0 , self.nx ) :
                str = str +  " {} ".format( self.boardChar[x][y] )
            str = str + "]\n"
        print( str )


    def getChar( self, nx, ny , prvNx, prvNy ) :
        szChar = ""
        if( prvNx == nx ):
            diffY = ( ny - prvNy )
            if( diffY > 0 ) : szChar = "{}D".format( diffY )
            else : szChar = "{}U".format(-diffY)
        if (prvNy == ny):
            diffX = (nx - prvNx )
            if (diffX > 0):
                szChar = "{}R".format(diffX)
            else:
                szChar = "{}L".format(-diffX)
        return szChar

    # To resolve situation when progressing is impossible
    def checkFailedCreation(self , chkIdx, prvNx, prvNy ) :
        cnt99 = 0
        if( self.debug ) : print( "[checkFailedCreation] ({},{}) ".format( prvNx , prvNy ))
        for l in range(0,5):
            if( self.board[l][prvNy] == '99' ) : cnt99 = cnt99 + 1
            if( self.board[prvNx][l] == '99' ) : cnt99 = cnt99 + 1

        if( cnt99 == 0 ) :
            if( self.debug ) : print("[checkFailedCreation][Failed] cnt99:{}".format(cnt99))
            return False
        if( self.debug ) : print("[checkFailedCreation][Succeed] cnt99:{}".format(cnt99))
        return True

    def oneShotBoard(self):
        self.debug = False
        ret = self.makeBoard()
        while ret == False:
            ret = puzzle.reset(self.nx, self.ny)
            ret = puzzle.makeBoard()
        self.displayBoard()

    def makeBoard(self):
        chkIdx = 0
        isDone = True
        isDoneBoard = True
        prvNx = 99
        prvNy = 99

        while isDone :
            nx = random.randrange(0,5)
            ny = random.randrange(0,5)
            if( self.board[nx][ny] == "99") :
                self.board[nx][ny] = str(chkIdx)
                if( self.debug ) : print( "First Set = ({},{})".format( nx , ny ) )
                chkIdx = chkIdx + 1
                isDone = False
                prvNx = nx
                prvNy = ny

        while isDoneBoard :
            isDone = True
            infoLoop = 0
            if (self.checkFailedCreation(chkIdx, prvNx, prvNy) == False): return False
            while isDone:
                nx = random.randrange(0, 5)
                ny = random.randrange(0, 5)
                if( self.debug ) : print("[2]new = (x:{},y:{}) -> Prv(x:{},y:{}) Val:{} loop:{}".format(nx, ny , prvNx, prvNy , self.board[nx][ny] , infoLoop ))
                infoLoop = infoLoop + 1
                if ( (self.board[nx][ny] == "99") and ( ((nx == prvNx) and ( ny != prvNy  )) or (( nx != prvNx ) and ( ny == prvNy )) ) ):
                    if( self.debug ) : self.showBoard()
                    if( self.debug ) : print("[{}]Set = (x:{},y:{}) -> Prv(x:{},y:{}) Val:{} loop:{}".format( chkIdx ,nx, ny , prvNx, prvNy , self.board[nx][ny] , infoLoop ))
                    self.board[nx][ny] = str(chkIdx)
                    chkIdx = chkIdx + 1
                    isDone = False
                    # set previous char in board
                    self.boardChar[prvNx][prvNy] = self.getChar( nx, ny , prvNx, prvNy )
                    prvNx = nx
                    prvNy = ny
            cnt99 = 0
            for x in range(0,self.nx) :
                    for y in range (0,self.ny) :
                        if(self.board[x][y] != '99') :
                            cnt99 = cnt99+1
            #self.showBoard()
            #print( "cnt99:{}".format(cnt99) )
            if( cnt99 == (self.nx * self.ny) ) :
                #print("cnt99 is done")
                self.boardChar[prvNx][prvNy] = "St"
                isDoneBoard = False
        return True



puzzle = Puzzle_Mesa1( 5 , 5 )

if False :
    retry = 0
    ret = puzzle.makeBoard()
    print("ret == {}".format(ret))
    while ret == False :
        print("retry")
        retry = retry + 1
        ret = puzzle.reset( 5 , 5 )
        ret = puzzle.makeBoard()

    print( "    creation result : cnt{}".format(retry) )
    puzzle.showBoard()
    puzzle.displayBoard()

if True :
    puzzle.oneShotBoard()







