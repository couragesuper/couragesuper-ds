# for XML
from xml.etree import ElementTree as ET

def Load( ) :
    xmltree = ET.parse( self.configFileName )
                    # access top xml node
    xmlroot = xmltree.getroot()
    if (xmlroot == None):
        print("[Error] UI Configuration Files doesn't have root node.")
        return 1

    for menus in xmlroot:
        # Menus
        nameMenus = menus.attrib['name']
        self.mapMenuItem[ nameMenus ] = menubar.addMenu( nameMenus )
        self.mapToolbar[nameMenus] = self.addToolBar(nameMenus)
        #print("{}".format(menus.attrib))
        for menu in menus:
            #make action & add menus
            nameMenu = menu.attrib['name']
            self.mapActions[ nameMenu ] = QAction(QIcon( "image\\" + menu.attrib['resource'] ), menu.attrib['name_short'], self)
            self.mapActions[ nameMenu ].setShortcut( menu.attrib['shortcut'] )
            self.mapActions[ nameMenu ].setStatusTip( menu.attrib['desc'])
            self.mapMenuItem[nameMenus].addAction( self.mapActions[ nameMenu ] )
            #add toolbar
            self.mapToolbar[nameMenus].addAction( self.mapActions[ nameMenu ] )

# iterative 2 depth nodes

class XML_Helper :

    def __init__(self , xml_name , isdebug):

        self.isdebug = isdebug
        # Tree
        self.xmlTree = ET.parse( xml_name )
        # Root
        self.xmlRootNode = self.xmlTree.getroot()
        # Nodes
        self.xmlNodes = [ node for node in self.xmlRootNode ]
        # Nodes_Nodes

        if(self.isdebug) :
            print( self.xmlRootNode )
            print( self.xmlRootNode.attrib )
            for elem in self.xmlRootNode :
                print( elem.attrib )

xml_helper = XML_Helper( "Test.xml" , True )

