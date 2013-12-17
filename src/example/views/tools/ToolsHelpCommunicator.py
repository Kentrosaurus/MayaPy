# ToolsHelpCommunicator.py
# (C)2013
# Scott Ernst

import os
import markdown

from PySide import QtCore

from pyglass.web.PyGlassCommunicator import PyGlassCommunicator

#___________________________________________________________________________________________________ ToolsHelpCommunicator
class ToolsHelpCommunicator(PyGlassCommunicator):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        """Creates a new instance of ToolsHelpCommunicator."""
        super(ToolsHelpCommunicator, self).__init__(None, **kwargs)
        self._target = None
        self._content = None

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: javaScriptID
    @property
    def javaScriptID(self):
        return 'CADENCE'

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ loadContent
    def loadContent(self, target):
        self._target = target
        helpPath     = target.getResourcePath('help.markdown', isFile=True)

        try:
            if os.path.exists(helpPath):
                f = open(helpPath, 'r+')
                md = f.read().encode('utf-8', 'ignore')
                f.close()
                self._content = markdown.markdown(md)
            else:
                return False
        except Exception, err:
            return False

        self.callUpdate()
        return True

#___________________________________________________________________________________________________ getContent
    @QtCore.Slot(result=unicode)
    def getContent(self):
        return self._content if self._content else u''

