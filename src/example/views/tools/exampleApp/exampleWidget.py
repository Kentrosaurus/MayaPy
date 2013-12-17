# TrackwayManagerWidget.py
# (C)2012-2013
# Scott Ernst and Kent A. Stevens


from nimble import cmds

from pyaid.json.JSON import JSON

from pyglass.widgets.PyGlassWidget import PyGlassWidget

from cadence.enum.TrackPropEnum import TrackPropEnum
from cadence.mayan.trackway.Track import Track

#___________________________________________________________________________________________________ TrackwayManagerWidget
class TrackwayManagerWidget(PyGlassWidget):

#===================================================================================================
#                                                                                                    C L A S S
    RESOURCE_FOLDER_PREFIX = ['tools']

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        super(TrackwayManagerWidget, self).__init__(parent, **kwargs)

        self.refreshBtn.clicked.connect(self.refreshUI)

        # in Edit Track tab:
        self.selectPriorBtn.clicked.connect(self.selectPrecursors)
        self.selectLaterBtn.clicked.connect(self.selectSuccessors)

        self.selectSeriesBtn.clicked.connect(self.selectSeries)
        self.deleteBtn.clicked.connect(self.deleteSelected)

        self.linkBtn.clicked.connect(self.linkSelectedTracks)
        self.unlinkBtn.clicked.connect(self.unlinkSelectedTracks)

        self.renameBtn.clicked.connect(self.renameSelected)
        self.setSelectedBtn.clicked.connect(self.setSelected)

        self.firstBtn.clicked.connect(self.goToFirstTrack)
        self.prevBtn.clicked.connect(self.goToPrevTrack)
        self.nextBtn.clicked.connect(self.goToNextTrack)
        self.lastBtn.clicked.connect(self.goToLastTrack)

        self.addBtn.clicked.connect(self.addTrack)
        self.findBtn.clicked.connect(self.findTrack)

        # in Edit Trackway tab:
        #self.trackwayCB.activated.connect(self.selectFromTrackwayCB)
        self.showTrackwayBtn.clicked.connect(self.showTrackway)
        self.hideTrackwayBtn.clicked.connect(self.hideTrackway)
        self.selectTrackwayBtn.clicked.connect(self.selectTrackway)
        self.showAllTrackwaysBtn.clicked.connect(self.showAllTrackways)
        self.hideAllTrackwaysBtn.clicked.connect(self.hideAllTrackways)
        self.selectAllTrackwaysBtn.clicked.connect(self.selectAllTrackways)
        self.setTrackwayBtn.clicked.connect(self.setSelectedTrackway)
        self.initBtn.clicked.connect(self.initializeTrackway)
        self.repairBtn.clicked.connect(self.repair)

        self.adjustSize()
        self.refreshUI()

#===================================================================================================
#                                                                                                     P U B L I C
#

#___________________________________________________________________________________________________ isTrackNode
    def isTrackNode(self, n):
        return cmds.attributeQuery(TrackPropEnum.SITE.name, node=n, exists=True)

#___________________________________________________________________________________________________ getAllTracks
    def getAllTracks(self):
        nodes = cmds.ls('track*') # all track nodes are presumed to start with 'track'

        if nodes is None:
            return None
        tracks = list()
        for n in nodes:
            if self.isTrackNode(n):
                tracks.append(Track(n))
        return tracks if len(tracks) > 0 else None

#___________________________________________________________________________________________________ getSelected
    def getSelected(self):
        selectedNodes = cmds.ls(selection=True, exactType='transform')
        if len(selectedNodes) == 0:
            return None
        tracks = list()
        for n in selectedNodes:
            if self.isTrackNode(n):
                tracks.append(Track(n))
        return tracks

#___________________________________________________________________________________________________ getFirstTrack
    def getFirstTrack(self):
        selectedTracks = self.getSelected()
        if not selectedTracks:
            return None
        t = selectedTracks[0]
        while t.prevTrack is not None:
            t = t.prevTrack
        return t

