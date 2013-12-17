# mayaPyWidget.py
# (C)2012-2013
# Scott Ernst and Kent A. Stevens


from nimble import cmds

from pyaid.json.JSON import JSON

from pyglass.widgets.PyGlassWidget import PyGlassWidget


#___________________________________________________________________________________________________ mayaPyWidget
class mayaPyWidget(PyGlassWidget):

#===================================================================================================
#                                                                                                    C L A S S
    RESOURCE_FOLDER_PREFIX = ['tools']

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        super(mayaPyWidget, self).__init__(parent, **kwargs)

        self.refreshBtn.clicked.connect(self.refreshUI)


#===================================================================================================
#                                                                                                     P U B L I C
#
#___________________________________________________________________________________________________ test
    def test(self):
        pass
