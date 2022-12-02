from xml.etree import ElementTree as ET
import threading
import time
from datetime import datetime
import sys
import os

# Project : Descrption Generator
    # 1. Input : ECO_Data.xml
    # 2. Output : Output / Projects.txt

class stopWatch :
    def reset(self) :
        self.start_time = time.time()
    def diff(self):
        return time.time() - self.start_time

class ECO_Desc_Gen :
    def __init__(self):
        self.debug = True
        self.dbgTag = "ECO_GEN"
        self.xmlConfigName = "none"
        self.data = {}

        if False :
            self.arrVariants = ["NAS", "CHINA", "DAB_ow", "DAB_row", "JAPAN", "CHINA(Linechina)", "EMC"]
            self.arrSuffix = ["IGCJ1PHN.BNSJ{}@PGZ.EKHQ", "IGCJ1PHC.BCCJ{}@PGZ.EKHQ", "IGCJ1PHE.BRBJ{}@PGZ.EKHQ",
                              "IGCJ1PHE.BRDJ{}@PGZ.EKHQ", "IGCJ1PHE.BJVJ{}@PGZ.EKHQ", "IGCJ1PHC.BCCC{}@PGZ.EKHQ",
                              "IGCJ1PHE.BRNJ{}@PGZ.EKHQ"]
            self.arrBIN = ["NA", "CH", "RO", "RD", "JA", "CH", "RD"]
        else :
            # reordering
            self.arrVariants = [ "JAPAN" , "DAB_ROW_W" , "NAS" , "CHINA" , "DAB_ROW_WO" , "CHINA_LINECHN" , "EMC" ]
            self.arrSuffix = [ "IGCJ1PHE.BJVJ{}@PGZ.EKHQ" , "IGCJ1PHE.BRDJ{}@PGZ.EKHQ" , "IGCJ1PHN.BNSJ{}@PGZ.EKHQ" ,
                               "IGCJ1PHC.BCCJ{}@PGZ.EKHQ" , "IGCJ1PHE.BRBJ{}@PGZ.EKHQ" , "IGCJ1PHC.BCCC{}@PGZ.EKHQ" ,
                               "IGCJ1PHE.BRNJ{}@PGZ.EKHQ" ]
            self.arrBIN = [ "JA" , "RD" , "NA" , "CH", "RO" , "CH", "RD" ]

        #"JL03{JA}{340}I{C}JLR_{220711}"
        self.fmtBIN = "JL03{}{}I{}JLR_{}"

    def log(self, subTag, level, msg):
        print("[{}][{}][{}][{}] {}".format(datetime.now(), self.dbgTag, subTag, level, msg))

    def loadRule(self , xmlname ):
        subTag = "loadRule"
        self.stopwatch = stopWatch()
        self.xmlConfigName = xmlname
        self.log( subTag, "I" , "config={}".format( self.xmlConfigName ))
        print("\n\n")
        #load config
        xmltree = ET.parse(self.xmlConfigName)
        xmlroot = xmltree.getroot()
        if (xmlroot == None):
            self.log(subTag, "E", subTag , "none of root")
            return False

        #<!-- <INFO IP="340" DATE="220711"/> -->
        #<!-- <NAVI ver="V4.0.5.30_IP34_20220428"  here="HERE_IP34.4.2022.21.39_20220524" skt="SK8.6.V0.22.165A.20220425" neusoft="IP34.navi-JLR_2221.3a_stabilization_jlr_IP34-0-g4f004ff.20220527" /> -->
        #<!-- <UFS size = "128G" SAA="SAA42582501" EBR="EBR34951204" LUN0_CRC="0x801722a3" LUN1_CRC="0xc11443ef" LUN2_CRC="0x32ffc7cf" LUN3_CRC="0xc71daf61" LUN4_CRC="0xe915b438" LUN5_CRC="0xbc7c92dd"/> -->
        #<!-- <MICOM value="SAA42581501" EBR="EBR31472674" BIN= "JL03NA340IGJLR_220711" checksum="0x11B5F562" /> -->
        #<!-- <HD_RADIO SAA="SAA42581501" EBR="EBR31472674" ver = "C0006.003" checksum="EBR31472674" /> -->
        #<!-- <ETHERNET SAA="SAA42581501" EBR="EBR31472674" ver = "v2.6.1.K" checksum="0x1DB33834" /> -->
        #<!-- <GPS SAA="SAA42585201" ver = "v6.09.32" EBR="EBR34968814" /> -->

        # eureka
        for node in xmlroot :
            #self.log(subTag,"I" , "{} : attrib={}".format(node.tag, node.attrib))
            data = {}
            for k,v in node.attrib.items() :
                data[ k ] = v
            self.data[ node.tag ] = data
        self.log(subTag, "I" , "loadrule={}".format(self.data) )

    def gen(self):
        #remove previous files
        path = os.getcwd() + "\\Output"
        list = os.listdir ( path )
        print( list )
        for fileelem in list :
            os.remove( path + "\\" + fileelem )

        subTag ="gen"
        nVar = len( self.arrVariants )
        for iVar in range(0,nVar) :
            text = ""
            suffix = str( self.arrSuffix[iVar] ).format( self.data["INFO"]["IP"])
            suffix_pre = suffix.split("@")[0]
            self.log( subTag , "I" , "variants = {} / suffix = {}".format( self.arrVariants[iVar] , suffix ) )

            #1.Changing Details
            text = text + "1. Changing Details : \n\n{}\n\n".format( suffix_pre )
            #text = text + "UFS 128G : {SAA42582501} / {JL03RD340ICJLR_220711} / LUN0.bin - 0x{801722a3}, LUN1.bin - 0x{c11443ef}, LUN2.bin - 0x{32ffc7cf}, LUN3.bin - 0x{c71daf61}, LUN4.bin - 0x{e915b438}, LUN5.bin - 0x{bc7c92dd}\n"

            binICCM = self.fmtBIN.format( self.arrBIN[iVar] , self.data["INFO"]["IP"] , "C" , self.data["INFO"]["DATE"] )
            binIGM = self.fmtBIN.format( self.arrBIN[iVar] , self.data["INFO"]["IP"] , "G" , self.data["INFO"]["DATE"] )

            text = text + "UFS 128G : {} / {} / LUN0.bin - {}, LUN1.bin - {}, LUN2.bin - {}, LUN3.bin - {}, LUN4.bin - {}, LUN5.bin - {}\n".format(
                self.data["UFS"]["SAA"] , binICCM ,self.data["UFS"]["LUN0_CRC"], self.data["UFS"]["LUN1_CRC"], self.data["UFS"]["LUN2_CRC"],
                self.data["UFS"]["LUN3_CRC"], self.data["UFS"]["LUN4_CRC"], self.data["UFS"]["LUN5_CRC"])

            #text = text + "MICOM : {SAA42581501} / {JL03NA340IGJLR_220711} / checksum:{0x11B5F562} "
            text = text + "MICOM : {} / {} / checksum:{} \n".format( self.data["MICOM"]["SAA"] , binIGM , self.data["MICOM"]["checksum"] )

            # Radio or DAB
            if False :
                if( iVar == 0 ) : # Radio
                    print("Radio")
                    # Flash memory (HD-RADIO) : SAA41305801 / C0006.003 / checksum:0x397372A9
                    #text = text + "Flash memory (HD-RADIO) : {SAA41305801} / {C0006.003} / checksum:{0x397372A9}"
                    text = text + "Flash memory (HD-RADIO) : {} / {} / checksum:{}\n".format( self.data["HD_RADIO"]["SAA"] , self.data["HD_RADIO"]["ver"] , self.data["HD_RADIO"]["checksum"] )
                if( iVar == 3 ) : # DAB
                    print("Dab") # work to do
            else :
                if (iVar == 2):  # Radio
                    print("Radio")
                    # Flash memory (HD-RADIO) : SAA41305801 / C0006.003 / checksum:0x397372A9
                    # text = text + "Flash memory (HD-RADIO) : {SAA41305801} / {C0006.003} / checksum:{0x397372A9}"
                    text = text + "Flash memory (HD-RADIO) : {} / {} / checksum:{}\n".format(
                        self.data["HD_RADIO"]["SAA"], self.data["HD_RADIO"]["ver"], self.data["HD_RADIO"]["checksum"])
                if (iVar == 1):  # DAB
                    print("Dab")
                    # "Flash memory (DAB) : SAA41323101 / CR11.2.5 / checksum:0x3AC1AFA8"
                    text = text + "Flash memory (DAB) : {} / {} / checksum:{}\n".format(
                        self.data["DAB"]["SAA"], self.data["DAB"]["ver"], self.data["DAB"]["checksum"])
                    # To do :

            #Ethernet
            #text = text + "Flash memory (Ethernet Switch) : {SAA41343601} / {v2.6.1.K} / checksum:{0x1DB33834}"
            text = text + "Flash memory (Ethernet Switch) : {} / {} / checksum:{}\n".format( self.data["ETHERNET"]["SAA"] , self.data["ETHERNET"]["ver"] , self.data["ETHERNET"]["checksum"] )

            #GPS
            #text = text + "GPS : SAA42585201 / v6.09.32 / checksum:0x17DD6321
            text = text + "GPS : {} / {} / checksum:{}\n\n".format( self.data["GPS"]["SAA"] ,  self.data["GPS"]["ver"] , self.data["GPS"]["checksum"] )

            # 2. Applicable Models
            text = text + "2. Applicable Models / Assembly : \n\n"

            #text = text + "UFS 128G : SAA42582501 (EBR34951204)\nMICOM : SAA42581501 (EBR31472674)\nFlash memory (HD-RADIO) : SAA41305801 (EBR34969614)\nFlash memory (Ethernet Switch) : SAA41343601 (EBR31472674)\nGPS : SAA42585201 (EBR34968814)\n"
            text = text + "UFS 128G : {} ({})\nMICOM : {} ({})\n".format( self.data["UFS"]["SAA"] , self.data["UFS"]["EBR"], self.data["MICOM"]["SAA"] , self.data["MICOM"]["EBR"] )

            if( iVar == 2 ) : # HD-Radio
                text = text + "Flash memory (HD-RADIO) : {} ({})\n".format( self.data["HD_RADIO"]["SAA"], self.data["HD_RADIO"]["EBR"] )
            elif ( iVar == 1 ) : # DAB
                text = text + "Flash memory (DAB) : {} ({})\n".format( self.data["DAB"]["SAA"], self.data["DAB"]["EBR"] )

            text = text + "Flash memory (Ethernet Switch) : {} ({})\n".format(self.data["ETHERNET"]["SAA"], self.data["ETHERNET"]["EBR"])

            # gps ebr is different
            ebr = "err"
            if( iVar == 0 ) : ebr = self.data["GPS"]["EBR_JAP"]
            elif ( iVar == 1 ): ebr = self.data["GPS"]["EBR_DAB_W"]
            elif ( iVar == 2 ): ebr = self.data["GPS"]["EBR_NAS"]
            elif ( iVar == 3 ): ebr = self.data["GPS"]["EBR_CHN"]
            elif ( iVar == 4 ): ebr = self.data["GPS"]["EBR_ROW_WO"]
            elif ( iVar == 5 ): ebr = self.data["GPS"]["EBR_CHN"]
            elif ( iVar == 6 ): ebr = self.data["GPS"]["EBR_EMC"]
            else : ebr = "ERROR"

            text = text + "GPS : {} ({})\n".format( self.data["GPS"]["SAA"] , ebr )

            #text = text + "3. Remark : \n\nJLR.NAVI.VERSION.READ: \"{V4.0.5.30_IP34_20220428}\" +
            #"JLR.HERE.NAVI.VERSION.READ: \"{HERE_IP34.4.2022.21.39_20220524}\" +
            #"JLR.SKT.NAVI.VERSION.READ: \"{SK8.6.V0.22.165A.20220425}\" +
            #"JLR.NEUSOFT.NAVI.VERSION.READ: \"{IP34.navi-JLR_2221.3a_stabilization_jlr_IP34-0-g4f004ff.20220527}\""

            # 3. Remarks
            text = text + "\n3. Remark : \n\nJLR.NAVI.VERSION.READ: \"{}\"\nJLR.HERE.NAVI.VERSION.READ: \"{}\"\nJLR.SKT.NAVI.VERSION.READ: \"{}\"\nJLR.NEUSOFT.NAVI.VERSION.READ: \"{}\"".format( self.data["NAVI"]["ver"] , self.data["NAVI"]["here"] , self.data["NAVI"]["skt"] , self.data["NAVI"]["neusoft"] )

            print( text )
            print("\n")

            file = open( ".\\Output\\" + suffix_pre + ".txt" , "w")
            file.write( text )
            file.close()

ECOGen = ECO_Desc_Gen()
ECOGen.loadRule("ECO_Data_IP35_605.xml")
ECOGen.gen()