#___________________________________________________________________________________________________ getLastTrack
    def getLastTrack(self):
        selectedTracks = self.getSelected()
        if not selectedTracks:
            return None
        t = selectedTracks[-1]
        while t.nextTrack is not None:
            t = t.nextTrack
        return t

#___________________________________________________________________________________________________ getFirstSelectedTrack
    def getFirstSelectedTrack(self):
        selectedTracks = self.getSelected()
        if not selectedTracks:
            return None
        s = selectedTracks[0]
        while s.prevTrack in selectedTracks:
            s = s.prevTrack
        return s

#___________________________________________________________________________________________________ getLastSelectedTrack
    def getLastSelectedTrack(self):
        selectedTracks = self.getSelected()
        if not selectedTracks:
            return None
        s = selectedTracks[-1]
        while s.nextTrack in selectedTracks:
            s = s.nextTrack
        return s

 #__________________________________________________________________________________________________ getTrackSeries
    def getTrackSeries(self):
        series = list()
        t = self.getFirstTrack()
        while t:
            series.append(t)
            t = t.nextTrack
        return series

#___________________________________________________________________________________________________ selectTrack
    def selectTrack(self, track):
       track.setCadenceCamFocus()
       cmds.select(track.node)

# __________________________________________________________________________________________________ goToFirstTrack
    def goToFirstTrack(self):
        t = self.getFirstTrack()
        if t is None:
            return
        self.selectTrack(t)
        self.refreshUI()

#___________________________________________________________________________________________________ gotoPrevTrack
    def goToPrevTrack(self):
        p = None
        t = self.getFirstSelectedTrack()
        if t is None:
            return
        p = t.prevTrack
        self.selectTrack(p if p else t)
        self.refreshUI()

#___________________________________________________________________________________________________ goToNextTrack
    def goToNextTrack(self):
        n = None
        t = self.getLastSelectedTrack()
        if t is None:
            return
        n = t.nextTrack
        self.selectTrack(n if n else t)
        self.refreshUI()

#___________________________________________________________________________________________________ goToLastTrack
    def goToLastTrack(self):
        t = self.getLastTrack()
        if t is None:
            return
        self.selectTrack(t)
        self.refreshUI()

#___________________________________________________________________________________________________ linkSelectedTracks
    def linkSelectedTracks(self):
        selected = self.getSelected()
        if selected is None:
            return
        i = 0
        while i < len(selected) - 1:
            selected[i+1].link(selected[i])
            i += 1
        cmds.select(selected[-1].node)
        self.refreshUI()

#___________________________________________________________________________________________________ unlinkSelectedTracks
    def unlinkSelectedTracks(self):
        selected = self.getSelected()
        if selected is None:
            return

        s1 = self.getFirstSelectedTrack()
        s2 = self.getLastSelectedTrack()
        p = s1.prevTrackNode
        n = s2.nextTrackNode

        if p and n:              # if track(s) to be unlinked are within
            s1.unlink()          # disconnect previous track from first selected track
            n.link(p)            # connect previous to next, bypassing the selected track(s)
            cmds.select(p.node)  # select the track just prior to the removed track(s)
        elif n and not p:        # selection includes the first track
            n.unlink()
            cmds.select(n.node)  # and select the track just after the selection
        elif p and not n:        # selection includes the last track
            s2.unlink()
            cmds.select(p.node)  # and bump selection back to the previous track
        for s in selected[0:-1]:
            s.unlink()
        self.refreshUI()

