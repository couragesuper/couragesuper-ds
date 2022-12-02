import pandas as pd

# work to do

filepath = "D:\\work\\rpt\\1_Progress_IP36\\ECO\\Scripts\\IP35_ECO605\\"
filename = "info_IP35_SMT.txt"

def parseSMTInfo( filePathName ) :
    print( filePathName )
    isFoundICCMHeader = False
    isFoundIGMHeader = False
    idxLun = 0
    with open( filePathName , "r" ) as f :
        line = f.readline()
        while( line ):
            if( "ICCM LUN checksum :" in line ) :
                isFoundICCMHeader = True
            if ("IGM Checksum : " in line) :
                isFoundIGMHeader = True
            if( (isFoundICCMHeader == True) and ( isFoundIGMHeader == False ) ) :
                if( ("DIAMOND_LUN" in line) and ("merkle.chksum" in line ) ) :
                    print( "CRC:{}".format( line ) )
                    print( line.split(":")[1].replace(" ","") )


            line = f.readline()

parseSMTInfo( filepath + filename )
exit(0)

#Columns : ['PART', 'SAA', 'NAS', 'CHN', 'woDAB', 'wDAB', 'JAP', 'CheckSum', 'Version']
#Parts : ['UFS', 'MICOM', 'HD-RADIO', 'DAB', 'ETHERNET', 'GPS']

scripts = "D:\\work\\rpt\\1_Progress_IP36\\ECO\\Scripts\\IP35_ECO605\\IP35_ECO605.xlsx"
df = pd.read_excel( scripts , engine='openpyxl' )

#print( df )
#print( df.columns )

columns = df.columns.tolist()

# convert Item list to index-item map
parts = df['PART'].tolist()
idxParts = { parts[idx] : idx for idx in range(0,len(parts)) }

# show results
print( "idxParts = {}".format( idxParts ) )
print( "columns = {}".format( columns )   )
print( "parts = {}".format( parts ) )

def makePartDict( ) :
    print( idxParts['UFS'])
    print(idxParts['MICOM'])
    print(idxParts['HD-RADIO'])
    print(idxParts['DAB'])
    print(idxParts['ETHERNET'])
    return

