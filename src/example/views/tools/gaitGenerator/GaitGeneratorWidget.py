# GaitGeneratorWidget.py
# (C)2012 http://cadence.ThreeAddOne.com
# Scott Ernst

import sys

from PySide.QtCore import *
from PySide.QtGui import *

from pyglass.widgets.PyGlassWidget import PyGlassWidget

from cadence.config.enum.GaitConfigEnum import GaitConfigEnum
from cadence.config.enum.SkeletonConfigEnum import SkeletonConfigEnum
from cadence.generator.gait.GaitGenerator import GaitGenerator
from cadence.mayan.gait.GaitVisualizer import GaitVisualizer
from cadence.util.math3D.Vector3D import Vector3D

#___________________________________________________________________________________________________ Viewer
class GaitGeneratorWidget(PyGlassWidget):

#===================================================================================================
#                                                                                       C L A S S

    RESOURCE_FOLDER_PREFIX = ['tools']

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        super(GaitGeneratorWidget, self).__init__(parent, **kwargs)

        w = self
        w.gadLengthLabel.setText(unicode(w.gadLengthSlider.value()))
        QObject.connect(w.gadLengthSlider, SIGNAL("valueChanged(int)"), w.gadLengthLabel.setNum)

        w.gaitPhaseLabel.setText(unicode(w.gaitPhaseSlider.value()))
        QObject.connect(w.gaitPhaseSlider, SIGNAL("valueChanged(int)"), w.gaitPhaseLabel.setNum)

        w.stepLengthLabel.setText(unicode(w.stepLengthSlider.value()))
        QObject.connect(w.stepLengthSlider, SIGNAL("valueChanged(int)"), w.stepLengthLabel.setNum)

        w.dutyFactorHindLabel.setText(unicode(w.dutyFactorHindSlider.value()))
        QObject.connect(w.dutyFactorHindSlider, SIGNAL("valueChanged(int)"), w.dutyFactorHindLabel.setNum)

        w.dutyFactorForeLabel.setText(unicode(w.dutyFactorForeSlider.value()))
        QObject.connect(w.dutyFactorForeSlider, SIGNAL("valueChanged(int)"), w.dutyFactorForeLabel.setNum)

        w.cyclesLabel.setText(unicode(w.cyclesSlider.value()))
        QObject.connect(w.cyclesSlider, SIGNAL("valueChanged(int)"), w.cyclesLabel.setNum)

        w.runButton.clicked.connect(self._runGaitGeneration)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _runGaitGeneration
    def _runGaitGeneration(self):
        w = self
        gg = GaitGenerator(
            overrides = {
                GaitConfigEnum.CYCLES:w.cyclesSlider.value(),
                GaitConfigEnum.DUTY_FACTOR_HIND:w.dutyFactorHindSlider.value(),
                GaitConfigEnum.DUTY_FACTOR_FORE:w.dutyFactorForeSlider.value(),
                GaitConfigEnum.PHASE:w.gaitPhaseSlider.value(),
                SkeletonConfigEnum.STRIDE_LENGTH:w.stepLengthSlider.value(),
                SkeletonConfigEnum.FORE_OFFSET:Vector3D(None, None, float(w.gadLengthSlider.value()))
            }
        )
        gg.run()

        gv = GaitVisualizer(data=gg.toCadenceData())
        gv.buildScene()

