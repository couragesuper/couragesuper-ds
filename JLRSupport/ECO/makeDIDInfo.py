#install rdxl
#install openpyxl

import pandas as pd

name_fmt = 'IGCJ1PHE.BJVJ{}';
dictVariants = [
    { 'variants' : 'JAPAN' , 'name' : 'JLR PIVI Diamond Japan (IGCJ1PHE.BJVJ340)' , 'fmt' : 'IGCJ1PHE.BJVJ{}' },
    { 'variants' : 'Row w/ Dab (nodab)' , 'name' : 'JLR PIVI Diamond RoW w/ DAB (IGCJ1PHE.BRDJ340)' , 'fmt' : 'IGCJ1PHE.BRDJ{}' },
    { 'variants' : 'NAS' , 'name' : 'JLR PIVI Diamond NAS (IGCJ1PHN.BNSJ340)' , 'fmt' : 'IGCJ1PHN.BNSJ{}' },
    { 'variants' : 'CHN' , 'name' : 'JLR PIVI Diamond CHN (IGCJ1PHC.BCCJ340)' , 'fmt' : 'IGCJ1PHC.BCCJ{}' },
    { 'variants' : 'w/o DAB (RO)' , 'name' : 'JLR PIVI Diamond w/o DAB (IGCJ1PHE.BRBJ340)' , 'fmt' : 'IGCJ1PHE.BRBJ{}' },
    { 'variants' : 'CHN (CH)' , 'name' : 'JLR PIVI Diamond CHN (IGCJ1PHC.BCCC340)' , 'fmt' : 'IGCJ1PHC.BCCC{}' },
    { 'variants' : 'EMC' , 'name' : 'JLR PIVI EMC (IGCJ1PHE.BRNJ340)' , 'fmt' : 'IGCJ1PHE.BRNJ{}' },
]

for elem in dictVariants :
    print( "variants:{}".format( elem["variants"] ) )
    for k,v in elem.items() :
        print("k:{}=v:{}".format(k,v))
    print("\n")

name_excel = "D:\\work\\rpt\\ECO\\DID Information\\SW ECO_DID_JL03RD340ICJLR_220711\\JLR PIVI DID_information_IP340_220711_REV7.xlsx"
df_eco =  pd.read_excel( open( name_excel ,'rb' ) , sheet_name = "Appx. JLR_part No" , engine = 'openpyxl' )

#df_eco = df_eco.drop(0)
df_eco = df_eco.iloc[:, 1:]

print( df_eco )
print( df_eco.columns )
print( df_eco.index )
print( df_eco.values )

