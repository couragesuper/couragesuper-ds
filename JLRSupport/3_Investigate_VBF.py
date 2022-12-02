import os

#Function

#Loader PIVI CCF
# 1) making compare list
    # dict : mdf / value

#Parsing Manager
    # 1) Single File
        # Compute Difference Distance
        # Change List

    # 2) Iteration Functino
        # making Score List
        # making Change Lists
        # union set / intersect set

    # Work to do
        # Filter (Searching Filter /
        # GUI


# PhoneProjection
    # 5F67 is important.

class pivi_ccf :
    def __init__(self):
        self.resetmembers()

    def resetmembers(self):
        self.filepath = ""
        # data
            # format id / mdf / val / name (with underline instead of empty space )
        self.data = []
        self.dataAll = []
        # data to compare with mdf value
        self.dictMdfToName = {}
        self.meanfulItem = []
        self.arr_result = []
        self.source_file = ""
        # remove 0 value to list
        self.removeZeroval = True
        self.dictMdfToVal = {}


    def load(self,file_path):
        file_txt = open(file_path, "r")
        self.filepath = file_path

        line = file_txt.readline()
        isFirst = True

        while line:
            if (isFirst == True):
                isFirst = False
                line = file_txt.readline()
                continue
            split_arr = line.split("\t")
            dict_elem = {
                "id": int( split_arr[0] ) ,
                "val": int( split_arr[1] , 16 ) ,
                "mdf": int( split_arr[2] , 16 ) ,
                "name": split_arr[3]
            }
            self.dictMdfToName[dict_elem["mdf"]] = dict_elem[ "name" ]
            self.dataAll.append(dict_elem)
            if( (self.removeZeroval == False ) or ( (self.removeZeroval == True) and (dict_elem["val"] != 0) )  ) :
                self.data.append(dict_elem)
                self.dictMdfToVal[dict_elem["mdf"]] = dict_elem["val"]
            line = file_txt.readline()

    def remove_zerovalue(self):
        for elem in self.data:
            if (elem["val"] != 0):
                self.arr_result.append(elem)

    def show_remove_zerovalue(self):
        print( self.arr_result )

    def showCompareMap(self):
        print( self.dictMdfToVal )
        
    def showMap(self):
        print( self.data)

    def query(self , type , filter ):
        dictArray = []
        for elem in self.dataAll :
            key = elem[ type ]
            if( key in filter ) :
                print( " ID:{0} MDF:{1} NAME:{2} VAL:{3} ".format( elem["id"] , hex( elem["mdf"]) , elem["name"] , hex( elem["val"] ) ) )
                dictArray.append( elem )
        return dictArray

    def extract_menufulItems(self):
        meanful_items = [
            "VEHICLE_TYPE",
            "DOORS",
            "TRANSMISSION_DRIVELINE",
            "FUEL",
            "STEERING_WHEEL_POSITION",
            "BRAND",
            "BODY_STYLE",
            "NAVIGATION_SYSTEM",
            "Head_Up_Display",
            "Model_Year",
            "FrntDispVariant",
            "FntDispCableLgth",
            "FntClusterCableLgth",
            "FrntUpperDispVariant",
            "HUDSubType",
            "HybridModeSelect",
            "IVIType",
            "IVISIMType",
            "GraceNotes"]
        for elem in self.data:
            for key in meanful_items:
                if (key.lower().replace("_", " ") == elem["name"].lower()):
                    self.meanfulItem.append(elem)
                    #print("name:{0} , mdf:{1} , value:{2}".format(elem["name"], elem["mdf"], elem["val"]))

    def showMeanfulItems(self):
        for elem in self.meanfulItem :
            print( elem )

    # type = id, name , mdf, val
    def showWithFilter(self ,  type , setFilter ):
        print( "PIVI CCF showWithFilter : File:{0} Type:{1} Filter:{2}  ".format( self.filepath, type, setFilter ))
        for elem in self.dataAll :
            for elem_filter in setFilter :
                if( elem[type] == elem_filter ) :
                    print("id:{0} mdf:{1} name:{2} val:{3}".format( (elem["id"]) , hex( elem["mdf"]) , elem["name"] , hex( elem["val"]) ) )

