# MayaPyHomeWidget.py
# (C)2013
# Scott Ernst

from pyglass.widgets.PyGlassWidget import PyGlassWidget

#___________________________________________________________________________________________________ MayaPyHomeWidget
class MayaPyHomeWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of MayaPyHomeWidget."""
        super(MayaPyHomeWidget, self).__init__(parent, **kwargs)

        self.assignment1Btn.clicked.connect(self._handleAssignment1)
        self.assignment2Btn.clicked.connect(self._handleAssignment2)

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleAssignment1
    def _handleAssignment1(self):
        self.mainWindow.setActiveWidget('assignment1')

#___________________________________________________________________________________________________ _handleAssignment2
    def _handleAssignment2(self):
        self.mainWindow.setActiveWidget('assignment2')
