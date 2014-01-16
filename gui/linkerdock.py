"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module
"""

from PyQt4.QtCore import pyqtSlot, Qt
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


def castFeatureId(text):
    try:
        return long(text)
    except ValueError:
        return None


class LinkerDock(QDockWidget, Ui_linker, SettingDialog):
    def __init__(self, mapCanvas):
        self.destinationLayer = None
        self.destinationProvider = None
        self.destinationField = None
        self.sourceLayer = None
        self.feature = None
        self.mapCanvas = mapCanvas
        self.settings = MySettings()
        self.linkRubber = QgsRubberBand(mapCanvas)
        self.featureRubber = QgsRubberBand(mapCanvas)
        self.mapTool = None

        QDockWidget.__init__(self)
        self.setupUi(self)
        self.enableUI()
        SettingDialog.__init__(self, MySettings(), False, True)

    def set(self, destinationLayer, destinationField, sourceLayer, feature):
        self.disconnectLayers()

        self.destinationLayer = destinationLayer
        self.destinationField = destinationField
        self.sourceLayer = sourceLayer
        self.feature = feature

        self.enableUI()

        self.linkRubber.reset()
        self.featureRubber.reset()
        if self.mapTool is not None:
            self.mapCanvas.unsetMapTool(self.mapTool)
        
        self.cancelButton.setIcon(QIcon(":/plugins/linkit/icons/cancel.svg"))
        self.deleteButton.setIcon(QIcon(":/plugins/linkit/icons/delete.svg"))
        self.drawButton.setIcon(QIcon(":/plugins/linkit/icons/drawline.svg"))
        self.selectButton.setIcon(QIcon(":/plugins/linkit/icons/maptool.svg"))

        self.featureIdLabel.setText("%u" % feature.id())
        currentValue = feature[destinationField]
        self.linkedItemID.setText("%s" % currentValue)
        self.drawLink()

        self.sourceLayer.layerDeleted.connect(self.close)
        self.destinationLayer.layerDeleted.connect(self.close)

        self.destinationLayer.editingStarted.connect(self.enableUI)
        self.destinationLayer.editingStopped.connect(self.enableUI)
        self.destinationLayer.featureDeleted.connect(self.featureDeleted)

        self.show()

    def disconnectLayers(self):
        try:
            self.destinationLayer.layerDeleted.disconnect(self.close)
            self.destinationLayer.editingStarted.disconnect(self.enableUI)
            self.destinationLayer.editingStopped.disconnect(self.enableUI)
        except:
            pass
        try:
            self.sourceLayer.layerDeleted.disconnect(self.enableUI)
        except:
            pass

    def enableUI(self):
        self.mapCanvas.unsetMapTool(self.mapTool)
        enable = False
        if self.destinationLayer is not None and self.sourceLayer is not None:
            if self.destinationLayer.isEditable():
                enable = True
        self.editButtonWidget.setEnabled(enable)
        self.selectButton.show()
        self.cancelButton.hide()

    def featureDeleted(self, fid):
        if self.feature is None:
            return
        if self.feature.id() == fid:
            self.close()

    def closeEvent(self, e):
        if self.mapTool is not None:
            self.mapCanvas.unsetMapTool(self.mapTool)
        self.linkRubber.reset()
        self.featureRubber.reset()
        self.disconnectLayers()

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
        self.updateLink("")

    def updateLink(self, new):
        new = castFeatureId(new)
        fldIdx = self.destinationLayer.fieldNameIndex(self.destinationField)
        if self.destinationLayer.isEditable():
            self.destinationLayer.editBuffer().changeAttributeValue(self.feature.id(), fldIdx, new)
        else:
            self.iface.messageBar().pushMessage("Link It", "Destination layer must be editable.",
                                                QgsMessageBar.WARNING, 3)
        self.drawLink()

    def featureIdentified(self, new):
        self.linkedItemID.setText("%s" % new)
        self.updateLink(new)
        self.unsetMapTool()

    @pyqtSlot(bool, name="on_drawButton_toggled")
    def drawLink(self, dummy=None):
        self.linkRubber.reset()
        if self.destinationLayer is None or self.sourceLayer is None or self.feature is None:
            return
        if self.drawButton.isChecked():
            # centroid of destination feature
            p1 = centroid(self.feature)
            # centroid of source feature
            f = QgsFeature()
            srcId = castFeatureId(self.linkedItemID.text())
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
            offset = 1/12
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
            self.linkRubber.setToGeometry(geom, self.destinationLayer)
            self.linkRubber.setWidth(self.settings.value("rubberWidth"))
            self.linkRubber.setColor(self.settings.value("rubberColor"))
            self.linkRubber.setLineStyle(Qt.DashLine)

            self.mapCanvas.refresh()



            
            

