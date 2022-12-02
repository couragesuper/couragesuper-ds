import random

# func: QuickSort
# var : first - index of first
# var : last - index of last
def QuickSort( arrList, first , last ) :
    if( first >= last ) : return
    pVal = arrList[last]
    pIdx = last
    l = first
    r = last - 1
    while( l < r ) :
        while( (l <= r) and ( arrList[l] <= pVal) ) : l = l + 1
        while( (l <= r) and ( arrList[r] >= pVal) ) : r = r - 1
        if( l < r ) :
            t = arrList[l]
            arrList[l] = arrList[r]
            arrList[r] = t
    if( arrList[l] > arrList[pIdx] ) : # WRONG 1
        t = arrList[l]
        arrList[l] = arrList[pIdx]
        arrList[pIdx] = t
        pIdx = l # WRONG 2
    QuickSort( arrList, first, pIdx - 1 )
    QuickSort( arrList, pIdx + 1, last )


randList = [ random.randrange(0,100) for i in range(0,20) ]
print( randList )
QuickSort( randList, 0, len(randList)-1)
print( randList )