import os


# Function

# Loader PIVI CCF
# 1) making compare list
# dict : mdf / value

# Parsing Manager
# 1) Single File
# Compute Difference Distance
# Change List

# 2) Iteration Functino
# making Score List
# making Change Lists
# union set / intersect set

# 20220624
# Comparing VBF and VBF


class pivi_ccf:
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

    def load(self, file_path):
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
                "id": int(split_arr[0]),
                "val": int(split_arr[1], 16),
                "mdf": int(split_arr[2], 16),
                "name": split_arr[3]
            }
            self.dictMdfToName[dict_elem["mdf"]] = dict_elem["name"]
            self.dataAll.append(dict_elem)
            if ((self.removeZeroval == False) or ((self.removeZeroval == True) )):
                self.data.append(dict_elem)
                self.dictMdfToVal[dict_elem["mdf"]] = dict_elem["val"]
            line = file_txt.readline()

    def remove_zerovalue(self):
        for elem in self.data:
            if (elem["val"] != 0):
                self.arr_result.append(elem)

    def show_remove_zerovalue(self):
        print(self.arr_result)

    def showCompareMap(self):
        print(self.dictMdfToVal)

    def showMap(self):
        print(self.data)

    def query(self, type, filter):
        dictArray = []
        for elem in self.dataAll:
            key = elem[type]
            if (key in filter):
                #print(" ID:{0} MDF:{1} NAME:{2} VAL:{3} ".format(elem["id"], hex(elem["mdf"]), elem["name"],hex(elem["val"])))
                dictArray.append(elem)
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
                    # print("name:{0} , mdf:{1} , value:{2}".format(elem["name"], elem["mdf"], elem["val"]))

    def showMeanfulItems(self):
        for elem in self.meanfulItem:
            print(elem)

    # type = id, name , mdf, val
    def showWithFilter(self, type, setFilter):
        print("PIVI CCF showWithFilter : File:{0} Type:{1} Filter:{2}  ".format(self.filepath, type, setFilter))
        for elem in self.dataAll:
            for elem_filter in setFilter:
                if (elem[type] == elem_filter):
                    print("id:{0} mdf:{1} name:{2} val:{3}".format((elem["id"]), hex(elem["mdf"]), elem["name"],
                                                                   hex(elem["val"])))


