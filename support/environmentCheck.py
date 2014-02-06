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

####################################################################################################
####################################################################################################

print u'System Information:'
print 100*u'-'
print u'VERSION:', sys.version
print u'LOCATION:', sys.exec_prefix
print u'SYSTEM:', sys.platform
print u'SYSTEM PATHS:'
for item in sys.path:
    print u'\t' + item
print u'OS ENVIRONMENT:'
for name,value in os.environ.iteritems():
    print u'\t' + name, u'->', value

print u'\nStatus Checks:'
print 100*u'-'

# Check for PyAid
try:
    from pyaid.ArgsUtils import ArgsUtils
    printResult(u'PyAid', u'PASSED')
except Exception, err:
    printResult(u'PyAid', u'FAILED')
    print u'Unable to continue without PyAid'
    sys.exit(1)

from pyaid.file.FileUtils import FileUtils
from pyaid.system.SystemUtils import SystemUtils

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
    print u'\t', p
result = SystemUtils.executeCommand('find /usr -name "libpyside-*.dylib"')
print result['out']

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
    print u'\t', foundLocation

# Check for PySide
try:
    from PySide import QtCore
    printResult(u'PySide', u'PASSED')
except Exception, err:
    printResult(u'PySide', u'FAILED')

# Check for PyGlass
try:
    from pyglass.app.PyGlassEnvironment import PyGlassEnvironment
    printResult(u'PyGlass', u'PASSED')
except Exception, err:
    printResult(u'PyGlass', u'FAILED')