class vbf_dir_parser :
    def __init__(self):
        self.resetmembers()

    def resetmembers(self):
        self.data = []
        self.isLogging_ParseVBF = False
        self.isLogging_SearchingFolder = False
        self.pivi_ccf = None
        self.isSaveToFile = True
        self.fileLog = None
        self.SetUnion = set()
        self.SetIntersect = set()
        self.isOnlyv08v4 = False
        self.isIgnoreZeroValue = True
        self.data = None

    def start(self):
        if( self.isSaveToFile ) :
            self.fileLog = open("save.txt" , "w+")

    def setPiviCCF_dictMdfToVal(self, dictMdfToVal ):
        # type check is required.
        self.dictMdfToVal = dictMdfToVal
        print( self.dictMdfToVal )

    def setPiviCCF_setData(self , data):
        self.data = data

    def search_vbf( self , root_dir, depth = 0 ):
        files = os.listdir(root_dir)
        for file in files:
            file = file.lower()
            path = os.path.join(root_dir, file)
            path = str(path).lower()

            if (os.path.isdir(path)):
                if (False):
                    emptyspace = ""
                    for i in range(0,depth) :
                        emptyspace = emptyspace + " "
                    print( "{0}{1}".format( emptyspace , path ) )
                self.search_vbf(path , depth + 1 )
            else:
                if (self.isLogging_SearchingFolder): print(file)
                split_dir = file.split(".")
                if (self.isLogging_SearchingFolder): print(split_dir)
                if (len(split_dir) != 2):
                    if (self.isLogging_SearchingFolder): print("error in file {}".format(file))
                else:
                    if (self.isLogging_SearchingFolder): print("-")
                    self.vbf_to_dict_array( path , False )


    def searching_dir_condition(self, root_dir, dictFilter ) :
        files = os.listdir(root_dir)
        for file in files:
            file = file.lower()
            path = os.path.join(root_dir, file)
            path = str(path).lower()

            if (os.path.isdir(path)):
                self.searching_dir_condition(path , dictFilter  )
                #print("searching dir {}" , path )
            else:
                split_dir = file.split(".")
                retDictArr = self.ParseVBF( path )
                print("Parse and Matching file {0}".format( path ))
                self.matchFilter( retDictArr , dictFilter )
                return

    def matchFilter( self, retDictArr , dictFilter ):
        try :
            dictMDFs = {}
            for elem in dictFilter:
                dictMDFs[ elem["mdf"] ] = elem["val"]
            #print( "matchDict={}".format( dictMDFs ) )
            for elem in retDictArr:
                mdf_vbf = elem["mdf"]
                val_vbf = elem["val"]
                szSign = "O"
                if( mdf_vbf in dictMDFs.keys() ) :
                    pivi_val = self.dictMdfToVal[ mdf_vbf ]
                    if( val_vbf != pivi_val ) : szSign = "X"
                    print("[{4}] name={0} mdf={1} PIVI:{2}->VBF:{3} ".format( elem["name"] , mdf_vbf , val_vbf , pivi_val ,  szSign ) )
        except:
            print("exception")

    # this is first version of searching and display version
    def vbf_to_dict_array( self , filepath , isShowDiff ):
        dict_skip = {"VIN1","VIN2","VIN3","VIN4","VIN5","VIN6","VIN7","VIN8","VIN9","VIN10","VIN11","VIN12","VIN13","VIN14","VIN15","VIN16","VIN17"}
        try :
            # print( "???={0}".format( filepath ) )
            file_name = os.path.basename(filepath).split(".")[0].lower()
            file_exe = os.path.basename(filepath).split(".")[1].lower()
            split_entry = file_name.split("_")

            if( (file_exe == "vbf") or (file_exe == "zip") or (file_name.split("_")[0] == "release" ) ) :
                if( self.isLogging_ParseVBF == True ) : print( "this is not text file ")
                return

            if( self.isOnlyv08v4 ) :
                if( "v08v4" not in file_name ) : return

            dict_array = []
            if( self.isLogging_ParseVBF == True ) : print(split_entry)
            file_vbf = open( filepath , "r")

            if (self.isSaveToFile == True):
                self.fileLog.write("File:{0}\n".format(filepath))

            setCCF = set()

            score = 0
            isFoundHeader = False
            txt_line = file_vbf.readline()
            while txt_line :
                if( len( txt_line )  == 0 ) : continue
                if( isFoundHeader == False ) :
                    txt_line_copy = txt_line
                    txt_line = file_vbf.readline()
                    split_elems = txt_line_copy.split("\t")
                    #print( split_elems )
                    if( (split_elems[0] == "Frame") and (split_elems[1] == "Byte") and (split_elems[2] == "MDFNum")  ) :
                        isFoundHeader = True
                    continue

                # to avoid Exception ,this is no problem because pivi doesn't use this value
                if( ( "ENGINE" in txt_line ) and ( "TYPE" in txt_line ) ) :
                    txt_line = file_vbf.readline()
                    continue

                if ( (("EnhFiltrationAQI" in txt_line ) ) and ( len(txt_line) < 48 )):
                    # bugs in JLR's vbf
                    txt_line = txt_line.replace("\n" , "-")
                    txt_line = txt_line + file_vbf.readline()
                    split_entry_line = txt_line.split("\t")
                    # if (self.isLogging_ParseVBF == True): print("except val:{0} mdf:{1} name:{2} ".format(split_entry_line[5][48:48 + 2] + split_entry_line[5][51:53].split("\n")[0], 16), (split_entry_line[4], 16), split_entry_line[5][0:48].split("-")[0].replace(" ", "_")) )
                else :
                    split_entry_line = txt_line.split("\t")

                # 1.Frame
                if( self.isLogging_ParseVBF == True ) : print(split_entry_line[0])
                # 2.BYTE
                if( self.isLogging_ParseVBF == True ) : print(split_entry_line[2])
                # 3.MDF
                if( self.isLogging_ParseVBF == True ) : print(split_entry_line[4])
                # 4.Parsing Name : Hueristic method
                if( self.isLogging_ParseVBF == True ) : print( split_entry_line[5][0:48].split("-")[0] )
                # 5.Value
                if( self.isLogging_ParseVBF == True ) : print( split_entry_line[5][48:48+2] + split_entry_line[5][51:53].split("\n")[0] )
                if( self.isLogging_ParseVBF == True ) : print("----------")

                dict = {
                    "id": 0 ,
                    "val": int ( split_entry_line[5][48:48+2] + split_entry_line[5][51:53].split("\n")[0] , 16)  ,
                    "mdf": int ( split_entry_line[4] , 16 )  ,
                    "name": split_entry_line[5][0:48].split("-")[0].replace(" " , "_" ) ,
                }

                #Skip List
                if( dict["name"] in dict_skip ) :
                    txt_line = file_vbf.readline()
                    continue

                # found difference
                mdf = dict["mdf"]
                if( (mdf in self.dictMdfToVal.keys()) and (self.dictMdfToVal[ mdf ] != dict["val"]) ) :
                    if( (self.isIgnoreZeroValue == False) or ( (self.isIgnoreZeroValue == True) and (self.dictMdfToVal[ mdf ] != 0) ) ):
                        score = score + 1
                        #if( self.isSaveToFile == True ) : self.fileLog.write( "\t mdf:{0} name:{1} -> dict{2} =/= vbf{3}\n ".format(  dict["mdf"] , dict["name"] , self.dictMdfToVal[ dict["mdf"] ] , dict["val"] ) )
                        if (isShowDiff == True): print(" mdf:{0} name:{1} // dict({2}) vbf({3}) ".format(hex(dict["mdf"]), dict["name"],self.dictMdfToVal[dict["mdf"]],dict["val"]))
                        setCCF.add( mdf )
                # read next line
                txt_line = file_vbf.readline()

            print( "{0}\tScore:\t{1} ".format(filepath ,score))
            if (self.isSaveToFile == True): self.fileLog.write("\t Score{0}\n ".format(score))

            self.SetUnion = self.SetUnion.union( setCCF )
            if( len( self.SetIntersect ) == 0 ) : self.SetIntersect = self.SetIntersect.union(setCCF)
            else : self.SetIntersect = self.SetIntersect.intersection(setCCF)

        except Exception as b:
            print( " except in [{0}][{1} ".format(filepath , b))
            print( " readline = {0}".format(txt_line))

    # this is second version of vbf
    def ParseVBF( self , filepath ):
        try :
            # checking name
            file_name = os.path.basename(filepath).split(".")[0].lower()
            file_exe = os.path.basename(filepath).split(".")[1].lower()
            split_entry = file_name.split("_")

                # skipping condition
                    # vbf file
            if( (file_exe == "vbf") or (file_exe == "zip") or (file_name.split("_")[0] == "release" ) ) :
                return

            if( self.isOnlyv08v4 ) :
                if( "v08v4" not in file_name ) :
                    return

            dict_array = []
            file_vbf = open( filepath , "r")

            isFoundHeader = False
            txt_line = file_vbf.readline()
            while txt_line :
                # skipping header
                if( len( txt_line )  == 0 ) : continue
                if( isFoundHeader == False ) :
                    txt_line_copy = txt_line
                    txt_line = file_vbf.readline()
                    split_elems = txt_line_copy.split("\t")
                    #print( split_elems )
                    if( (split_elems[0] == "Frame") and (split_elems[1] == "Byte") and (split_elems[2] == "MDFNum")  ) :
                        isFoundHeader = True
                    continue

                # handling exception
                if( ( "ENGINE" in txt_line ) and ( "TYPE" in txt_line ) ) :
                    txt_line = file_vbf.readline()
                    continue

                if ( (("EnhFiltrationAQI" in txt_line ) ) and ( len(txt_line) < 48 )):
                    # bugs in JLR's vbf
                    txt_line = txt_line.replace("\n" , "-")
                    txt_line = txt_line + file_vbf.readline()
                    split_entry_line = txt_line.split("\t")
                    # if (self.isLogging_ParseVBF == True): print("except val:{0} mdf:{1} name:{2} ".format(split_entry_line[5][48:48 + 2] + split_entry_line[5][51:53].split("\n")[0], 16), (split_entry_line[4], 16), split_entry_line[5][0:48].split("-")[0].replace(" ", "_")) )
                else :
                    split_entry_line = txt_line.split("\t")

                dict = {
                    "id": 0 ,
                    "val": int ( split_entry_line[5][48:48+2] + split_entry_line[5][51:53].split("\n")[0] , 16)  ,
                    "mdf": int ( split_entry_line[4] , 16 )  ,
                    "name": split_entry_line[5][0:48].split("-")[0].replace(" " , "_" ) ,
                }
                dict_array.append( dict )
                txt_line = file_vbf.readline()
            return dict_array

        except Exception as b:
            print( " except in [{0}][{1} ".format(filepath , b))
            print( " readline = {0}".format(txt_line))



