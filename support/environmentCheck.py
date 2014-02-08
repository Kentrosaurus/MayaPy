# environmentCheck.py
# (C)2014
# Scott Ernst

""" A script file for creating a summarized status of the host environment's readiness for using
    MayaPy and dependencies. Currently limited to function only on Mac OSX platform. """

import os
import sys

#___________________________________________________________________________________________________ printResult
def printResult(label, status):
        print label + u'.'*(60 - len(label)) + status

#___________________________________________________________________________________________________ padString
def padString(label, char, width, isCenter = True):
    n = width - len(label)
    if n <= 0:
        return label
    elif isCenter:
        n = round(n/2.0)
    return char*int(n) + label

####################################################################################################
####################################################################################################

print u'\n\n' + 100*u'='
print padString(u'ENVIRONMENT CHECK RESULTS', u' ', 100) + u'\n'
print u'System Information:'
print 100*u'-'
print u'VERSION:', sys.version
print u'PREFIX:', sys.prefix
print u'LOCATION:', sys.exec_prefix
print u'SYSTEM:', sys.platform
print u'SYSTEM PATHS:'
for item in sys.path:
    print u'  * ' + item
print u'OS ENVIRONMENT:'
for name,value in os.environ.iteritems():
    print u'  * ' + name, u': ', value

print u'\nStatus Checks:'
print 100*u'-'

# Check for interpreter location
if not sys.prefix.startswith(u'/Library/Frameworks/Python.framework/Versions/2.7'):
    printResult(u'Interpreter', u'FAILED')
    print u'ERROR: You are not using a valid Python interpreter'
else:
    printResult(u'Interpreter', u'PASSED')

# Check for PyAid
try:
    from pyaid.ArgsUtils import ArgsUtils
    printResult(u'PyAid', u'PASSED')
except Exception, err:
    printResult(u'PyAid', u'FAILED')
    print u'Unable to continue without PyAid'
    raise err

from pyaid.debug.Logger import Logger
from pyaid.file.FileUtils import FileUtils
from pyaid.system.SystemUtils import SystemUtils

logger = Logger('environmentCheck', printOut=True)

# Check for Qt 4.X
foundLocation = None
for p in os.listdir(u'/usr/local/'):
    if p.startswith(u'Qt4.'):
        foundLocation = p
printResult(
    u'Qt (%s)' % (foundLocation if foundLocation else u'4.x'),
    u'PASSED' if foundLocation else u'FAILED' )

# Check for PySide system dynamic libraries
paths = []
for p in os.listdir(u'/usr/lib'):
    if p.endswith(u'.dylib') and p.startswith(u'libpyside-'):
        paths.append(p)

printResult(u'PySide (Dynamic Libraries)', u'PASSED' if paths else u'FAILED')
for p in paths:
    print u'  * ', p
result = SystemUtils.executeCommand('find /usr -name "libpyside-*.dylib"')
print u'  + ' + u'\n  + '.join(result['out'].strip().replace(u'\r', u'').split(u'\n'))

# Check for PySide site package shared libraries
foundLocation = None
for p in sys.path:
    p = FileUtils.createPath(p, u'PySide', isDir=True)
    if not os.path.exists(p):
        continue
    if os.path.exists(FileUtils.createPath(p, u'QtCore.so', isFile=True)):
        foundLocation = p
        break

printResult(u'PySide (Package Libraries)', u'PASSED' if foundLocation else u'FAILED')
if foundLocation:
    print u'  * ', foundLocation

# Check for PySide
try:
    from PySide import QtCore
    printResult(u'PySide', u'PASSED')
except Exception, err:
    printResult(u'PySide', u'FAILED')
    logger.writeError(u'Unable to import PySide', err)

# Check for PyGlass
try:
    from pyglass.app.PyGlassEnvironment import PyGlassEnvironment
    printResult(u'PyGlass', u'PASSED')
except Exception, err:
    printResult(u'PyGlass', u'FAILED')
    logger.writeError(u'Unable to import PyGlass', err)
