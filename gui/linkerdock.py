"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module
"""

from PyQt4.QtCore import pyqtSlot, Qt
from PyQt4.QtGui import QDockWidget, QIcon
from qgis.core import QgsProject, QgsFeature, QgsFeatureRequest, QgsPoint, QgsGeometry, QGis, QgsMapLayerRegistry
from qgis.gui import QgsRubberBand, QgsMessageBar, QgsRelationReferenceWidgetWrapper
from math import pi, sqrt, sin, cos

from linkit.qgissettingmanager import SettingDialog
from linkit.core.mysettings import MySettings
from linkit.ui.ui_linker import Ui_linker


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
        self.iface = iface
        self.settings = MySettings()
        self.linkRubber = QgsRubberBand(self.mapCanvas)
        self.featureRubber = QgsRubberBand(self.mapCanvas)
        self.mapTool = None

        self.relationManager = QgsProject.instance().relationManager()
        self.relationManager.relationsLoaded.connect(self.loadRelations)
        self.relation = None

        self.relationWidgetWrapper = None

        QDockWidget.__init__(self)
        self.setupUi(self)
        SettingDialog.__init__(self, MySettings(), False, True)

        self.relationComboBox.currentIndexChanged.connect(self.currentRelationChanged)

    def loadRelations(self):
        self.relation = None
        self.relationComboBox.clear()
        for relation in self.relationManager.referencedRelations():
            if relation.referencingLayer.hasGeometryType():
                self.relations.append(relation)
                self.relationComboBox.addItem(relation.name(), relation.id())

    def currentRelationChanged(self, index):
        self.referencingFeatureLayout.setEnabled(index >= 0)
        relationId = self.relationComboBox.itemData(index)
        self.relation = self.relationManager.relation(relationId)
        self.setReferencingFeature(QgsFeature())

    def setReferencingFeature(self, feature):
        # delete old wrapper
        del self.relationWidgetWrapper

        # get current relation
        idx = self.relationComboBox.currentIndex()
        if idx == -1:
            return
        relation = self.relations[idx]

        # disable relation reference widget if no referencing feature
        self.referencedFeatureLayout.setEnabled(feature.isValid())

        # set line edit
        if not feature.isValid():
            self.referencingFeatureLineEdit.clear()
            return
        self.referencingFeatureLineEdit.setText(feature.id())

        fieldIdx = relation.fieldPairs()[0].first
        self.relationWidgetWrapper = QgsRelationReferenceWidgetWrapper(relation.referencingLayer, fieldIdx, self.iface.mapCanvas(), self.iface.messageBar())
        self.relationWidgetWrapper.initWidget(self.relationReferenceWidget)
        self.relationWidgetWrapper.setEnable(relation.referencingLayer.editable())
        self.relationWidgetWrapper.setValue(fieldIdx)


"""
    def disconnectLayers(self):
        try:
            self.destinationLayer.layerDeleted.disconnect(self.close)
            self.destinationLayer.editingStarted.disconnect(self.enableUI)
            self.destinationLayer.editingStopped.disconnect(self.enableUI)
            self.destinationLayer = None
        except:
            pass
        try:
            self.sourceLayer.layerDeleted.disconnect(self.enableUI)
            self.sourceLayer = None
        except:
            pass



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
        if not srcId:
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
"""