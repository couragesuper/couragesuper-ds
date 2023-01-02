# original source for Convert tool between mysql and sqlite

import sys
import os

sys.path.append("../../Common")
from Mysql.libmysql import dbConMysql
import sqlite3
import urllib

from xml.etree import ElementTree as ET

# convertor mysql to sqlite
# ver 20230102

dbName_Bible = "bible_20230102.db"

print("sqlite3.version:{}".format(sqlite3.version))
print("sqlite3.sqlite_version:{}".format(sqlite3.sqlite_version))


def Loader_Config ( xmlfile ) :
    print( "DavidLab FlaskServer Config" )
    subTag = "Loader_Config"
    # check xml file
    config = {}
    xmltree = ET.parse( xmlfile )
    xmlroot = xmltree.getroot()
    if (xmlroot == None):
        print(subTag, "E", "Root node error.")
        exit(0)
    for node in xmlroot:
        #print( "tag = {}".format(node.tag))
        if ( node.tag == "Queries" ) :
            dictData = {}
            for sub_node in node :
                data = {}
                data['k'] = sub_node.attrib['k']
                data['c'] = sub_node.attrib['c']
                data['r'] = sub_node.attrib['r']
                data['u'] = sub_node.attrib['u']
                data['insert'] = True if sub_node.attrib['insert'] == 'True' else False

                #print( "sub_node={}".format( sub_node.attrib ) )
                dictData[ data['k'] ] = (data)
            config['queries'] = dictData
        elif (node.tag == "DB"):
            #print( "DB={}".format( node.attrib)  )
            data = {}
            for k, v in node.attrib.items() :
                if( k == 'raise_on_warnings') :
                    if( v == 'TRUE') : data[k] = True
                    else : data[k] = False
                else : data[k] = v
            config['db'] = data
    print( "config={}".format( config ) )
    return config;

conv_rule = Loader_Config("Config.xml")
print( "conv_rule:{}\m".format( conv_rule ) )
print( "conv_rule / user : {} , password: {} , host: {} , database:{}\n" .format( conv_rule['db']['user'],conv_rule['db']['password'],conv_rule['db']['host'],conv_rule['db']['database'] ) )

config_db = {'user': conv_rule['db']['user'], 'password': conv_rule['db']['password'], 'host': conv_rule['db']['host'], 'database': conv_rule['db']['database'],
            'raise_on_warnings': True}

db_bible = dbConMysql(config_db)

if os.path.exists( dbName_Bible ) : os.remove( dbName_Bible )
sqlite_bible = sqlite3.connect( dbName_Bible )

with sqlite_bible:
    # sqlite cursor
    cursor = sqlite_bible.cursor()
    print( "conv_rule keys: {}".format( conv_rule['queries'].keys() ) )
    for query in conv_rule['queries'].keys():
        #print("query : {}".format(query))
        print("query {}={}".format(query, conv_rule['queries'][query]))
        cursor.execute( conv_rule['queries'][query]['c'] )
        cnt = 0
        if( conv_rule['queries'][query]['insert'] == True ) :

            # pull data from mysql server
            ret = db_bible.selectQueryWithRet( conv_rule['queries'][query]['r'] )
            for elem in ret['data'] :
                try :
                    for elem_field in elem.keys():
                        # handle string field
                        if (type(elem[elem_field]) == str):
                            elem[elem_field] = elem[elem_field].replace('"', '""')
                    cursor.execute( conv_rule['queries'][query]['u'].format(**elem) )
                    cnt = cnt + 1
                except Exception as e:
                    print("\t\t\t\t[Exception] query = {}".format(conv_rule['queries'][query]['u'].format(**elem)))
        print("query = {} cnt = {}".format( query , cnt ))
    sqlite_bible.commit()
exit(0)
