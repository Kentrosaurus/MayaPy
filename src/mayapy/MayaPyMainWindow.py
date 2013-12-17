# CadenceMainWindow.py
# (C)2013
# Scott Ernst

from PySide import QtCore
from PySide import QtGui

from pyaid.OsUtils import OsUtils

from pyglass.windows.PyGlassWindow import PyGlassWindow

# AS NEEDED: from cadence.models import tracks
from cadence.views.home.CadenceHomeWidget import CadenceHomeWidget
from cadence.views.tools.CadenceToolViewerWidget import CadenceToolViewerWidget

#___________________________________________________________________________________________________ CadenceMainWindow
class CadenceMainWindow(PyGlassWindow):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, **kwargs):
        PyGlassWindow.__init__(
            self,
            widgets={
                'home':CadenceHomeWidget,
                'toolViewer':CadenceToolViewerWidget },
            title='Cadence Toolset',
            keyboardCallback=self._handleKeyboardCallback,
            **kwargs )
        self.setMinimumSize(1024,480)
        self.setContentsMargins(0, 0, 0, 0)

        widget = self._createCentralWidget()
        layout = QtGui.QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        widget.setLayout(layout)

        self.setActiveWidget('home')

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ toggleInteractivity
    def toggleInteractivity(self, value):
        if self._currentWidget.widgetID == 'home':
            self.setEnabled(value)
        else:
            if value and not self.isEnabled():
                self.setEnabled(value)
            self._currentWidget.toggleInteractivity(value)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _initializeImpl
    def _initializeImpl(self, *args, **kwargs):
        # Initialize databases
        from cadence.models import tracks
        super(CadenceMainWindow, self)._initializeImpl()

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleKeyboardCallback
    def _handleKeyboardCallback(self, event):
        mod  = event.modifiers()
        mods = QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier
        if mod != mods:
            if OsUtils.isMac():
                mods = QtCore.Qt.ShiftModifier | QtCore.Qt.MetaModifier
                if mod != mods:
                    return False
            else:
                return False

        op = self.windowOpacity()

        if event.key() in [QtCore.Qt.Key_Plus, QtCore.Qt.Key_Equal]:
            op = min(1.0, op + 0.2)
        elif event.key() in [QtCore.Qt.Key_Minus, QtCore.Qt.Key_Underscore]:
            op = max(0.2, op - 0.2)
        else:
            return False

        self.setWindowOpacity(op)
        return True

