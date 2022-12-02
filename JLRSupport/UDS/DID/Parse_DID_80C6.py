
#Parsing 80C6

pkt_did_80c6 = "62 80 C6 10 00 00 49 12 49 40 00 FF FF FF FF 00 10 00 00 F0 00 00 F0 00 00 10 00 00 10 00 00 F0 00 00 FF FF 00 F0 00 00"

# Input "XX XX XX XX XX XX XX"
# Ouput : List of integer
def HexstrToList( inString ) :
    split = pkt_did_80c6.split(" ")
    return [int(x, 16) for x in split]

did_80c6 = HexstrToList( pkt_did_80c6 );

if False :
    idx = 0
    for elem in did_80c6:
        print( "ID:{0} {1}".format(idx, hex(elem)) )
        idx = idx + 1

class did80c6 :
    def __init__(self , inData ):
        print( "did80C6 : len : {0}".format( len(inData) ))

        #type checker
        if type( inData ) is not list :
            print("inData isn't List")

        if type( inData[0] ) is not int :
            print("type of inData isn't integer")

        self.dictData = {
            "Camera" :{
                "Result" : (inData[3] & 0xF0) >> 4 ,
                "ErrorCount" : ((inData[3] & 0xF) << 8) | inData[4]  ,
                "NumOfPowerCycle" : inData[5]
            },
            "FrontUSB" : {
                "PID" : (inData[6] << 24) | (inData[7] << 16) | (inData[8] << 8) | (inData[9]) ,
                "CountOfPowerCycle" : inData[10]
            },
            "RearUSB" : {
                "PID" : (inData[11] << 24) | (inData[12] << 16) | (inData[13] << 8) | (inData[14]) ,
                "CountOfPowerCycle" : inData[15]
            },
            "DabReceiver" : {
                "Result" : (inData[16] & 0xF0) >> 4 ,
                "ErrorCount" : ( (inData[16] & 0xF) << 8 ) | inData[17],
                "NumOfPowerCycle" : inData[18]
            },
            "SdarsReceiver" : {
                "Result" : (inData[19] & 0xF0) >> 4 ,
                "ErrorCount" : ( (inData[19] & 0xF) << 8 ) | inData[20],
                "NumOfPowerCycle" : inData[21]
            },
            "Vics" : {
                "Result" : (inData[22] & 0xF0) >> 4 ,
                "ErrorCount" : ( (inData[22] & 0xF) << 8 ) | inData[23],
                "NumOfPowerCycle" : inData[24]
            },
            "BtAnt" : {
                "Result" : (inData[25] & 0xF0) >> 4 ,
                "ErrorCount" : ( (inData[25] & 0xF) << 8 ) | inData[26],
                "NumOfPowerCycle" : inData[27]
            },
            "WIFI" : {
                "Result" : (inData[28] & 0xF0) >> 4 ,
                "ErrorCount" : ( (inData[28] & 0xF) << 8 ) | inData[29],
                "NumOfPowerCycle" : inData[30]
            },
            "GNSS" : {
                "Result" : (inData[31] & 0xF0) >> 4 ,
                "ErrorCount" : ( (inData[31] & 0xF) << 8 ) | inData[32],
                "NumOfPowerCycle" : inData[33]
            },
            "ESIM" : {
                "Result" : (inData[34] & 0xF0) >> 4 ,
                "ErrorCount" : ( (inData[34] & 0xF) << 8 ) | inData[35],
                "NumOfPowerCycle" : inData[36]
            },
            "AppleAuth" : {
                "Result" : (inData[37] & 0xF0) >> 4 ,
                "ErrorCount" : ( (inData[37] & 0xF) << 8 ) | inData[38],
                "NumOfPowerCycle" : inData[38]
            },
            "Memory" : {
                "Result" : (inData[39] & 0xF0) >> 4 ,
                "ErrorCount" : ( (inData[39] & 0xF) << 8 ) | inData[40],
                "NumOfPowerCycle" : inData[41]
            },
            "DABSPI" : {
                "Result" : (inData[42] & 0xF0) >> 4 ,
                "ErrorCount" : ( (inData[42] & 0xF) << 8 ) | inData[43],
                "NumOfPowerCycle" : inData[44]
            },
        }

    def showData(self):
        for k,v in self.dictData.items() :
            print( "{0}".format(k) )
            for k2,v2 in v.items() :
                print( " {0}, Val:{1}".format(k2, hex(v2) ))

inst80c6 = did80c6( did_80c6 )
inst80c6.showData()

