import JLR_UDS_Automation as uds
import time

def Assertion_DO() :
    print( "Assertion_DO={}".format(uds.ASSERTION()) )

repeat = 1000
delay = 0

for i in range(0,repeat) :
    print("\n Test No : {}".format(i))

    uds.ACTION_CONNECT()
    Assertion_DO()

    uds.ACTION_F111()
    Assertion_DO()

    uds.ACTION_F113()
    Assertion_DO()

    uds.ACTION_F188()
    Assertion_DO()

    uds.ACTION_F18C()
    Assertion_DO()

    uds.ACTION_F1BE()
    Assertion_DO()

    uds.ACTION_F1BF()
    Assertion_DO()

    uds.ACTION_EXTSESSION()
    Assertion_DO()

    uds.ACTION_ODST()
    Assertion_DO()

    uds.ACTION_ODST_RET()
    Assertion_DO()

    uds.CLOSE()
    time.sleep( delay )



