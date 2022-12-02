# Test for FIR

# FIR Fake Data
fir_input_data = []

fir_input_data.append( bytearray([0x01, 0x02, 0x07, 0x001d, 0x0000, 0x0014, 0x0000, 0x0005, 0x0000]) )
fir_input_data.append( bytearray([0x01, 0x02, 0x09, 0x0014, 0x0000, 0x0014, 0x0000, 0x000a, 0x0000]) )
fir_input_data.append( bytearray([0x01, 0x02, 0x09, 0x0000, 0x0000, 0x0014, 0x0000, 0x0014, 0x0000]) )
fir_input_data.append( bytearray([0x01, 0x02, 0x0b, 0x0022, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000]) )
fir_input_data.append( bytearray([0x01, 0x02, 0x0c, 0x0029, 0x0000, 0x0000, 0x0000, 0x0007, 0x0000]) )
fir_input_data.append( bytearray([0x01, 0x02, 0x0c, 0x0029, 0x0000, 0x0000, 0x0000, 0x0007, 0x0000]) )
fir_input_data.append( bytearray([0x01, 0x02, 0x07, 0x001d, 0x0000, 0x0014, 0x0000, 0x0005, 0x0000]) )
fir_input_data.append( bytearray([0x01, 0x02, 0x09, 0x0014, 0x0000, 0x0014, 0x0000, 0x000a, 0x0000]) )
fir_input_data.append( bytearray([0x01, 0x02, 0x09, 0x0000, 0x0000, 0x0014, 0x0000, 0x0014, 0x0000]) )
fir_input_data.append( bytearray([0x01, 0x02, 0x0b, 0x0022, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000]) )

if False : # Test is ok
    for elem in fir_input_data :
        print(elem) # OK
        for elem_2 in elem :
            print( hex(elem_2) ) # need to change hexa format


filename = "D:\\work\\rpt\\1_Progress_IP35\\20220829_FIR_DUMMY\\20220831_FIX_1ST\\80D6_Input.txt"
def readDIDData( filename ) :
    fCorvus = open(filename, "r+")
    didArray = []
    isDebug = False

    buf = fCorvus.readline(1024)
    while len(buf) > 0 :
        if( ( "Send" in buf ) or ( "Received" in buf ) ) :
            if( isDebug ) : print("Skip={}".format(buf))
        else :
            split_buf = buf.split(" ")
            if( isDebug ) : print( split_buf )
            if (split_buf[0] == "62" and split_buf[1] == "80" and split_buf[2] == "D6"):
                if( isDebug ) : print("Handle-{}".format(buf))
                arr = bytearray()
                for idx in range(3, len(split_buf) - 1):
                    arr.append(int(split_buf[idx], 16))
                if( isDebug ) : print( "add array={}".format( arr ) )
                didArray.append(arr)
        buf = fCorvus.readline(1024)
    return didArray

didData = readDIDData( filename )
print( "[readDIDData] \t Len:{0} \t Data:{1}".format( len(didData) , didData ))

#62 80 D6 AB CC DD EE EF FF GG GH HH II IJ JJ KK KL LL MM MN NN OO OP PP QQ RR RR RR RR SS SS SS SS TT UU VV WW XX YY ZZ ZZ ZZ ZZ A1 A1 A1 A1 A2 A3 A4
#         00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46

def parse80D6Data ( iData ) : # inData is byteArray
    dicRet = {}
    dicRet["autotune"] = hex((iData[0] & 0xF0) >> 4)
    dicRet["screencheck"] = hex((iData[0] & 0xF ))

    dicRet["fir_cur"] = hex(iData[1])
    dicRet["fir_prv"] = hex(iData[2])

    name = [    "crc_h_u_c",    "crc_h_u_P",    "crc_h_l_c",    "crc_h_l_P",    "crc_m_u_c",    "crc_m_u_P",    "crc_m_l_c",    "crc_m_l_P",    "crc_l_u_c",    "crc_l_u_P",    "crc_l_l_c",    "crc_l_l_P"    ]

    for i in range(0,6) :
        val_combination = (iData[ 3 + i * 3 ] << 16) | (iData[ 3 + i * 3 + 1] << 8) | (iData[ 3 + i * 3 +2])
        print( " val_combi {0} = {1} ".format( i, hex(val_combination) ))
        dicRet[ name[ 2 * i ] ] = hex( val_combination >> 12 )
        dicRet[ name[ 2 * i + 1 ]] = hex( val_combination & 0xFFF )
    print(dicRet)

parse80D6Data ( didData[0] )