#___________________________________________________________________________________________________ initializeTrackway
    def initializeTrackway(self):
        """  This creates the initial two tracks for each of the four series of a trackway.
        Select the eight initial tracks and then set series information"""

        trackProperties = self.getTrackPropertiesFromUI()
        # load up a new dictionary for this

        lp1 = Track(Track.createNode())
        lp1.left   = True
        lp1.pes    = True
        lp1.number = 1
        lp1.x      = 200.0
        lp1.z      = 100.0
        lp1.width  = 0.4
        lp1.length = 0.6

        rp1 = Track(Track.createNode())
        rp1.left   = False
        rp1.pes    = True
        rp1.number = 1
        rp1.x      = 100.0
        rp1.z      = 100.0
        rp1.width  = 0.4
        rp1.length = 0.6

        lm1 = Track(Track.createNode())
        lm1.left   = True
        lm1.pes    = False
        lm1.number = 1
        lm1.x      = 200.0
        lm1.z      = 200.0
        lm1.width  = 0.25
        lm1.length = 0.2

        rm1 = Track(Track.createNode())
        rm1.left   = False
        rm1.pes    = False
        rm1.number = 1
        rm1.x      = 100.0
        rm1.z      = 200.0
        rm1.width  = 0.25
        rm1.length = 0.2

        lp2 = Track(Track.createNode())
        lp2.left   = True
        lp2.pes    = True
        lp2.number = 2
        lp2.x      = 200.0
        lp2.z      = 400.0
        lp2.width  = 0.4
        lp2.length = 0.6

        rp2 = Track(Track.createNode())
        rp2.left   = False
        rp2.pes    = True
        rp2.number = 2
        rp2.x      = 100.0
        rp2.z      = 400.0
        rp2.width  = 0.4
        rp2.length = 0.6

        lm2 = Track(Track.createNode())
        lm2.left   = True
        lm2.pes    = False
        lm2.number = 1
        lm2.x      = 200.0
        lm2.z      = 500.0
        lm2.width  = 0.25
        lm2.length = 0.2

        rm2 = Track(Track.createNode())
        rm2.left   = False
        rm2.pes    = False
        rm2.number = 1
        rm2.x      = 100.0
        rm2.z      = 500.0
        rm2.width  = 0.25
        rm2.length = 0.2

        lp2.link(lp1)
        rp2.link(rp1)
        lm2.link(lm1)
        rm2.link(rm1)

        cmds.select([
            lp1.node, rp1.node, lm1.node, rm1.node,
            lp2.node, rp2.node, lm2.node, rm2.node] )
        lp1.setCadenceCamFocus()
        self.setSelected()

#___________________________________________________________________________________________________ addTrack
    def addTrack(self):
        lastTrack = self.getLastTrack()
        if lastTrack is None:
            return
        prevTrackNode = lastTrack.prevTrackNode
        nextTrack = Track(cmds.duplicate(lastTrack.node)[0])
        nextName  = Track.incrementName(lastTrack.name)
        nextTrack.name = nextName
        dx = lastTrack.x - prevTrackNode.x
        dz = lastTrack.z - prevTrackNode.z
        nextTrack.x = lastTrack.x + dx
        nextTrack.z = lastTrack.z + dz
        nextTrack.link(lastTrack)
        nextTrack.setCadenceCamFocus()
        self.refreshUI()
#___________________________________________________________________________________________________ getNamefromUI
    def getNameFromUI(self):
        return self.rightLeftLE.text() + self.manusPesLE.text() + self.numberLE.text()

#___________________________________________________________________________________________________ getTrackwayPropertiesFromUI
    def getTrackwayPropertiesFromUI(self):
        dictionary = dict()

        dictionary[TrackPropEnum.COMM.name]            = self.communityLE.text()
        dictionary[TrackPropEnum.SITE.name]            = self.siteLE.text()
        dictionary[TrackPropEnum.YEAR.name]            = self.yearLE.text()
        dictionary[TrackPropEnum.SECTOR.name]          = self.sectorLE.text()
        dictionary[TrackPropEnum.LEVEL.name]           = self.levelLE.text()
        dictionary[TrackPropEnum.TRACKWAY_TYPE.name]   = self.trackwayTypeLE.text()
        dictionary[TrackPropEnum.TRACKWAY_NUMBER.name] = self.trackwayNumberLE.text()
        return dictionary

#___________________________________________________________________________________________________ floatLE
    def floatLE(self, string, default =0.0):
        return default if string == '' else float(string)

