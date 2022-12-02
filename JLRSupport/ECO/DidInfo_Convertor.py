
from xml.etree import ElementTree as ET

didItem = [ 'JLR.UFS.SW.VERSION(ICCM)', 'JLR.IGM.HW.VERSION',
            'JLR.ICCM.HW.VERSION','JLR.RADIO.GRADE.VERSION',
            'JLR.MICOM.FW.VERSION(IGM)','JLR.GRACE.NOTE.VERSION',
            'JLR.VISTEON.VERSION','JLR.APPD.VERSION',
            'JLRBROADCAST.DB.VERSION','JLR.ETHERNET.FIRM.VERSION',.
            'JLR.GPS.VERSION.READ','JLR.DAB.MODULE.VERSION',
            'JLR.HD.MODULE.VERSION','JLR.XM.MODULE.VERSION.READ',
            'JLR.NAVI.VERSIO.READ','JLR.HERE.NAVI.VERSION.READ',
            'JLR.NEUSOFT.NAVI.VERSION.READ','JLR.SKT.NAVI.VERSION.READ','JLR.MAP.VERSION.READ','JLR.HERE.NAVI.MAP.VERSION.READ','JLR.NEUSOFT.NAI.MAP.VERSION.READ','JLR.SKT.NAVI.MAP.VERSION.READ','JLR.SECURE.BOOT.FUSING','JLR.SIM.IMEI.READ','BOUGHT(ICCM)','ASSEMBLY(ICCM)','H/W_PARTNUM(ICCM)','SERIALNUM(ICCM)','ASSMBLY(IGM)','H/W_PARTNUM(IGM)','F188_SW(ICCM)','F188_SW(IGM)','F120_CPU(ICCM)','F120_V850(ICCM)' ];

arrVariants = ['JLR PIVI Diamond Japan (IGCJ1PHE.BJVJ340)',
               'JLR PIVI Diamond RoW w/ DAB (IGCJ1PHE.BRDJ340)',
               'JLR PIVI Diamond NAS (IGCJ1PHN.BNSJ340)',
               'JLR PIVI Diamond CHN (IGCJ1PHC.BCCJ340)',
               'JLR PIVI Diamond w/o DAB (IGCJ1PHE.BRBJ340)',
               'JLR PIVI Diamond CHN (IGCJ1PHC.BCCC340)',
               'JLR PIVI EMC (IGCJ1PHE.BRNJ340)', ]

arrVariants_Fmt = ['JLR PIVI Diamond Japan (IGCJ1PHE.BJVJ{})',
               'JLR PIVI Diamond RoW w/ DAB (IGCJ1PHE.BRDJ{})',
               'JLR PIVI Diamond NAS (IGCJ1PHN.BNSJ{})',
               'JLR PIVI Diamond CHN (IGCJ1PHC.BCCJ{})',
               'JLR PIVI Diamond w/o DAB (IGCJ1PHE.BRBJ{})',
               'JLR PIVI Diamond CHN (IGCJ1PHC.BCCC{})',
               'JLR PIVI EMC (IGCJ1PHE.BRNJ{})', ]

ip_val = "340"
arrVariants = [ "JA" ,"RD" , "NA" ,"CH" , "RO" ,"CH" ,"CH" ]


for elem in arrVariants_Fmt :
    print( elem.format( ip_val ))











