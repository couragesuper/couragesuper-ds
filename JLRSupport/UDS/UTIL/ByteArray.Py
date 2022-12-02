
# Byte Array

# 1.Assign ByteArray
ba = bytearray([0x62, 0x80, 0xC6, 0x10, 0x00, 0x00, 0x49, 0x12, 0x49, 0x40, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x10, 0x00, 0x00, 0xF0, 0x00, 0x00, 0xF0, 0x00, 0x00, 0x10, 0x00, 0x00, 0x10, 0x00, 0x00, 0xF0, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0xF0, 0x00, 0x00])
print(ba)
print( hex( ba[0]) )
print( len(ba))

data = b'\x02\xfd\x00\x01\x00\x00\x00\x00'

bOn1 = True
bOn2 = True
bOn3 = True

# 2.Iteration in ByteArray
if bOn1 :
    print("ba type{}".format(type(ba)))
    for i in range(0,len(ba)) :
        print( "IDX:{0} = Val:{1}".format( i , ba[i]) )

# 3.Iteration on Bytes
if bOn2 :
    print("data type{}".format(type(data)))
    for i in range(0,len(data)) :
        print( "IDX:{0} = Val:{1}".format( i , data[i]) )

# 4.Converting Bytes to Bytearray
if bOn3 :
    #이게 되는듯  하다.
    ba_cvt = bytearray( data )
    print("ba_cvt type{}".format(type(ba_cvt)))
    for i in range(0,len(ba_cvt)) :
        print( "IDX:{0} = Val:{1}".format( i , hex(ba_cvt[i]) ) )
