# CadenceEnvironment.py
# (C)2012-2013 http://cadence.threeaddone.com
# Scott Ernst

import os

from pyaid.file.FileUtils import FileUtils

#___________________________________________________________________________________________________ CadenceEnvironment
class CadenceEnvironment(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    BASE_UNIX_TIME = 1373932675

    _ENV_PATH = os.path.dirname(os.path.abspath(__file__))

#___________________________________________________________________________________________________ getConfigPath
    @classmethod
    def getConfigPath(cls, folder =None, filename =None):
        return cls._createAbsolutePath('config', folder, filename)

#___________________________________________________________________________________________________ getConfigPath
    @classmethod
    def getDataPath(cls, folder =None, filename =None):
        return cls._createAbsolutePath('data', folder, filename)

#___________________________________________________________________________________________________ getResourcePath
    @classmethod
    def getResourcePath(cls, folder =None, filename =None):
        return cls._createAbsolutePath('resources', folder, filename)

#___________________________________________________________________________________________________ getResourceScriptPath
    @classmethod
    def getResourceScriptPath(cls, *args, **kwargs):
        return FileUtils.createPath(
            cls._ENV_PATH, '..', '..', 'resources', 'scripts', *args, **kwargs)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createAbsolutePath
    @classmethod
    def _createAbsolutePath(cls, rootFolder, folder, filename):
        p = rootFolder if isinstance(rootFolder, list) else [rootFolder]
        if isinstance(folder, basestring):
            p.append(folder)
        elif isinstance(folder, list):
            p += folder

        if isinstance(filename, basestring):
            p.append(filename)

        out = os.path.join(cls._ENV_PATH, '..', '..', *p)
        if filename or out.split(os.sep)[-1].find('.') > 0:
            return out

        return out + os.sep