filter1 = { "VEHICLE_TYPE" , "DOORS" , "TRANSMISSION_DRIVELINE" ,"STEERING_WHEEL_POSITION	" , "IMCAPIXVideoSettings" , "GEARBOX_TYPE",  "BRAND" , "NAVIGATION_SYSTEM" , "FrntDispVariant" , "FrontAVIOPanel" , "NAVIGATION_SYSTEM" , "USB2Hub" ,
            "FntDispCableLgth" , "FntClusterCableLgth"  , "FrntLowerDispVariant" , "FrntUpperDispVariant" , "IVIType" , "IVISIMType" , "IVIWiFiHotspot" ,
            "IVIAPIXClusterComms" ,"MLASoftSwitches" , "PHONEPROJECTION_VER"  }

filter_zero = { "FntUIPCableLgth" , "NAVI_HIBERNATED" , "IVIClusterImgType" , "FrontConnectSocket"}

if True :
    pp_ccf_path = "D:\\work\\rpt\\20220525_corvus_gwm_update\\Ccf_PIVI\\pp_yoonchoi\\ccf.txt"
    pivi_ccf = pivi_ccf()
    pivi_ccf.load( pp_ccf_path )
    if False :
        pivi_ccf.showMap(); # show data --> PASS
        pivi_ccf.showCompareMap() # show mdf to val --> PASS
        print( pivi_ccf.dictMdfToName ) # show mdf to name --> PASS
        pivi_ccf.showWithFilter( "name" , filter1 ) # show filter with name
        pivi_ccf.showWithFilter("name", filter_zero ) # show filter with name , zero value

    FilterDiag = {
        "IVIType",
        "NAVIGATION_SYSTEM",
        "HibernatedNavSys",
        "NGISubscriptionVerMSB",
        "NGISubscriptionVerLSB",
        "IVISIMType",
        "FrntLowerDispVariant",
        "FntClusterCableLgth",
        "FREQUENCY_BAND_STEP_RADIO",
        "NGINLIDigRadRecSys",
        "FrontAVIOPanel",
        "FrontConnectSocket",
        "USB2Hub",
        "SWPhaseIdentifier",
        "IVIType",
        "Gracenotes"
    }
    FilterExtra = {
        "BRAND", "ROOF_TYPE","BODY_STYLE","SUSPENSION"
    }

    filterPP = {"Connect_and_View",
                "NAVIGATION_SYSTEM",
                "VOICE_CONTROL",
                "BLUETOOTH_HANDSFREE",
                "FrntDispVariant",
                "FrntLowerDispVariant",
                "FrntUpperDispVariant",
                "FrontAVIOPanel",
                "BRAND",
                "GEARBOX_TYPE",
                "STEERING_WHEEL_POSITION",
                "HybridType",
                "FUE",
                "ChargingInlet1",
                "ChargingInlet2",
                "VEHICLE_TYPE",
                "IVIType",
                "HibernatedNavSys",
                "DOORS"
                }
    if False :
        pivi_ccf.query( "mdf" , { 0x5f67 } )
        pivi_ccf.query( "name", FilterDiag )
        print("\n")
        pivi_ccf.query("name", FilterExtra)
        print("PP\n")
        pivi_ccf.query("name", filterPP)

    pivi_ccf.query("name", filterPP)

    dictArrPP_inPivi =  pivi_ccf.query("name", filterPP)
    print( dictArrPP_inPivi )

