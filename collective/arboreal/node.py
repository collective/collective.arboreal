from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2

from AccessControl import ClassSecurityInfo

from Globals import InitializeClass
from BTrees.IOBTree import IOBTree

from config import ManageProperties

from Products.CMFPlone.interfaces.NonStructuralFolder import INonStructuralFolder

from OFS.OrderedFolder import OrderedFolder
from OFS.IOrderSupport import IOrderedContainer

class Node(OrderedFolder):
    """A node in a tree.

    The node can contain its children"""
    meta_type = 'ArborealNode'
    __implements__ = (INonStructuralFolder, IOrderedContainer)
    
    security = ClassSecurityInfo()
    
    security.declarePublic("Title")
    def Title(self):
        """Return the node name."""
        return self.title
    
    security.declareProtected(ManageProperties, 'setTitle')
    def setTitle(self, title):
        """Set the title."""
        self.title = title
    
    security.declareProtected(ManageProperties, 'addChild')
    def addChild(self, name, id=None):
        """Create a subnode of this node."""
        if not id:
            id = self.generateUniqueId()
        node = Node(id)
        node.title = name
        self._setObject(id, node)
        return id
    
    security.declarePublic("getNodePath")
    def getNodePath(self):
        """Return the path of the node to the root of the tree."""
        current = self
        path = []
        while current.meta_type==self.meta_type:
            path.append(current.id)
            current = current.aq_parent
        path.reverse()
        return '/'+'/'.join(path)
        