#___________________________________________________________________________________________________ getTrackPropertiesFromUI
    def getTrackPropertiesFromUI(self):
        """ Get UI values (except for WIDTH, LENGTH, ROTATION, X and Z """
        d = self.getTrackwayPropertiesFromUI() # first get the trackway properties
        # then add to the dictionary the specifics of a given track
        d[TrackPropEnum.NAME.name]  = self.getNameFromUI()
        d[TrackPropEnum.INDEX.name] = self.indexLE.text()
        d[TrackPropEnum.ID.name]    = self.idLE.text()
        d[TrackPropEnum.NOTE.name]  = self.noteTE.toPlainText()

        d[TrackPropEnum.WIDTH_UNCERTAINTY.name]    = self.floatLE(self.widthUncertaintyLE.text())
        d[TrackPropEnum.WIDTH_MEASURED.name]       = self.floatLE(self.widthMeasuredLE.text())
        d[TrackPropEnum.LENGTH_UNCERTAINTY.name]   = self.floatLE(self.lengthUncertaintyLE.text())
        d[TrackPropEnum.LENGTH_MEASURED.name]      = self.floatLE(self.lengthMeasuredLE.text())
        d[TrackPropEnum.ROTATION_UNCERTAINTY.name] = self.floatLE(self.rotationUncertaintyLE.text())
        d[TrackPropEnum.DEPTH_MEASURED.name]       = self.floatLE(self.depthMeasuredLE.text())
        d[TrackPropEnum.DEPTH_UNCERTAINTY.name]    = self.floatLE(self.depthUncertaintyLE.text())

        return d

#___________________________________________________________________________________________________ setSelected
    def setSelected(self):
        selectedTracks = self.getSelected()
        if not selectedTracks:
            return

        if len(selectedTracks) == 1:
            selectedTracks[0].setProperties(self.getTrackPropertiesFromUI())
        else:
            dictionary = self.getTrackwayPropertiesFromUI()
            dictionary[TrackPropEnum.NOTE.name] = self.noteTE.toPlainText()
            for t in selectedTracks:
                t.setProperties(dictionary)
        self.refreshUI()

#___________________________________________________________________________________________________ clearUI
    def clearUI(self):
        self.communityLE.setText('')
        self.siteLE.setText('')
        self.yearLE.setText('')
        self.sectorLE.setText('')
        self.levelLE.setText('')
        self.trackwayTypeLE.setText('')
        self.trackwayNumberLE.setText('')
        self.leftLE.setText('')
        self.pesLE.setText('')
        self.numberLE.setText('')

        self.widthLE.setText('')
        self.widthUncertaintyLE.setText('')
        self.widthMeasuredLE.setText('')

        self.lengthLE.setText('')
        self.lengthUncertaintyLE.setText('')
        self.lengthMeasuredLE.setText('')

        self.rotationLE.setText('')
        self.rotationUncertaintyLE.setText('')

        self.depthMeasuredLE.setText('')
        self.depthUncertaintyLE.setText('')

        self.indexLE.setText('')
        self.idLE.setText('')
        self.noteTE.setPlainText('')

        self.xLE.setText('')
        self.zLE.setText('')

        self.prevTrackLbl.setText(u'')
        self.nextTrackLbl.setText(u'')