if False :
    # Single Target
    parser = vbf_dir_parser()
    parser.setPiviCCF_dictMdfToVal(pivi_ccf.dictMdfToVal)
    testfile = "D:\\work\\rpt\\20220525_corvus_gwm_update\\CCF_review\\IP33_ccfs\\L663\\L663\\VBF\\21MY\\21MY_L663_Without_RSE_ICE_12-02-2021\ICE\\Without_RSE\\600_L663_UKA_PIVI_RIG_CCF\\600L663UKASV08v4.txt"
    # except in [d:\work\rpt\20220525_corvus_gwm_update\ccf_review\ip33_ccfs\l663\l663\vbf\22my\22my_l663_without_rse_swb_ice_22-10-2021\swb\without_rse\627_l663_kou_pivi_rig_ccf\627l663kousv08v4.txt]
    # [invalid literal for int() with base 16: '' readline = 7E		3		0x7E33	EnhFiltrationAQI
    exceptfile1 = "d:\\work\\rpt\\20220525_corvus_gwm_update\\ccf_review\\ip33_ccfs\\l663\\l663\\vbf\\22my\\22my_l663_without_rse_swb_ice_22-10-2021\\swb\\without_rse\\627_l663_kou_pivi_rig_ccf\\627l663kousv08v4.txt"
    parser.vbf_to_dict_array( exceptfile1 )
