# MayaPyHomeWidget.py
# (C)2013
# Scott Ernst

from PySide import QtCore
from PySide import QtGui

from pyglass.gui.scrollArea.SimpleScrollArea import SimpleScrollArea
from pyglass.widgets.PyGlassWidget import PyGlassWidget
from pyglass.widgets.LineSeparatorWidget import LineSeparatorWidget

#___________________________________________________________________________________________________ MayaPyHomeWidget
class MayaPyHomeWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of MayaPyHomeWidget."""
        super(MayaPyHomeWidget, self).__init__(parent, widgetFile=False, **kwargs)
        self._firstView = True

        mainLayout = self._getLayout(self, QtGui.QHBoxLayout)
        mainLayout.setContentsMargins(6, 6, 6, 6)
        mainLayout.setSpacing(6)

        self._toolScroller = SimpleScrollArea(self)
        mainLayout.addWidget(self._toolScroller)
        self._toolBox = self._toolScroller.containerWidget
        self._getLayout(self._toolBox, QtGui.QVBoxLayout)

        self._statusBox, statusLayout = self._createElementWidget(self, QtGui.QVBoxLayout, True)
        statusLayout.addStretch()

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _activateWidgetDisplayImpl
    def _activateWidgetDisplayImpl(self, **kwargs):
        if self._firstView:
            self._firstView = False

#___________________________________________________________________________________________________ _addTool
    def _addTool(self, definition):
        widget, layout = self._createElementWidget(self._toolBox, QtGui.QVBoxLayout, True)
        layout.setContentsMargins(0, 0, 0, 6)
        layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        widget.id = 'toolItem'
        data = dict()

        layout.addWidget(LineSeparatorWidget(widget))
        layout.addSpacing(6)

        w, l = self._createWidget(widget, QtGui.QHBoxLayout, True)
        l.setAlignment(QtCore.Qt.AlignBottom)

        name = QtGui.QLabel(w)
        name.setText(definition['name'])
        name.setStyleSheet("QLabel { font-size:16px; color:#333; }")
        l.addWidget(name)
        l.addStretch()
        data['label'] = name

        btn = QtGui.QPushButton(w)
        btn.setText('Open')
        btn.clicked.connect(self._handleOpenTool)
        l.addWidget(btn)
        data['btn'] = btn

        desc = QtGui.QLabel(widget)
        desc.setText(definition['description'])
        desc.setStyleSheet("QLabel { font-size:11px; color:#666; }")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        data['desc'] = desc

        data['definition'] = definition
        widget.userData    = data
        return widget

