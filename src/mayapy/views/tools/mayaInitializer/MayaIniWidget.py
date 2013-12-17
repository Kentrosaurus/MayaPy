# MayaIniWidget.py
# (C)2013
# Scott Ernst

from pyglass.widgets.PyGlassWidget import PyGlassWidget

from cadence.views.tools.mayaInitializer.MayaIniRemoteThread import MayaIniRemoteThread

#___________________________________________________________________________________________________ MayaIniWidget
class MayaIniWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    RESOURCE_FOLDER_PREFIX = ['tools']

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of MayaIniWidget."""
        super(MayaIniWidget, self).__init__(parent, **kwargs)

        self.runBtn.clicked.connect(self._handleExecute)
        self.removeBtn.clicked.connect(self._handleRemove)
        self.reportTextEdit.setReadOnly(True)

        self._thread = None

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runInitializer
    def _runInitializer(self, install =True, test =False):
        text = self.reportTextEdit
        text.clear()
        self._toggleEnabled(False)

        self._thread = MayaIniRemoteThread(self, test=test, install=install)
        self._thread.execute(self._handleInitializerComplete, self._handleThreadLog)

#___________________________________________________________________________________________________ _toggleEnabled
    def _toggleEnabled(self, value):
        self.mainWindow.toggleInteractivity(value)
        self.controlsBox.setEnabled(value)

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleExecute
    def _handleExecute(self):
        self._runInitializer(install=True, test=self.testChk.isChecked())

#___________________________________________________________________________________________________ _handleRemove
    def _handleRemove(self):
        self._runInitializer(install=False, test=self.testChk.isChecked())

#___________________________________________________________________________________________________ _handleInitializerComplete
    def _handleInitializerComplete(self, response):
        self._toggleEnabled(True)
        self.refreshGui()
        self._thread = None

#___________________________________________________________________________________________________ _handleThreadLog
    def _handleThreadLog(self, value):
        self.reportTextEdit.append(value)
