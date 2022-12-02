
rawDidData = "62 80 C6 10 00 00 49 12 49 40 00 49 12 49 40 00 F0 00 00 F0 00 00 10 00 00 10 00 00 10 00 00 10 00 00 30 30 00 10 00 00 00 00 F0 00 00"

def DidRawStrToByteArray( rawData ) :
    splitDidData = rawDidData.split(" ")
    #print(splitDidData)
    DidArray = bytearray()
    for elem in splitDidData:
        DidArray.append(int(elem, 16))
    return DidArray

DidArray = DidRawStrToByteArray( rawDidData )

print( DidArray )

def ParseDid80C6( iData ) :
    Data = {}
    accumlateVal = 0
    NumberofData = 13
    aModule = ["Camera","Front USB","Rear USB","Dab Receiver","Sdars Receiver","Vics","BT Antenna","WIFI Antenna","GNSS ","ESIM","Apple Auth","Memory","Dab Internal(SPI)"]
    aParseType = [1,2,2,1,1,1,1,1,1,1,1,3,1]
    aOffset = [0,3,8,13,16,19,22,25,28,31,34,37,39]

    if False : print(  "len{0} len{1} len{2}".format(  len(aModule) , len(aParseType) , len(aOffset) ) )

    for idx in range( 0 , NumberofData ) :
        parseType = aParseType[idx]
        module = aModule[idx]
        offset = aOffset[idx] + 3
        print( "ParseDid80C6 elem :{} {} {}".format( parseType, module, offset ))
        if( parseType == 1) :
            postfix = "ret"
            Data[module + "_" + postfix] = hex((iData[offset] & 0xF0) >> 4)

            postfix = "ErrorCount"
            accumlateVal = (iData[offset] << 8) | iData[offset + 1]
            accumlateVal = accumlateVal & 0xFFF
            Data[module + "_" + postfix] = hex(accumlateVal)

            postfix = "ErrorCountPowerCycle"
            Data[module + "_" + postfix] = hex(iData[offset + 2])
        elif (parseType == 2) :
            postfix = "PID"
            accumlateVal = (iData[offset] << 24) | (iData[offset+1] << 16) | (iData[offset+2] << 8) | (iData[offset+3])
            Data[module + "_" + postfix] = hex(accumlateVal)

            postfix = "ErrorCountPowerCycle"
            Data[module + "_" + postfix] = hex(iData[offset+4])
        elif (parseType == 3) :
            postfix = "ErrorCount"
            Data[module + "_" + postfix] = hex(iData[offset])

            postfix = "ErrorCountPowerCycle"
            Data[module + "_" + postfix] = hex(iData[offset + 1])
    return Data

ParseDid80C6 = ParseDid80C6( DidArray )
print( ParseDid80C6 )

























