"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDockWidget, QIcon
from qgis.core import QgsFeature, QgsFeatureRequest, QgsPoint, QgsGeometry, QGis
from qgis.gui import QgsRubberBand
from math import pi, sqrt, sin, cos

from ..qgissettingmanager import SettingDialog
from ..core.mysettings import MySettings
from ..ui.ui_linker import Ui_linker
from maptoolgetfeature import MapToolGetFeature


def floatrange(a, b, step):
    while a < b:
        yield a
        a += step
    yield b


def centroid(feature):
    geom = feature.geometry()
    if geom.type() == QGis.Line:
        return geom.interpolate(geom.length()/2).asPoint()
    else:
        return geom.centroid().asPoint()


class LinkerDock(QDockWidget, Ui_linker, SettingDialog):
    def __init__(self, mapCanvas, destinationLayer, destinationField, sourceLayer, feature):
        self.destinationLayer = destinationLayer
        self.destinationProvider = destinationLayer.dataProvider()
        self.destinationField = destinationField
        self.sourceLayer = sourceLayer
        self.feature = feature
        self.mapCanvas = mapCanvas
        self.rubber = QgsRubberBand(mapCanvas)

        QDockWidget.__init__(self)
        self.setupUi(self)
        self.drawButton.setCheckable(True)
        SettingDialog.__init__(self, MySettings(), False, True)
        self.cancelButton.hide()
        
        self.cancelButton.setIcon(QIcon(":/plugins/linkit/icons/cancel.svg"))
        self.deleteButton.setIcon(QIcon(":/plugins/linkit/icons/delete.svg"))
        self.drawButton.setIcon(QIcon(":/plugins/linkit/icons/drawline.svg"))
        self.selectButton.setIcon(QIcon(":/plugins/linkit/icons/maptool.svg"))

        self.featureIdLabel.setText("%u" % feature.id())
        currentValue = feature[destinationField]
        self.linkedItemID.setText("%s" % currentValue)

    def closeEvent(self, e):
        self.rubber.reset()

    def clear(self):
        self.setEnabled(False)
        self.fid = False
        self.linkedItemID.clear()

    @pyqtSlot(name="on_selectButton_clicked")
    def setMapTool(self):
        self.mapTool = MapToolGetFeature(self.mapCanvas, self.sourceLayer)
        self.mapTool.featureIdentified.connect(self.featureIdentified)
        self.mapCanvas.setMapTool(self.mapTool)
        self.selectButton.hide()
        self.cancelButton.show()

    @pyqtSlot(name="on_cancelButton_clicked")
    def unsetMapTool(self, dummy=None):
        self.mapCanvas.unsetMapTool(self.mapTool)
        self.selectButton.show()
        self.cancelButton.hide()

    @pyqtSlot(name="on_deleteButton_clicked")
    def deleteLink(self):
        self.linkedItemID.clear()

    def castFeatureId(self, text):
        try:
            return long(text)
        except ValueError:
            return None

    @pyqtSlot(str, name="on_linkedItemID_textChanged")
    def updateLink(self, new):
        new = self.castFeatureId(new)
        fldIdx = self.destinationProvider.fieldNameIndex(self.destinationField)
        self.destinationProvider.changeAttributeValues({self.feature.id(): {fldIdx: new}})
        self.drawLink(self.drawButton.isChecked())
        self.mapCanvas.refresh()

    def featureIdentified(self, new):
        self.linkedItemID.setText("%s" % new)
        self.unsetMapTool()

    @pyqtSlot(bool, name="on_drawButton_toggled")
    def drawLink(self, checked):
        self.rubber.reset()
        if checked:
            # centroid of destination feature
            p1 = centroid(self.feature)
            # centroid of source feature
            f = QgsFeature()
            srcId = self.castFeatureId(self.linkedItemID.text())
            if srcId is None:
                return
            if self.sourceLayer.getFeatures(QgsFeatureRequest().setFilterFid(srcId)).nextFeature(f) is False:
                return
            p2 = centroid(f)
            # point in middle
            mp = QgsPoint((p1.x()+p2.x())/2, (p1.y()+p2.y())/2)
            # distance between the two points
            d = sqrt(p1.sqrDist(p2))
            # orthogonal direction to segment p1-p2
            az = (p1.azimuth(p2)+90)*pi/180
            # create point distant to segment of offset of segment length, will be center of circular arc
            # offset should be  0 < offset < 1
            offset = 1/6
            cp = QgsPoint(mp.x()+d*offset*sin(az),
                          mp.y()+d*offset*cos(az))
            # radius
            r = d*sqrt(4*offset*offset+1)/2
            # calculate start and end azimuth of circular arc
            az1 = cp.azimuth(p1)
            az2 = cp.azimuth(p2)
            if az2 < az1:
                az2 += 360
            # draw arc
            vx = [cp.x()+r*sin(az*pi/180) for az in floatrange(az1, az2, 5)]
            vy = [cp.y()+r*cos(az*pi/180) for az in floatrange(az1, az2, 5)]
            arc = [QgsPoint(vx[i], vy[i]) for i in range(len(vx))]
            geom = QgsGeometry().fromPolyline(arc)
            self.rubber.setToGeometry(geom, self.destinationLayer)



            
            

