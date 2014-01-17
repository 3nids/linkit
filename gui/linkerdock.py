"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module
"""

from PyQt4.QtCore import pyqtSlot, Qt
from PyQt4.QtGui import QDockWidget, QIcon
from qgis.core import QgsFeature, QgsFeatureRequest, QgsPoint, QgsGeometry, QGis, QgsMapLayerRegistry
from qgis.gui import QgsRubberBand, QgsMessageBar
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
    def __init__(self, iface):
        self.destinationLayer = None
        self.destinationProvider = None
        self.destinationField = None
        self.sourceLayer = None
        self.featureId = None
        self.iface = iface
        self.mapCanvas = iface.mapCanvas()
        self.settings = MySettings()
        self.linkRubber = QgsRubberBand(self.mapCanvas)
        self.featureRubber = QgsRubberBand(self.mapCanvas)
        self.mapTool = None

        QDockWidget.__init__(self)
        self.setupUi(self)
        SettingDialog.__init__(self, MySettings(), False, True)

    def set(self, destinationLayerId, destinationField, sourceLayerId, featureId):
        self.disconnectLayers()

        self.destinationLayer = QgsMapLayerRegistry.instance().mapLayer(destinationLayerId)
        self.destinationField = destinationField
        self.sourceLayer = QgsMapLayerRegistry.instance().mapLayer(sourceLayerId)

        self.featureIdLabel.setText("%u" % featureId)
        self.featureId = featureId

        self.enableUI()

        self.featureRubber.reset()

        if self.mapTool is not None:
            self.mapCanvas.unsetMapTool(self.mapTool)
        
        self.cancelButton.setIcon(QIcon(":/plugins/linkit/icons/cancel.svg"))
        self.deleteButton.setIcon(QIcon(":/plugins/linkit/icons/delete.svg"))
        self.drawButton.setIcon(QIcon(":/plugins/linkit/icons/drawline.svg"))
        self.selectButton.setIcon(QIcon(":/plugins/linkit/icons/maptool.svg"))

        try:
            self.sourceLayer.layerDeleted.connect(self.close)
        except:
            pass
        try:
            self.destinationLayer.layerDeleted.connect(self.close)
            self.destinationLayer.editingStarted.connect(self.enableUI)
            self.destinationLayer.editingStopped.connect(self.enableUI)
            self.destinationLayer.featureDeleted.connect(self.featureDeleted)
        except:
            pass

        self.show()

    def disconnectLayers(self):
        pass
        # try:
        #     self.destinationLayer.layerDeleted.disconnect(self.close)
        #     self.destinationLayer.editingStarted.disconnect(self.enableUI)
        #     self.destinationLayer.editingStopped.disconnect(self.enableUI)
        # except:
        #     pass
        # try:
        #     self.sourceLayer.layerDeleted.disconnect(self.enableUI)
        # except:
        #     pass

    def enableUI(self):
        self.mapCanvas.unsetMapTool(self.mapTool)

        enable = False

        feature = self.getFeature()
        ok = feature[0]

        if not ok:
            self.iface.messageBar().pushMessage("Link It", feature[1], QgsMessageBar.WARNING, 4)
        else:
            # update current value
            currentValue = feature[1][self.destinationField]
            self.linkedItemID.setText("%s" % currentValue)
            self.drawLink()

        # destination layer is editable
        if ok and self.destinationLayer.isEditable():
            enable = True

        # enable UI
        self.editButtonWidget.setEnabled(enable)
        self.selectButton.show()
        self.cancelButton.hide()

    def getFeature(self):
        # check layers
        if self.destinationLayer is None:
            return False, "Destination layer does not exist."

        if self.sourceLayer is None:
            return False, "Source layer does not exist."

        # check feature exist and fetch feature at once
        feature = QgsFeature()
        if self.destinationLayer.getFeatures(QgsFeatureRequest().setFilterFid(self.featureId)).nextFeature(feature) is False:
            return False, "Could not fetch feature at ID %u." % self.featureId

        # check destination field exist
        if self.destinationLayer.fieldNameIndex(self.destinationField) == -1:
            return False, "Destination field (%s) does not exist." % self.featureId

        return True, feature

    def featureDeleted(self, fid):
        if self.feature is None:
            return
        if self.featureId == fid:
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
            if not self.destinationLayer.editBuffer().changeAttributeValue(self.featureId, fldIdx, new):
                self.iface.messageBar().pushMessage("Link It", "Could not update link value.",
                                                    QgsMessageBar.WARNING, 4)
        else:
            self.iface.messageBar().pushMessage("Link It", "Destination layer must be editable.",
                                                QgsMessageBar.WARNING, 4)
        self.drawLink()

    def featureIdentified(self, new):
        self.linkedItemID.setText("%s" % new)
        self.updateLink(new)
        self.unsetMapTool()

    @pyqtSlot(bool, name="on_drawButton_toggled")
    def drawLink(self, dummy=None):
        self.linkRubber.reset()
        ok, dstFeature = self.getFeature()

        if not ok or not self.drawButton.isChecked():
            return

        # centroid of destination feature
        p1 = centroid(dstFeature)
        # centroid of source feature
        srcFeature = QgsFeature()
        srcId = dstFeature[self.destinationField]
        if srcId is None:
            return
        if self.sourceLayer.getFeatures(QgsFeatureRequest().setFilterFid(srcId)).nextFeature(srcFeature) is False:
            return
        p2 = centroid(srcFeature)
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



            
            

