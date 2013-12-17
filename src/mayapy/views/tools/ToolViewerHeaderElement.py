# ToolViewerHeaderElement.py
# (C)2013
# Scott Ernst

from PySide import QtGui

from pyglass.gui.PyGlassGuiUtils import PyGlassGuiUtils
from pyglass.elements.PyGlassElement import PyGlassElement

#___________________________________________________________________________________________________ ToolViewerHeaderElement
class ToolViewerHeaderElement(PyGlassElement):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of ToolViewerHeaderElement."""
        super(ToolViewerHeaderElement, self).__init__(parent, **kwargs)

        layout = self._getLayout(self, QtGui.QHBoxLayout)
        layout.setContentsMargins(6, 6, 6, 6)

        label = QtGui.QLabel(self)
        label.setText(u' ')
        label.setStyleSheet("QLabel { font-size:18px; color:#CCC; }")
        self._headerLabel = label
        layout.addWidget(label)
        layout.addStretch()

        btn = QtGui.QPushButton(self)
        btn.setText('Close')
        btn.clicked.connect(self._handleCloseTool)
        layout.addWidget(btn)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: propertyName
    @property
    def propertyName(self):
        return None
    @propertyName.setter
    def propertyName(self, value):
        pass

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ setLabel
    def setLabel(self, value):
        """Doc..."""
        self._headerLabel.setText(value)

#___________________________________________________________________________________________________ paintEvent
    def paintEvent(self, *args, **kwargs):
        PyGlassGuiUtils.fillPainter(self, self.size(), QtGui.QColor.fromRgb(50, 50, 50))

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleCloseTool
    def _handleCloseTool(self):
        self.mainWindow.setActiveWidget('home')
