"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module
"""

from PyQt4.QtCore import pyqtSlot, Qt
from PyQt4.QtGui import QDockWidget
from qgis.core import QgsProject, QgsFeature, QgsRelation
from qgis.gui import QgsRubberBand, QgsMessageBar, QgsEditorWidgetRegistry, QgsMapToolIdentifyFeature, QgsAttributeEditorContext

from linkit.qgissettingmanager import SettingDialog
from linkit.core.mysettings import MySettings
from linkit.core.arc import arc
from linkit.ui.ui_linker import Ui_linker


def centroid(feature):
    geom = feature.geometry()
    if geom.type() == QGis.Line:
        return geom.interpolate(geom.length()/2).asPoint()
    else:
        return geom.centroid().asPoint()


class LinkerDock(QDockWidget, Ui_linker, SettingDialog):
    def __init__(self, iface):
        # GUI
        QDockWidget.__init__(self)
        self.setupUi(self)
        SettingDialog.__init__(self, MySettings(), False, True)

        self.relationReferenceWidget.setAllowMapIdentification(True)
        self.relationReferenceWidget.setEmbedForm(False)

        # QGIS
        self.iface = iface
        self.settings = MySettings()
        self.linkRubber = QgsRubberBand(self.iface.mapCanvas())
        self.featureRubber = QgsRubberBand(self.iface.mapCanvas())
        self.mapTool = QgsMapToolIdentifyFeature(self.iface.mapCanvas())
        self.mapTool.setButton(self.identifyReferencingFeatureButton)

        # Relation management
        self.relationManager = QgsProject.instance().relationManager()
        self.relationManager.relationsLoaded.connect(self.loadRelations)
        self.relation = QgsRelation()
        self.referencingFeature = QgsFeature()
        self.relationWidgetWrapper = None
        self.editorContext = QgsAttributeEditorContext()
        self.editorContext.setVectorLayerTools(self.iface.vectorLayerTools())

        # Connect signal/slot
        self.relationComboBox.currentIndexChanged.connect(self.currentRelationChanged)
        self.mapTool.featureIdentified.connect(self.setReferencingFeature)

        # load relations at start
        self.loadRelations()

    def runForFeature(self, relationId, layer, feature):
        index = self.relationComboBox.findData(relationId)
        self.relationComboBox.setCurrentIndex(index)
        self.setReferencingFeature(feature)
        self.show()
        if not layer.isEditable():
            self.iface.messageBar().pushMessage("Link It", "Cannot set a new related feature since %s is not editable" % layer.name(), QgsMessageBar.WARNING, 4)
        else:
            self.relationReferenceWidget.mapIdentification()

    @pyqtSlot(name="on_identifyReferencingFeatureButton_clicked")
    def activateMapTool(self):
        self.iface.mapCanvas().setMapTool(self.mapTool)

    def deactivateMapTool(self):
        self.iface.mapCanvas().unsetMapTool(self.mapTool)

    def loadRelations(self):
        self.relation = QgsRelation()
        self.referencingFeature = QgsFeature()
        self.relationComboBox.clear()
        for relation in self.relationManager.referencedRelations():
            if relation.referencingLayer().hasGeometryType():
                self.relationComboBox.addItem(relation.name(), relation.id())

    def currentRelationChanged(self, index):
        # disconnect previous relation
        if self.relation.isValid():
            self.relation.referencingLayer().editingStarted.disconnect(self.relationEditableChanged)
            self.relation.referencingLayer().editingStopped.disconnect(self.relationEditableChanged)
            self.relation.referencingLayer().attributeValueChanged.disconnect(self.layerValueChangedOutside)

        self.referencingFeatureLayout.setEnabled(index >= 0)
        relationId = self.relationComboBox.itemData(index)
        self.relation = self.relationManager.relation(relationId)
        self.mapTool.setLayer(self.relation.referencingLayer())
        self.setReferencingFeature()
        # connect
        if self.relation.isValid():
            self.relation.referencingLayer().editingStarted.connect(self.relationEditableChanged)
            self.relation.referencingLayer().editingStopped.connect(self.relationEditableChanged)
            self.relation.referencingLayer().attributeValueChanged.connect(self.layerValueChangedOutside)

    def setReferencingFeature(self, feature=QgsFeature()):
        self.deactivateMapTool()
        self.referencingFeature = QgsFeature(feature)

        del self.relationWidgetWrapper

        # disable relation reference widget if no referencing feature
        self.referencedFeatureLayout.setEnabled(feature.isValid())

        # set line edit
        if not self.relation.isValid() or not feature.isValid():
            self.referencingFeatureLineEdit.clear()
            self.relationReferenceWidget.setForeignKey(None)
            self.relationWidgetWrapper = None
            return
        self.referencingFeatureLineEdit.setText("%s" % feature.id())

        fieldIdx = self.fieldIndex()
        widgetConfig = self.relation.referencingLayer().editorWidgetV2Config(fieldIdx)
        self.relationWidgetWrapper = QgsEditorWidgetRegistry.instance().create("RelationReference",
                                                                               self.relation.referencingLayer(),
                                                                               fieldIdx,
                                                                               widgetConfig,
                                                                               self.relationReferenceWidget,
                                                                               self,
                                                                               self.editorContext)

        self.relationWidgetWrapper.setEnabled(self.relation.referencingLayer().isEditable())
        self.relationWidgetWrapper.setValue(feature[fieldIdx])
        self.relationWidgetWrapper.valueChanged.connect(self.foreignKeyChanged)
        # override field definition to allow map identification
        self.relationReferenceWidget.setAllowMapIdentification(True)
        self.relationReferenceWidget.setEmbedForm(False)

    def foreignKeyChanged(self, newKey):
        if not self.relation.isValid() or not self.relation.referencingLayer().isEditable() or not self.referencingFeature.isValid():
            return
        if not self.relation.referencingLayer().editBuffer().changeAttributeValue(self.referencingFeature.id(), self.fieldIndex(), newKey):
            self.iface.messageBar().pushMessage("Link It", "Cannot change attribute value.", QgsMessageBar.CRITICAL)

    def relationEditableChanged(self):
        if self.relationWidgetWrapper is not None:
            self.relationWidgetWrapper.setEnabled(self.relation.isValid() and self.relation.referencingLayer().isEditable())

    def layerValueChangedOutside(self, fid, fieldIdx, value):
        if not self.relation.isValid() or not self.referencingFeature.isValid() or self.relationWidgetWrapper is None:
            return
        # not the correct feature
        if fid != self.referencingFeature.id():
            return
        # not the correct field
        if fieldIdx != self.fieldIndex():
            return
        # widget already has this value
        if value == self.relationWidgetWrapper.value():
            return
        self.relationWidgetWrapper.valueChanged.disconnect(self.foreignKeyChanged)
        self.relationWidgetWrapper.setValue(value)
        self.relationWidgetWrapper.valueChanged.connect(self.foreignKeyChanged)

    def fieldIndex(self):
        if not self.relation.isValid():
            return -1
        fieldName = self.relation.fieldPairs().keys()[0]
        fieldIdx = self.relation.referencingLayer().fieldNameIndex(fieldName)
        return fieldIdx

    def closeEvent(self, e):
        print "clsose"
        self.iface.mapCanvas().unsetMapTool(self.mapTool)
        self.linkRubber.reset()
        self.featureRubber.reset()
        if self.relation.isValid():
            self.relation.referencingLayer().editingStarted.disconnect(self.relationEditableChanged)
            self.relation.referencingLayer().editingStopped.disconnect(self.relationEditableChanged)
            self.relation.referencingLayer().attributeValueChanged.disconnect(self.layerValueChangedOutside)


    @pyqtSlot(name="on_drawButton_toggled")
    def drawLink(self):
        self.linkRubber.reset()
        referencedFeature = self.relationReferenceWidget.getFeature()

        if not self.drawButton.isChecked() or not self.feature.isValid() or not referencedFeature.isValid() or not self.relation.isValid():
            return

        p1 = centroid(referencedFeature)
        p2 = centroid(self.referencingFeature)
        geom = arc(p1, p2)

        self.linkRubber.setToGeometry(geom, self.destinationLayer)
        self.linkRubber.setWidth(self.settings.value("rubberWidth"))
        self.linkRubber.setColor(self.settings.value("rubberColor"))
        self.linkRubber.setLineStyle(Qt.DashLine)

        self.mapCanvas.refresh()
