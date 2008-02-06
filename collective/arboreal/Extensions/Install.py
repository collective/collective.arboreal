from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import manage_addTool
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from Products.Archetypes.atapi import listTypes
from Products.Archetypes.Extensions.utils import install_subskin
from Products.Archetypes.Extensions.utils import installTypes

from StringIO import StringIO
import sys

from Products.Arboreal.config import *

def installCollapsibleTreeCSS(self, out):
    csstool = getToolByName(self, 'portal_css')
    stylesheet_ids = csstool.getResourceIds()
    extra_css = ['tree.css', 'finder.css']
    for ec in extra_css:
        if ec not in stylesheet_ids:
            csstool.registerStylesheet(ec, media="screen", rendering='import')
    print >> out, 'Installed css %s' % ', '.join(extra_css)

def installCollapsibleTreeJS(self, out):
    """ Install all the javascript for collapsible tree"""
    jstool = getToolByName(self, 'portal_javascripts')
    script_ids = jstool.getResourceIds()
    extra_js = ['tree.js', 'finder.js']
    for ej in extra_js:
        if ej not in script_ids:
            jstool.registerScript(ej)
    print >> out, 'Installed javascript %s' % ', '.join(extra_js)

def install(self):
    out = StringIO()
    portal=getToolByName(self,'portal_url').getPortalObject()

    print >> out, "Successfully installed %s." % TOOL_NAME

    install_subskin(self,out,GLOBALS)
    
    
    try:
        portal.manage_addProduct["Arboreal"].manage_addTool(TOOL_META)
    except:
        # heuristics for testing if an instance with the same name already exists
        # only this error will be swallowed.
        # Zope raises in an unelegant manner a 'Bad Request' error
        e=sys.exc_info()
        if e[0] != 'Bad Request':
            raise

    # register tool in control panel
    portal_control_panel=getToolByName(self,'portal_controlpanel',None)
    portal_control_panel.registerConfiglet( TOOL_NAME #id of your Product
        , TOOL_NAME # Title of your Product
        , 'string:${portal_url}/portal_arboreal/arboreal_view'
        , 'python:True'   # a condition
        , 'Manage portal' # access permission
        , 'Products'      # section to which the configlet should be added: (Plone,Products,Members)
        , True            # visibility
        , '%sID' % TOOL_META
        , 'arboreal_icon.gif' # icon in control_panel
        , 'Use it to define dynamic vocabularies.'
        , None
        )

    # dont allow tool listed as content in navtree

    mtntl = list(self.portal_properties.navtree_properties.metaTypesNotToList)
    if not TOOL_META in mtntl:
        mtntl.append(TOOL_META)
        self.portal_properties.navtree_properties._p_changed=1
        self.portal_properties.navtree_properties.metaTypesNotToList=mtntl


    installCollapsibleTreeCSS(self, out)
    installCollapsibleTreeJS(self, out)

    return out.getvalue()

def uninstall(self):
    out = StringIO()
    portal=getToolByName(self,'portal_url').getPortalObject()
    portal_conf=getToolByName(self,'portal_controlpanel')
    portal_conf.unregisterConfiglet( TOOL_NAME )
    print >> out, "Successfully uninstalled %s." % TOOL_NAME
    return out.getvalue()