elif False :

    root_dir_l663 = "D:\\work\\rpt\\20220525_corvus_gwm_update\\CCF_review\\IP33_ccfs\\L663\\L663\\VBF"

    root_dir_l663_my20 = "D:\\work\\rpt\\20220525_corvus_gwm_update\\DQA_VBF\\L663_20MY\\CCF\\VBF\\L663\\20MY"
    #D:\work\rpt\20220525_corvus_gwm_update\DQA_VBF\L663_20MY\CCF\VBF\L663\20MY\Archives
    root_dir_l663_my20_archive = "D:\\work\\rpt\\20220525_corvus_gwm_update\\DQA_VBF\\L663_20MY\\CCF\\VBF\\L663\\20MY\\Archives"

    parser = vbf_dir_parser()
    parser.setPiviCCF_dictMdfToVal( pivi_ccf.dictMdfToVal )
    parser.start()
    parser.search_vbf( root_dir_l663_my20 )

    if False :
        print( parser.SetUnion )
        print( parser.SetIntersect )
    if True :
        print("\nUnion\n")
        for elem in parser.SetUnion :
            print( "mdf:{0} / name:{1}".format( hex(elem) ,  pivi_ccf.dictMdfToName[elem] ) )
        print("\nIntersect\n")
        for elem in parser.SetIntersect :
            print( "mdf:{0} / name:{1}".format( hex(elem) ,  pivi_ccf.dictMdfToName[elem] ) )

elif False :
    #print( pivi_ccf.dictMdfToVal[0x5f67] )

    parser = vbf_dir_parser()
    parser.setPiviCCF_dictMdfToVal( pivi_ccf.dictMdfToVal )
    parser.start()
    file = "d:\\work\\rpt\\20220525_corvus_gwm_update\\ccf_review\\ip33_ccfs\\l663\\l663\\vbf\\23my\\23my_l663_without_rse_midline_ice_23-12-2021\\midline\\without_rse\\600_l663_ukp_pivi_rig_ccf\\600l663ukpsv08v4.txt"

    file_19my_file = "d:\\work\\rpt\\20220525_corvus_gwm_update\\dqa_vbf\\l663_20my\\ccf\\vbf\\l663\\20my\\archives\\20my_l663_ice_highline_hud_20-06-2019\\ice_highline_hud\\without_rse\\600_l663_uka_pivi_rig_ccf\\600l663ukasv08v4.txt"
    parser.vbf_to_dict_array( file_19my_file , True )

elif True :

    file_19my_file = "D:\\work\\rpt\\20220525_corvus_gwm_update\\Vbf\\IP31_CCF\\L663\\L663\\VBF"

    parser = vbf_dir_parser()
    parser.setPiviCCF_dictMdfToVal(pivi_ccf.dictMdfToVal)
    parser.setPiviCCF_setData( pivi_ccf.dataAll )

    parser.searching_dir_condition( file_19my_file , dictArrPP_inPivi )

#PLAN PIVI에서 0이 아닌 CCF 목록만