#___________________________________________________________________________________________________ refreshUI
    def refreshUI(self):
        selectedTracks = self.getSelected()
        self.clearUI()

        if selectedTracks is None:
            return

        t = selectedTracks[0]
        if len(selectedTracks) == 1:
            self.leftLE.setText(u'L'if t.left else u'R')
            self.pesLE.setText(u'P'if t.pes else u'M')
            self.numberLE.setText(unicode(t.number))

            v = t.width
            self.widthLE.setText(u'' if v is None else '%.2f' % v)

            v = t.widthMeasured
            self.widthMeasuredLE.setText(u'' if v is None else '%.2f' % v)

            v = t.widthUncertainty
            self.widthUncertaintyLE.setText(u'' if v is None else '%.1f' % v)

            v = t.length
            self.lengthLE.setText(u'' if v is None else '%.2f' % v)

            v = t.lengthMeasured
            self.lengthMeasuredLE.setText(u'' if v is None else '%.2f' % v)

            v = t.lengthUncertainty
            self.lengthUncertaintyLE.setText(u'' if v is None else '%.1f' % v)

            v = t.rotation
            self.rotationLE.setText(u'' if v is None else '%.2f' % v)

            v = t.rotationUncertainty
            self.rotationUncertaintyLE.setText(u'' if v is None else '%.1f' % v)

            v = t.depthMeasured
            self.depthMeasuredLE.setText(u'' if v is None else '%.2f' % v)

            v = t.depthUncertainty
            self.depthUncertaintyLE.setText(u'' if v is None else '%.1f' % v)

            v = t.index
            self.indexLE.setText(u'' if v is None else v)

            v = t.id
            self.idLE.setText(u'' if v is None else v)

            v = t.note
            self.noteTE.setPlainText(u'' if v is None else v)

            v = t.x
            self.xLE.setText(u'' if v is None else '%.2f' % v)

            v = t.z
            self.zLE.setText(u'' if v is None else '%.2f' % v)

            v = self.getFirstTrack()
            self.firstTrackLbl.setText(unicode('') if v is None else unicode(v.name))

            v = t.prevTrack
            self.prevTrackLbl.setText(u'' if v is None else unicode(v.name))

            v = t.nextTrack
            self.nextTrackLbl.setText(u'' if v is None else unicode(v.name))

            v = self.getLastTrack()
            self.lastTrackLbl.setText(u'' if v is None else unicode(v.name))

        v = t.comm
        self.communityLE.setText(u'' if v is None else v)

        v = t.site
        self.siteLE.setText(u'' if v is None else v)

        v = t.year
        self.yearLE.setText(u'' if v is None else v)

        v = t.sector
        self.sectorLE.setText(u'' if v is None else v)

        v = t.level
        self.levelLE.setText(u'' if v is None else v)

        v = t.trackwayType
        self.trackwayTypeLE.setText(u'' if v is None else v)

        v = t.trackwayNumber
        self.trackwayNumberLE.setText(u'' if v is None else v)

        if v is not None:
            self.addTrackwayToCB(v)
            i = self.trackwayCB.findText(v)
            self.trackwayCB.setCurrentIndex(i)

#___________________________________________________________________________________________________ renameSelected
    def renameSelected(self):
        selectedTracks = self.getSelected()
        if selectedTracks is None:
             return None
        name = self.getNameFromUI()
        for t in selectedTracks:
             t.name = name
             name   = Track.incrementName(name)

#___________________________________________________________________________________________________ selectSuccessors
    def selectSuccessors(self):
        t = self.getLastSelectedTrack()
        if t is None:
            return
        successor = list()
        t = t.nextTrack
        while t:
            successor.append(t.node)
            t = t.nextTrack
        cmds.select(successor)

#___________________________________________________________________________________________________ selectPrecursors
    def selectPrecursors(self):
         t = self.getFirstSelectedTrack()
         if t is None:
             return
         precursors = list()
         t = t.prevTrack
         while t:
            precursors.append(t.node)
            t = t.prevTrack
         cmds.select(precursors)

#___________________________________________________________________________________________________ selectSeries
    def selectSeries(self):
        tracks = self.getTrackSeries()
        if tracks is None:
            return
        print "This track series consists of %s tracks" % len(tracks)
        nodes = list()
        for t in tracks:
            nodes.append(t.node)
        cmds.select(nodes)

#___________________________________________________________________________________________________ deleteSelected
    def deleteSelected(self):
        tracks = self.getSelected()
        if tracks is None:
            return
        self.unlinkSelectedTracks()
        nodes = list()
        for t in tracks:
            nodes.append(t.node)
        cmds.delete(nodes)

#___________________________________________________________________________________________________ selectAllTracks
    def selectAllTracks(self):
        tracks = self.getAllTracks()
        if len(tracks) == 0:
            return
        nodes = list()
        for t in tracks:
            nodes.append(t.node)
        cmds.select(nodes)

