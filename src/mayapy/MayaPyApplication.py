# CadenceApplication.py
# (C)2013
# Scott Ernst

from pyglass.app.PyGlassApplication import PyGlassApplication

#___________________________________________________________________________________________________ CadenceApplication
class CadenceApplication(PyGlassApplication):

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: debugRootResourcePath
    @property
    def debugRootResourcePath(self):
        return ['..', '..', 'resources']

#___________________________________________________________________________________________________ GS: splashScreenUrl
    @property
    def splashScreenUrl(self):
        return 'splashscreen.png'

#___________________________________________________________________________________________________ GS: appID
    @property
    def appID(self):
        return 'Cadence'

#___________________________________________________________________________________________________ GS: appGroupID
    @property
    def appGroupID(self):
        return 'cadence'

#___________________________________________________________________________________________________ GS: mainWindowClass
    @property
    def mainWindowClass(self):
        from cadence.CadenceMainWindow import CadenceMainWindow
        return CadenceMainWindow

####################################################################################################
####################################################################################################

if __name__ == '__main__':
    CadenceApplication().run()
