"""
Link It
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
Feb. 2013
"""

from PyQt4.QtCore import pyqtSignal
from qgis.gui import QgsMapToolIdentify


class MapToolGetFeature(QgsMapToolIdentify):
    featureIdentified = pyqtSignal(long)

    def __init__(self, canvas, layer):
        self.layer = layer
        self.canvas = canvas
        QgsMapToolIdentify.__init__(self, canvas)

    def canvasReleaseEvent(self, mouseEvent):
        results = self.identify(mouseEvent.x(), mouseEvent.y(), [self.layer], self.TopDownStopAtFirst)
        if len(results) > 0:
            self.featureIdentified.emit(results[0].mFeature.id())
                    

