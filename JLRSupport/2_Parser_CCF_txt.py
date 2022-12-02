import os

dir = "D:\\work\\rpt\\20220525_corvus_gwm_update\\pp\\ccf.txt"

file_txt = open( dir ,"r" )
arr_dict_ccf_from_pivi = []

def convert_ccffile_to_array_dict ( file_path ) :
    global arr_dict_ccf_from_pivi
    line = file_txt.readline()
    count = 0
    while line :
        if( count == 0 ) :
            count = count + 1
            line = file_txt.readline()
            continue
        split_arr = line.split("\t")
        dict_elem = {
            "id" : split_arr[0],
            "val": split_arr[1],
            "mdf": split_arr[2],
            "name": split_arr[3].replace("_" ," " )
        }
        arr_dict_ccf_from_pivi.append( dict_elem )
        count = count + 1
        line = file_txt.readline()

convert_ccffile_to_array_dict ( dir )
#print( arr_dict_ccf_from_pivi )

def remove_zeroval_elem_in_ccf_dict() :
    global arr_dict_ccf_from_pivi
    arr_result = []
    for elem in arr_dict_ccf_from_pivi :
        if( elem["val"] != 0 ) :
            arr_result.append( elem )
    return arr_result

arr_result = remove_zeroval_elem_in_ccf_dict()

print( arr_result )
print( len( arr_result ))

meanful_items = [ "VEHICLE_TYPE" , "DOORS" , "TRANSMISSION_DRIVELINE" , "FUEL" , "STEERING_WHEEL_POSITION" , "BRAND" ,"BODY_STYLE", "NAVIGATION_SYSTEM", "Head_Up_Display", "Model_Year", "FrntDispVariant", "FntDispCableLgth", "FntClusterCableLgth", "FrntUpperDispVariant", "HUDSubType", "HybridModeSelect", "IVIType", "IVISIMType" ]

def show_meanfun_item() :
    global arr_result
    for elem in arr_result :
        for key in meanful_items :
            if( key.lower().replace("_" , " " ) == elem["name"].lower() ) :
                print( "name:{0} , mdf:{1} , value:{2}".format(elem["name"] , elem["mdf"] , elem["val"]) )

show_meanfun_item()