#___________________________________________________________________________________________________ exportSelected
    def exportSelected(self):
        tracks = self.getSelected()

        if tracks is None:
            return

        l = list()
        for t in tracks:
            l.append(t.getProperties())

        JSON.toFile('../../sandbox/test.json', l)

        return tracks

#___________________________________________________________________________________________________ addTrackwayToCB
    def addTrackwayToCB(self, trackway):
        tracks = self.getSelected()

        i = self.trackwayCB.findText(trackway)
        if i == -1:
            self.trackwayCB.addItem(trackway)

#___________________________________________________________________________________________________ showTrackway
    def showTrackway(self):
        tracks = self.getSelected()
        if tracks is None:
            return
        t = tracks[0]
        trackway = t.trackwayType + t.trackwayNumber
        layer = trackway + '_Layer'
        if cmds.objExists(layer):
            cmds.setAttr('%s.visibility' % layer, 1)

#___________________________________________________________________________________________________ hideTrackway
    def hideTrackway(self):
        tracks = self.getSelected()
        if tracks is None:
            return
        t = tracks[0]
        trackway = t.trackway
        layer = trackway + '_Layer'
        if cmds.objExists(layer):
            cmds.setAttr('%s.visibility' % layer, 0)

#___________________________________________________________________________________________________ findTrack
    def findTrack(self):
        targetName = self.getNameFromUI()
        targetTrackway = self.trackwayLE.text()
        for node in cmds.ls('track*', exactType='transform'):
            if self.isTrackNode(node):
                name = cmds.getAttr('%s.name' % node)
                trackway = cmds.getAttr('%s.trackway' % node)
                if name == targetName and trackway == targetTrackway:
                    t = Track(node)
                    self.selectTrack(t)
                    return

#___________________________________________________________________________________________________ selectTrackway
    def selectTrackway(self):
        targetType   = self.trackwayTypeLE.text()
        targetNumber = self.trackwayNumberLE.text()
        tracks = self.getAllTracks()
        nodes = list()
        for t in tracks:
            if t.trackwayType == targetType and t.trackwayNumber == targetNumber:
                nodes.append(t.node)
        cmds.select(nodes, add=True)

#___________________________________________________________________________________________________ showAllTrackways
    def showAllTrackways(self):
        print 'showAllTrackways: clicked'

#___________________________________________________________________________________________________ hideAllTrackways
    def hideAllTrackways(self):
        print 'hideAllTrackways: clicked'

#___________________________________________________________________________________________________ selectAllTrackways
    def selectAllTrackways(self):
        print 'selectAllTrackways: clicked'

#___________________________________________________________________________________________________ setSelectedTrackway
    def setSelectedTrackway(self):
        print 'selectTrackway: clicked'

#___________________________________________________________________________________________________ test
    def test(self):
        pass

#___________________________________________________________________________________________________ repair
    def repair(self):
        tracks = self.getSelected()
#        tracks = self.getAllTracks()
        if tracks is None:
            return

        for t in tracks:
            print 'repairing track %s' % t.node
            if t.nodeHasAttribute('name'):
                v = cmds.getAttr(t.node + '.name')
                print 'name = ', v
                if len(v) > 0:
                    t.left = True if v[0] == u'L' else False
                if len(v) > 1:
                    t.pes  = True if v[1] == u'P' else False
                if len(v) > 2:
                    print 'number = ', v[2:]
                    t.number = v[2:]
                cmds.deleteAttr(t.node + '.name')
            if t.nodeHasAttribute('trackway'):
                v = cmds.getAttr(t.node + '.trackway')
                print 'repair:  trackway = ', v
                t.trackwayType = v[0]
                t.trackwayNumber = v[1:]
                cmds.deleteAttr(t.node + '.trackway')
            if t.nodeHasAttribute('next'):
                cmds.deleteAttr(t.node + '.next')
            if t.nodeHasAttribute('prev'):
                cmds.deleteAttr(t.node + '.prev')
        print 'done'
        self.mainWindow.updateStatusBar('done', 4000)
