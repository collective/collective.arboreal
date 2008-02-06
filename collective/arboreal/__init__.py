from Products.CMFCore.utils import ToolInit
from Products.Arboreal.arboreal import Arboreal
from Products.CMFCore import utils, permissions, DirectoryView

from Products.Arboreal.config import *

DirectoryView.registerDirectory('skins', GLOBALS)
DirectoryView.registerDirectory('skins/arboreal', GLOBALS)


def initialize(context):
    # initialize tree management tool
    utils.ToolInit(TOOL_NAME,
                   tools=[Arboreal],
                   icon='arboreal.gif').initialize( context )
    
    # cImport the multipath index so it is registered
    import index
    import arborealselection 
    context.registerClass(index.MultiPathIndex,
        permission='Add Pluggable Index',
        constructors=(index.manage_addMultiPathIndexForm,
                      index.manage_addMultiPathIndex),
        icon='zmi/index.gif',
        visibility=None
     )