class vbf_dir_parser:
    def __init__(self):
        self.resetmembers()

    # class members
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
        self.isShowHeader = False

    # for filelogger
    def resetSearch(self , logname ):
        self.isShowHeader = False
        try :
            self.fileLog = open( logname + ".csv" , "w" )
        except Exception as e :
            print( "Exception in resetSearch={}".format(e) )

    # Not using
    def start(self):
        if (self.isSaveToFile):
            self.fileLog = open("save.txt", "w+")

    # setters
        # pivi's DicttoVal to compare
    def setPiviCCF_dictMdfToVal(self, dictMdfToVal):
        # type check is required.
        self.dictMdfToVal = dictMdfToVal
        #print(self.dictMdfToVal)

        # pivi's All Data to compare
    def setPiviCCF_setData(self, data):
        self.data = data

    # searching
        # 1. obsolete
    def search_vbf(self, root_dir, depth=0):
        files = os.listdir(root_dir)
        for file in files:
            file = file.lower()
            path = os.path.join(root_dir, file)
            path = str(path).lower()

            if (os.path.isdir(path)):
                if (False):
                    emptyspace = ""
                    for i in range(0, depth):
                        emptyspace = emptyspace + " "
                    print("{0}{1}".format(emptyspace, path))
                self.search_vbf(path, depth + 1)
            else:
                if (self.isLogging_SearchingFolder): print(file)
                split_dir = file.split(".")
                if (self.isLogging_SearchingFolder): print(split_dir)
                if (len(split_dir) != 2):
                    if (self.isLogging_SearchingFolder): print("error in file {}".format(file))
                else:
                    if (self.isLogging_SearchingFolder): print("-")
                    self.vbf_to_dict_array(path, False)

        # 2. compare pivi's ccf and vbfs in folders
    def searching_dir_condition(self, root_dir, dictFilter):
        files = os.listdir(root_dir)
        #print( files )
        for file in files:
            file = file.lower()
            path = os.path.join(root_dir, file)
            path = str(path).lower()

            if (os.path.isdir(path)):
                self.searching_dir_condition(path, dictFilter)
                #print("searching dir {}".format( path ) )
            else:
                #print("searching file {}".format(path))
                split_dir = file.split(".")
                retDictArr = self.ParseVBF(path)
                if type(retDictArr) is list:
                    score , header, rpt_str = self.matchFilter(retDictArr, dictFilter)
                    if( self.isShowHeader == False ) :
                        self.isShowHeader =True
                        print( header )
                        self.fileLog.write( header.replace("\t",",") + "\n" )
                    szOut = "{0}\t{1}\t{2} ".format(path , score , rpt_str )
                    print( szOut )
                    self.fileLog.write( szOut.replace("\t",",") +"\n" )

    # maching function
        # arg 1 : VBF's dict
        # arg 2 : filter data
    def matchFilter(self, retDictArr, dictFilter):
        dictMDFs = {}
        count = 0
        score = 0
        szDiffStr = ""
        szDiffField = ""
        szFields = ""

        szHeader_pri = "File\tScore\tDiffEntry\t"
        szHeader_sec = "File\tScore\tDiffEntry\t"

        for elem in dictFilter:
            dictMDFs[elem["mdf"]] = elem["val"]

        for elem in retDictArr:
            try:
                mdf_vbf = elem["mdf"]
                val_vbf = elem["val"]
                szSign = "O"
                if (mdf_vbf in dictMDFs.keys()):
                    # Add Header
                    szHeader_pri = szHeader_pri + "ret\t" + elem["name"] + "\t"
                    szHeader_sec = szHeader_sec + "ret\t" + "0x{}\t".format(hex(mdf_vbf))
                    #print("{}-{}-{}".format(mdf_vbf, val_vbf, szSign))
                    count = count + 1
                    pivi_val = self.dictMdfToVal[mdf_vbf]
                    if (val_vbf != pivi_val):
                        szSign = "X"
                        score = score + 1
                        #print("[{5}] [{4}] name={0} mdf=0x{1} PIVI:0x{2}->VBF:0x{3} ".format(elem["name"], hex(mdf_vbf), hex(val_vbf), hex(pivi_val),szSign, count)) # 3
                        szDiffField = szDiffField + "/" + elem["name"] + "(0x" + str(hex(mdf_vbf)) +")"
                    szFields = szFields + "{0}\tP:{1}/V:{2}\t".format(szSign,hex(pivi_val),hex(val_vbf))
                    #szDiffStr = szDiffStr + "[{5}] [{4}] {0}:(0x{1}) PIVI:(0x{2})VBF:(0x{3})\t".format(elem["name"], hex(mdf_vbf), hex(val_vbf), hex(pivi_val),szSign, count) # 2
                    #szDiffStr = szDiffStr + "[{4}] {0}:(0x{1}) PIVI:(0x{2})VBF:(0x{3})\t".format(elem["name"],hex(mdf_vbf),hex(val_vbf),hex(pivi_val),szSign) # 1
            except Exception as e:
                print(" except >>{} ".format( e ) )
        return score , szHeader_pri + "\n" + szHeader_sec   , szDiffField + "," + szFields

    # show all difference
        # target : pivi @ vbf
    def match(self, retDictArr ):
        szFields = ""

        for elem in retDictArr:
            try:
                mdf_vbf = elem["mdf"]
                val_vbf = elem["val"]
                if ( mdf_vbf in self.dictMdfToVal.keys() ):
                    pivi_val = self.dictMdfToVal[mdf_vbf]
                    szSign = "O"
                    if (val_vbf != pivi_val):
                        szSign = "X"
                        szFields = szFields + elem["name"] + "(0x" + str(hex(mdf_vbf)) +")" + "\t" +  "{0}\tP:{1}/V:{2}\t".format(szSign,hex(pivi_val),hex(val_vbf)) + "\n"
            except Exception as e:
                print(" except >>{} ".format( e ) )
        print( szFields )

    def match_showall(self, retDictArr ):
        szFields = ""
        cntMatch = 0
        cntNotMatch = 0

        for elem in retDictArr:
            try:
                mdf_vbf = elem["mdf"]
                val_vbf = elem["val"]
                if ( mdf_vbf in self.dictMdfToVal.keys() ):
                    pivi_val = self.dictMdfToVal[mdf_vbf]
                    szSign = "O"
                    if (val_vbf != pivi_val):
                        szSign = "X"
                        cntNotMatch  = cntNotMatch + 1
                    else :
                        cntMatch = cntMatch + 1
                    szFields = szFields + elem["name"] + "(0x" + str(hex(mdf_vbf)) +")" + "\t" +  "{0}\tP:{1}/V:{2}\t".format(szSign,hex(pivi_val),hex(val_vbf)) + "\n"
            except Exception as e:
                print(" except >>{} ".format( e ) )
        print( "Count of match:{} , Count of not match: {}".format( cntMatch, cntNotMatch))
        print( szFields )


    # this is first version of searching and display version
    def vbf_to_dict_array(self, filepath, isShowDiff):
        dict_skip = {"VIN1", "VIN2", "VIN3", "VIN4", "VIN5", "VIN6", "VIN7", "VIN8", "VIN9", "VIN10", "VIN11", "VIN12",
                     "VIN13", "VIN14", "VIN15", "VIN16", "VIN17"}
        try:
            file_name = os.path.basename(filepath).split(".")[0].lower()
            file_exe = os.path.basename(filepath).split(".")[1].lower()
            split_entry = file_name.split("_")

            if ((file_exe == "vbf") or (file_exe == "zip") or (file_name.split("_")[0] == "release")):
                if (self.isLogging_ParseVBF == True): print("this is not text file ")
                return

            if (self.isOnlyv08v4):
                if ("v08v4" not in file_name): return

            dict_array = []
            if (self.isLogging_ParseVBF == True): print(split_entry)
            file_vbf = open(filepath, "r")

            if (self.isSaveToFile == True):
                self.fileLog.write("File:{0}\n".format(filepath))

            setCCF = set()

            score = 0
            isFoundHeader = False
            txt_line = file_vbf.readline()
            while txt_line:
                if (len(txt_line) == 0): continue
                if (isFoundHeader == False):
                    txt_line_copy = txt_line
                    txt_line = file_vbf.readline()
                    split_elems = txt_line_copy.split("\t")
                    # print( split_elems )
                    if ((split_elems[0] == "Frame") and (split_elems[1] == "Byte") and (split_elems[2] == "MDFNum")):
                        isFoundHeader = True
                    continue

                # to avoid Exception ,this is no problem because pivi doesn't use this value
                if (("ENGINE" in txt_line) and ("TYPE" in txt_line)):
                    txt_line = file_vbf.readline()
                    continue

                if ((("EnhFiltrationAQI" in txt_line)) and (len(txt_line) < 48)):
                    # bugs in JLR's vbf
                    txt_line = txt_line.replace("\n", "-")
                    txt_line = txt_line + file_vbf.readline()
                    split_entry_line = txt_line.split("\t")
                    # if (self.isLogging_ParseVBF == True): print("except val:{0} mdf:{1} name:{2} ".format(split_entry_line[5][48:48 + 2] + split_entry_line[5][51:53].split("\n")[0], 16), (split_entry_line[4], 16), split_entry_line[5][0:48].split("-")[0].replace(" ", "_")) )
                else:
                    split_entry_line = txt_line.split("\t")

                # 1.Frame
                if (self.isLogging_ParseVBF == True): print(split_entry_line[0])
                # 2.BYTE
                if (self.isLogging_ParseVBF == True): print(split_entry_line[2])
                # 3.MDF
                if (self.isLogging_ParseVBF == True): print(split_entry_line[4])
                # 4.Parsing Name : Hueristic method
                if (self.isLogging_ParseVBF == True): print(split_entry_line[5][0:48].split("-")[0])
                # 5.Value
                if (self.isLogging_ParseVBF == True): print(
                    split_entry_line[5][48:48 + 2] + split_entry_line[5][51:53].split("\n")[0])
                if (self.isLogging_ParseVBF == True): print("----------")

                dict = {
                    "id": 0,
                    "val": int(split_entry_line[5][48:48 + 2] + split_entry_line[5][51:53].split("\n")[0], 16),
                    "mdf": int(split_entry_line[4], 16),
                    "name": split_entry_line[5][0:48].split("-")[0].replace(" ", "_"),
                }

                # Skip List
                if (dict["name"] in dict_skip):
                    txt_line = file_vbf.readline()
                    continue

                # found difference
                mdf = dict["mdf"]
                if ((mdf in self.dictMdfToVal.keys()) and (self.dictMdfToVal[mdf] != dict["val"])):
                    if ((self.isIgnoreZeroValue == False) or (
                            (self.isIgnoreZeroValue == True) and (self.dictMdfToVal[mdf] != 0))):
                        score = score + 1
                        # if( self.isSaveToFile == True ) : self.fileLog.write( "\t mdf:{0} name:{1} -> dict{2} =/= vbf{3}\n ".format(  dict["mdf"] , dict["name"] , self.dictMdfToVal[ dict["mdf"] ] , dict["val"] ) )
                        if (isShowDiff == True): print(
                            " mdf:{0} name:{1} // dict({2}) vbf({3}) ".format(hex(dict["mdf"]), dict["name"],self.dictMdfToVal[dict["mdf"]],dict["val"]))
                        setCCF.add(mdf)
                # read next line
                txt_line = file_vbf.readline()

            print("{0}\tScore:\t{1} ".format(filepath, score))
            if (self.isSaveToFile == True): self.fileLog.write("\t Score{0}\n ".format(score))

            self.SetUnion = self.SetUnion.union(setCCF)
            if (len(self.SetIntersect) == 0):
                self.SetIntersect = self.SetIntersect.union(setCCF)
            else:
                self.SetIntersect = self.SetIntersect.intersection(setCCF)

        except Exception as b:
            print(" except in [{0}][{1} ".format(filepath, b))
            print(" readline = {0}".format(txt_line))

    # this is second version of vbf
    def ParseVBF(self, filepath):
        try:
            # checking name
            file_name = os.path.basename(filepath).split(".")[0].lower()
            file_exe = os.path.basename(filepath).split(".")[1].lower()
            split_entry = file_name.split("_")

            # skipping condition
            # vbf file
            if ((file_exe == "vbf") or (file_exe == "zip") or ("release" in file_name.split("_"))):
                #print("ParseVBF...Returned 1")
                return

            if (self.isOnlyv08v4):
                if ("v08v4" not in file_name):
                    #print("ParseVBF...Returned 1")
                    return

            dict_array = []
            file_vbf = open(filepath, "r")

            isFoundHeader = False
            txt_line = file_vbf.readline()
            while txt_line:
                # skipping header
                if (len(txt_line) == 0): continue
                if (isFoundHeader == False):
                    txt_line_copy = txt_line
                    txt_line = file_vbf.readline()
                    split_elems = txt_line_copy.split("\t")
                    #print( split_elems )
                    if ((split_elems[0] == "Frame") and (split_elems[1] == "Byte") and (split_elems[2] == "MDFNum")):
                        isFoundHeader = True
                    continue

                # handling exception
                if (("ENGINE" in txt_line) and ("TYPE" in txt_line)):
                    txt_line = file_vbf.readline()
                    continue

                if ((("EnhFiltrationAQI" in txt_line)) and (len(txt_line) < 48)):
                    # bugs in JLR's vbf
                    txt_line = txt_line.replace("\n", "-")
                    txt_line = txt_line + file_vbf.readline()
                    split_entry_line = txt_line.split("\t")
                    # if (self.isLogging_ParseVBF == True): print("except val:{0} mdf:{1} name:{2} ".format(split_entry_line[5][48:48 + 2] + split_entry_line[5][51:53].split("\n")[0], 16), (split_entry_line[4], 16), split_entry_line[5][0:48].split("-")[0].replace(" ", "_")) )
                else:
                    split_entry_line = txt_line.split("\t")

                dict = {
                    "id": 0,
                    "val": int(split_entry_line[5][48:48 + 2] + split_entry_line[5][51:53].split("\n")[0], 16),
                    "mdf": int(split_entry_line[4], 16),
                    "name": split_entry_line[5][0:48].split("-")[0].replace(" ", "_"),
                }
                dict_array.append(dict)
                txt_line = file_vbf.readline()
            #print("Returned...1")
            return dict_array

        except Exception as b:
            print(" except in [{0}][{1} ".format(filepath, b))
            print(" readline = {0}".format(txt_line))

    def match_VBF_and_VBF(self , vbf1_path , vbf2_path , filter ):
        vbf_data1 = self.ParseVBF(vbf1_path)
        vbf_data2 = self.ParseVBF(vbf2_path)
        self.compare_VBF_and_VBF( vbf_data1, vbf_data2 , filter)

    def compare_VBF_and_VBF(self, vbf_data1, vbf_data2 , dictFilter ):
        keys = dictFilter.keys()
        try :
            for elem1 in vbf_data1:
                if elem1["mdf"] in keys :
                    for elem2 in vbf_data2 :
                        if elem1["mdf"] == elem2["mdf"] :
                            if elem1["val"] != elem2["val"] :
                                print(" (Not matched)  MDF:{0} Name:{1}/{2} VAL:{3}/{4}".format( hex(elem1["mdf"]) ,elem1["name"],elem2["name"],elem1["val"],elem2["val"]))
        except Exception as e:
            print(" except >>{} ".format(e))

