#this is version 1.

# 디렉토리 순회
import os

# entering dir and dir
ismode1 = True
# file
ismode2 = False
# entry split_dir
ismode3 = False
# error file format
ismode4 = False
# non error
ismode5 = False


def print_files_in_dir ( root_dir  ) :
    files = os.listdir( root_dir )
    for file in files:
        file = file.lower()
        path = os.path.join(root_dir ,file)
        path = str( path ).lower()
        #check directory
        if( os.path.isdir( path ) ) :
            if( ismode1 ) : print( "enter dir " , path )
            print_files_in_dir( path )
        else :
            if( ismode2 ) : print( file )
            split_dir = file.split(".")
            if( ismode3 ) : print( split_dir )
            if( len( split_dir ) != 2 ) :
                if( ismode4 ) : print("error in file {}".format( file ))
            else :
                if( ismode5 ) : print("-")
                handle_file( path )

def handle_file( filepath ) :
    #print( "???={0}".format( filepath ) )
    file_name = os.path.basename(filepath).split(".")[0]
    file_exe = os.path.basename( filepath ).split(".")[1]
    split_entry = file_name.split( "_" )
    print( split_entry )

root_dir = "D:\\work\\rpt\\20220525_corvus_gwm_update\\CCF_review\\IP33_ccfs\\L663\\L663\\VBF"

# print( root_dir )
print_files_in_dir ( root_dir  )



