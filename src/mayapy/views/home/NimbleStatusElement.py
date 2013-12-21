# NimbleStatusElement.py
# (C)2013
# Scott Ernst

import nimble

from PySide import QtCore
from PySide import QtGui

from pyglass.gui.PyGlassGuiUtils import PyGlassGuiUtils
from pyglass.elements.PyGlassElement import PyGlassElement
from pyglass.themes.ColorSchemes import ColorSchemes
from pyglass.themes.ThemeColorBundle import ThemeColorBundle

from mayapy.enum.UserConfigEnum import UserConfigEnum

#___________________________________________________________________________________________________ NimbleStatusElement
class NimbleStatusElement(PyGlassElement):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _ACTIVE_LABEL = u'Nimble Connected'
    _ACTIVE_INFO  = u'An active connection exists to a Maya Nimble server'

    _INACTIVE_LABEL = u'Nimble Disabled'
    _INACTIVE_INFO  = u'Nimble will remain disabled until you initiate a retry'

    _FAILED_LABEL = u'Nimble Disconnected'
    _FAILED_INFO  = u'Unable to connect to a Maya Nimble server instance'

    _LABEL_STYLE  = "QLabel { font-size:16px; color:#C#; }"
    _INFO_STYLE   = "QLabel { font-size:11x; color:#C#; }"

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, enabled =False, **kwargs):
        """Creates a new instance of NimbleStatusElement."""
        super(NimbleStatusElement, self).__init__(parent, **kwargs)
        self._colors      = None
        self._status      = False
        self._timer       = None
        self._activeCheck = False
        self._canceled    = False
        self.disabled     = not enabled

        mainLayout = self._getLayout(self, QtGui.QVBoxLayout)
        self.setContentsMargins(6, 6, 6, 6)

        self._label = QtGui.QLabel(self)
        self._label.setText(u'Nimble Connecting...')
        mainLayout.addWidget(self._label)

        self._info = QtGui.QLabel(self)
        self._info.setText(u'Trying to establish a connection to a Maya Nimble server')
        mainLayout.addWidget(self._info)

        self._buttonBox, buttonLayout = self._createWidget(self, QtGui.QHBoxLayout, True)
        buttonLayout.addStretch()

        btn = QtGui.QPushButton(self._buttonBox)
        btn.setText(u'Retry')
        btn.clicked.connect(self._handleRetryClick)
        buttonLayout.addWidget(btn)

        btn = QtGui.QPushButton(self._buttonBox)
        btn.setText(u'Cancel')
        btn.clicked.connect(self._handleCancelClick)
        buttonLayout.addWidget(btn)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ paintEvent
    def paintEvent(self, *args, **kwargs):
        """Doc..."""
        if self._colors:
            PyGlassGuiUtils.gradientPainter(
                self, self.size(), self._colors.light.qColor, self._colors.dark.qColor)

#___________________________________________________________________________________________________ refresh
    def refresh(self):
        if self._activeCheck or self._canceled:
            return
        self._activeCheck = True

        if self.disabled:
            self._colors = ThemeColorBundle(ColorSchemes.GREY)
            self._status = False
            self._label.setText(self._INACTIVE_LABEL)
            self._info.setText(self._INACTIVE_INFO)
        else:
            try:
                # Run an ls command looking for the time node (to prevent large returns)
                nimble.cmds.ls(exactType='time')
                self._colors = ThemeColorBundle(ColorSchemes.GREEN)
                self._status = True
                self._label.setText(self._ACTIVE_LABEL)
                self._info.setText(self._ACTIVE_INFO)
            except Exception, err:
                print 'FAILED: Nimble connection attempt'
                self._colors = ThemeColorBundle(ColorSchemes.RED)
                self._status = False
                self._label.setText(self._FAILED_LABEL)
                self._info.setText(self._FAILED_INFO)

        self._label.setStyleSheet(self._LABEL_STYLE.replace('#C#', self._colors.strong.web))
        self._info.setStyleSheet(self._INFO_STYLE.replace('#C#', self._colors.weak.web))

        self._buttonBox.setVisible(not self._status)

        self.repaint()

        if not self._status and not self.disabled:
            QtCore.QTimer.singleShot(10000, self._handleTimer)
        self._activeCheck = False

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _handleTimer
    @QtCore.Slot()
    def _handleTimer(self, *args, **kwargs):
        if self._canceled:
            return

        if not self.isOnDisplay:
            QtCore.QTimer.singleShot(20000, self._handleTimer)
        else:
            self.refresh()

#___________________________________________________________________________________________________ _handleRetryClick
    def _handleRetryClick(self):
        self.mainWindow.appConfig.set(UserConfigEnum.NIMBLE_TEST_STATUS, True)

        self.disabled = False
        self.refresh()

#___________________________________________________________________________________________________ _handleCancelClick
    def _handleCancelClick(self):
        if self.disabled:
            return

        self.mainWindow.appConfig.set(UserConfigEnum.NIMBLE_TEST_STATUS, False)

        self.disabled = True
        self.refresh()