filter1 = {"VEHICLE_TYPE", "DOORS", "TRANSMISSION_DRIVELINE", "STEERING_WHEEL_POSITION	", "IMCAPIXVideoSettings",
           "GEARBOX_TYPE", "BRAND", "NAVIGATION_SYSTEM", "FrntDispVariant", "FrontAVIOPanel", "NAVIGATION_SYSTEM",
           "USB2Hub",
           "FntDispCableLgth", "FntClusterCableLgth", "FrntLowerDispVariant", "FrntUpperDispVariant", "IVIType",
           "IVISIMType", "IVIWiFiHotspot",
           "IVIAPIXClusterComms", "MLASoftSwitches", "PHONEPROJECTION_VER"}

filter_zero = {"FntUIPCableLgth", "NAVI_HIBERNATED", "IVIClusterImgType", "FrontConnectSocket"}

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
    "BRAND", "ROOF_TYPE", "BODY_STYLE", "SUSPENSION"
}

filterPP = {
            "Connect_and_View",
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

# name field has condition it doesn't exist

filterExtra = {
    "Connect_and_View",
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
    "FUEL",
    "ChargingInlet1",
    "ChargingInlet2",
    "VEHICLE_TYPE",
    "IVIType",
    "HibernatedNavSys",
    "DOORS",
    "ROOF_TYPE",
    "BODY_STYLE",
    "SUSPENSION",
    "NGISubscriptionVerMSB",
    "NGISubscriptionVerLSB",
    "IVISIMType",
    "FntClusterCableLgth",
    "FREQUENCY_BAND_STEP_RADIO",
    "NGINLIDigRadRecSys",
    "FrontConnectSocket",
    "USB2Hub",
    "SWPhaseIdentifier",
    "Gracenotes",
    "IMCAPIXVideoSettings"
}

# matching PIVI and CarLine Folder
    # unzip is required
if False:
    ### 1. comparing pivi and vbf folder

    moon_ccf_path = "D:\\work\\rpt\\gwmup\\Ccf_PIVI\\moon\\ccf_l460.txt"
    pp_ccf_path = "d:\\work\\rpt\\gwmup\\Ccf_PIVI\\pp_yoonchoi\\ccf.txt"
    pp_ccf_path_new = "D:\\work\\rpt\\20221017-Gwmup2\\ccf.txt"

    vbf_l663_ip30_file = "d:\\work\\rpt\\gwmup\\Vbf\\IP31_CCF\\L663\\L663\\VBF"
    vbf_l663_ip33_file = "D:\\work\\rpt\\gwmup\\Vbf\\IP33_ccfs\\L663\\L663\\VBF"

    vbf_l460_ip33_file = "D:\\work\\rpt\\gwmup\\Vbf\\IP33_ccfs\\L460\\L460\\VBF"

    # configruation
    build_type = 5
    if build_type == 1 :  # PP/L663
        ccf_path = pp_ccf_path
        vbf_path = vbf_l663_ip33_file
        log_name = "PP_PIVI_VBF_L663_IP33"
    elif build_type == 2 :  #PP/L460
        ccf_path = pp_ccf_path
        vbf_path = vbf_l460_ip33_file
        log_name = "PP_PIVI_VBF_L460_IP33"
    elif build_type == 3:   #MOON/L663
        ccf_path = moon_ccf_path
        vbf_path = vbf_l663_ip33_file
        log_name = "MOON_PIVI_VBF_L663_IP33"
    elif build_type == 4:   #
        ccf_path = moon_ccf_path
        vbf_path = vbf_l460_ip33_file
        log_name = "MOON_PIVI_VBF_L460_IP33"
    elif build_type == 5:   #
        ccf_path = pp_ccf_path_new
        vbf_path = vbf_l663_ip33_file
        log_name = "PPNEW_PIVI_VBF_L660_IP33"
    else :
        print("error")
        exit(0)

    print("VBF Compare between pivi ccf and vbf dir");

    filter = filterExtra

    pivi_ccf = pivi_ccf()
    pivi_ccf.load( ccf_path )

    parser = vbf_dir_parser()
    parser.setPiviCCF_dictMdfToVal(pivi_ccf.dictMdfToVal)

    parser.setPiviCCF_setData(pivi_ccf.dataAll)
    dictArrPP_inPivi = pivi_ccf.query("name", filter)
    parser.resetSearch( log_name )
    parser.searching_dir_condition( vbf_path , dictArrPP_inPivi )
elif True :
    ### 2.single file comapre
    if False :
        pp_ccf_path = "d:\\work\\rpt\\gwmup\\Ccf_PIVI\\pp_yoonchoi\\ccf.txt"
        vbf_path = "D:\\work\\rpt\\gwmup\\Review\\SDSMaker_WIthJLRVBF\\23MY_600L663UKPSV08v4.txt"
    else :
        pp_ccf_path = "D:\\work\\rpt\\1_Progress_IP36\\20221101_GWM_Update\\ccf.txt"
        vbf_path = "D:\\work\\rpt\\1_Progress_IP36\\20221101_GWM_Update\\154X761USSSV12v6.txt"

    # 1. pivi loader
    pivi_ccf = pivi_ccf()
    pivi_ccf.load( pp_ccf_path )

    # 2. vbf parser
    parser = vbf_dir_parser()
    parser.setPiviCCF_dictMdfToVal(pivi_ccf.dictMdfToVal)
    parser.setPiviCCF_setData(pivi_ccf.dataAll)

    # 3. single File
    parser.resetSearch("Dummy")
    vbf_data = parser.ParseVBF(vbf_path)
    parser.match_showall( vbf_data  )
elif False :

    dictFilter = {
        0x2377: "Connect_and_View",
        0x1327: "NAVIGATION_SYSTEM",
        0x1127: "VOICE_CONTROL",
        0x1747: "BLUETOOTH_HANDSFREE",
        0x4363: "FrntDispVariant",
        0x5C53: "FrntLowerDispVariant",
        0x5C57: "FrntUpperDispVariant",
        0x4372: "FrontAVIOPanel",
        0x0977: "BRAND",
        0x0247: "GEARBOX_TYPE",
        0x0227: "STEERING_WHEEL_POSITION",
        0x5687: "HybridType",
        0x0177: "FUEL",
        0x5D43: "ChargingInlet1",
        0x5D47: "ChargingInlet2",
        0x0127: "VEHICLE_TYPE",
        0x6F47: "IVIType",
        0x7F23: "HibernatedNavSys",
        0x0137: "DOORS",
        0x0A47: "ROOF_TYPE",
        0x0A77: "BODY_STYLE",
        0x0B57: "SUSPENSION",
        0x5F47: "NGISubscriptionVerMSB",
        0x5F57: "NGISubscriptionVerLSB",
        0x7482: "IVISIMType",
        0x5987: "FntClusterCableLgth",
        0x1067: "FREQUENCY_BAND_STEP_RADIO",
        0x4837: "NGINLIDigRadRecSys",
        0x8167: "FrontConnectSocket",
        0x5142: "USB2Hub",
        0x4477: "Gracenotes",
        0x5F67: "IMCAPIXVideoSettings"
    }

    vbf_550 = "D:\\work\\rpt\\1_Progress_IP35\\LGEDEV-83689_F000-04_DTC\\L550 BOM18 ADC18\\BOM18 ADC18\\067L550JPJSV16v1.txt"
    vbf_560 = "D:\\work\\rpt\\1_Progress_IP35\\LGEDEV-83689_F000-04_DTC\\L560 BOM18 ADC18\\BOM18 ADC18\\156L560JPJSV16v6.txt"

    parser = vbf_dir_parser()
    parser.match_VBF_and_VBF( vbf_550 , vbf_560 , dictFilter )
