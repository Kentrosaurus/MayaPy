# TrackwayImporterWidget.py
# (C)2013 http://cadence.ThreeAddOne.com
# Scott Ernst

from PySide import QtCore

from pyaid.file.FileUtils import FileUtils

from pyglass.dialogs.PyGlassBasicDialogManager import PyGlassBasicDialogManager
from pyglass.elements.PyGlassElementUtils import PyGlassElementUtils
from pyglass.widgets.PyGlassWidget import PyGlassWidget

from cadence.enum.UserConfigEnum import UserConfigEnum
from cadence.data.TrackCsvImporterRemoteThread import TrackCsvImporterRemoteThread
from cadence.models.tracks.Tracks_Track import Tracks_Track

#___________________________________________________________________________________________________ Viewer
class TrackwayImporterWidget(PyGlassWidget):

#===================================================================================================
#                                                                                       C L A S S

    _OVERWRITE_IMPORT_SUFFIX = '_OVERWRITE_IMPORT'

    RESOURCE_FOLDER_PREFIX = ['tools']

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        super(TrackwayImporterWidget, self).__init__(parent, **kwargs)

        PyGlassElementUtils.registerCheckBox(
            owner=self,
            target=self.overwriteImportChk,
            configSetting=self.__class__.__name__ + self._OVERWRITE_IMPORT_SUFFIX)

        self.loadAllBtn.clicked.connect(self._handleLoadAllTracks)
        self.importBtn.clicked.connect(self._handleImportCsv)
        self._thread = None

#===================================================================================================
#                                                                                 H A N D L E R S

#___________________________________________________________________________________________________ _handleLoadAllTracks
    def _handleLoadAllTracks(self):
        self.setEnabled(False)
        model   = Tracks_Track.MASTER
        session = model.createSession()
        entries = session.query(model).all()
        for entry in entries:
            track = entry.createTrack()
            track.generateNode()
        session.close()
        self.setEnabled(True)

#___________________________________________________________________________________________________ _handleImportCsv
    def _handleImportCsv(self):
        path = PyGlassBasicDialogManager.browseForFileOpen(
            parent=self,
            caption=u'Select CSV File to Import',
            defaultPath=self.mainWindow.appConfig.get(UserConfigEnum.LAST_BROWSE_PATH) )
        if not path:
            return

        # Store directory location as the last active directory
        self.mainWindow.appConfig.set(
            UserConfigEnum.LAST_BROWSE_PATH,
            FileUtils.getDirectoryOf(path) )

        # Disable gui while import in progress
        self.mainWindow.setEnabled(False)
        self.mainWindow.refreshGui()

        self._thread = TrackCsvImporterRemoteThread(
            parent=self,
            path=path,
            force=self.overwriteImportChk.isChecked())
        self._thread.execute(callback=self._handleCsvImportComplete)

#___________________________________________________________________________________________________ _handleCsvImportComplete
    def _handleCsvImportComplete(self, response):
        if response['response']:
            print 'ERROR: CSV Import Failed'
            print '  OUTPUT:', response['output']
            print '  ERROR:', response['error']

        self.mainWindow.setEnabled(True)
