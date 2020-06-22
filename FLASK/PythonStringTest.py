dictarg = {"a":"1" ,"b":"2" ,"c":"3"}
sz="{b},{c}"
print( sz.format( b = 1 , c = 2) )
print( sz.format( **dictarg ) )
#.format(dictarg)

