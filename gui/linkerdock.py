"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module
"""

from PyQt4.QtCore import pyqtSlot, Qt, QSettings, QTimer
from PyQt4.QtGui import QDockWidget, QColor
from qgis.core import QgsProject, QgsFeature, QgsRelation, QGis
from qgis.gui import QgsRubberBand, QgsMessageBar, QgsEditorWidgetRegistry, QgsMapToolIdentifyFeature, QgsAttributeEditorContext, QgsHighlight

from linkit.qgissettingmanager import SettingDialog
from linkit.core.mysettings import MySettings
from linkit.core.arc import arc
from linkit.ui.ui_linker import Ui_linker


class LinkerDock(QDockWidget, Ui_linker, SettingDialog):
    def __init__(self, iface):
        # QGIS
        self.iface = iface
        self.settings = MySettings()
        self.linkRubber = QgsRubberBand(self.iface.mapCanvas())
        self.featureHighlight = None
        # Relation management
        self.relationManager = QgsProject.instance().relationManager()
        self.relationManager.changed.connect(self.loadRelations)
        self.relation = QgsRelation()
        self.referencingFeature = QgsFeature()
        self.relationWidgetWrapper = None
        self.editorContext = QgsAttributeEditorContext()
        self.editorContext.setVectorLayerTools(self.iface.vectorLayerTools())

        # GUI
        QDockWidget.__init__(self)
        self.setupUi(self)
        SettingDialog.__init__(self, MySettings(), False, True)
        self.drawButton.setChecked(self.settings.value("drawEnabled"))

        self.relationReferenceWidget.setAllowMapIdentification(True)
        self.relationReferenceWidget.setEmbedForm(False)

        self.mapTool = QgsMapToolIdentifyFeature(self.iface.mapCanvas())
        self.mapTool.setButton(self.identifyReferencingFeatureButton)

        # Connect signal/slot
        self.relationComboBox.currentIndexChanged.connect(self.currentRelationChanged)
        self.mapTool.featureIdentified.connect(self.setReferencingFeature)

        # load relations at start
        self.loadRelations()

    def showEvent(self, QShowEvent):
        self.drawLink()

    def closeEvent(self, e):
        self.iface.mapCanvas().unsetMapTool(self.mapTool)
        self.linkRubber.reset()
        self.deleteHighlight()
        self.deleteWrapper()
        self.disconnectLayer()

    def disconnectLayer(self):
        if self.relation.isValid():
            self.relation.referencingLayer().editingStarted.disconnect(self.relationEditableChanged)
            self.relation.referencingLayer().editingStopped.disconnect(self.relationEditableChanged)
            self.relation.referencingLayer().attributeValueChanged.disconnect(self.layerValueChangedOutside)

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
        self.deleteWrapper()
        self.disconnectLayer()
        self.relation = QgsRelation()
        self.referencingFeature = QgsFeature()
        self.relationComboBox.currentIndexChanged.disconnect(self.currentRelationChanged)
        self.relationComboBox.clear()
        for relation in self.relationManager.referencedRelations():
            if relation.referencingLayer().hasGeometryType():
                self.relationComboBox.addItem(relation.name(), relation.id())
        self.relationComboBox.setCurrentIndex(-1)
        self.relationComboBox.currentIndexChanged.connect(self.currentRelationChanged)
        self.currentRelationChanged(-1)

    def currentRelationChanged(self, index):
        # disconnect previous relation
        if self.relation.isValid():
            try:
                self.relation.referencingLayer().editingStarted.disconnect(self.relationEditableChanged)
                self.relation.referencingLayer().editingStopped.disconnect(self.relationEditableChanged)
                self.relation.referencingLayer().attributeValueChanged.disconnect(self.layerValueChangedOutside)
            except TypeError:
                pass

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
        self.deleteWrapper()

        # disable relation reference widget if no referencing feature
        self.referencedFeatureLayout.setEnabled(feature.isValid())

        # set line edit
        if not self.relation.isValid() or not feature.isValid():
            self.referencingFeatureLineEdit.clear()
            return
        self.referencingFeatureLineEdit.setText("%s" % feature.id())

        fieldIdx = self.referencingFieldIndex()
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

        # update drawn link
        self.highlightReferencingFeature()
        self.drawLink()

    def deleteWrapper(self):
        if self.relationWidgetWrapper is not None:
            self.relationWidgetWrapper.valueChanged.disconnect(self.foreignKeyChanged)
            self.relationWidgetWrapper.setValue(None)
            del self.relationWidgetWrapper
            self.relationWidgetWrapper = None

    def foreignKeyChanged(self, newKey):
        if not self.relation.isValid() or not self.relation.referencingLayer().isEditable() or not self.referencingFeature.isValid():
            self.drawLink()
            return
        if not self.relation.referencingLayer().editBuffer().changeAttributeValue(self.referencingFeature.id(), self.referencingFieldIndex(), newKey):
            self.iface.messageBar().pushMessage("Link It", "Cannot change attribute value.", QgsMessageBar.CRITICAL)
        self.drawLink()

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
        if fieldIdx != self.referencingFieldIndex():
            return
        # widget already has this value
        if value == self.relationWidgetWrapper.value():
            return
        self.relationWidgetWrapper.valueChanged.disconnect(self.foreignKeyChanged)
        self.relationWidgetWrapper.setValue(value)
        self.relationWidgetWrapper.valueChanged.connect(self.foreignKeyChanged)

    def referencingFieldIndex(self):
        if not self.relation.isValid():
            return -1
        fieldName = self.relation.fieldPairs().keys()[0]
        fieldIdx = self.relation.referencingLayer().fieldNameIndex(fieldName)
        return fieldIdx

    @pyqtSlot(bool, name="on_drawButton_toggled")
    def drawLink(self):
        self.settings.setValue("drawEnabled", self.drawButton.isChecked())
        self.linkRubber.reset()
        if not self.drawButton.isChecked() or not self.referencingFeature.isValid() or not self.relation.isValid():
            return

        referencedFeature = self.relationReferenceWidget.referencedFeature()
        if not referencedFeature.isValid():
            return

        p1 = self.centroid(self.relation.referencedLayer(), referencedFeature)
        p2 = self.centroid(self.relation.referencingLayer(), self.referencingFeature)
        geom = arc(p1, p2)

        self.linkRubber.setToGeometry(geom, None)
        self.linkRubber.setWidth(self.settings.value("rubberWidth"))
        self.linkRubber.setColor(self.settings.value("rubberColor"))
        self.linkRubber.setLineStyle(Qt.DashLine)

    def centroid(self, layer, feature):
        geom = feature.geometry()
        if geom.type() == QGis.Line:
            geom = geom.interpolate(geom.length()/2)
        else:
            geom = geom.centroid()
        return self.iface.mapCanvas().mapSettings().layerToMapCoordinates(layer, geom.asPoint())

    @pyqtSlot(name="on_highlightReferencingFeatureButton_clicked")
    def highlightReferencingFeature(self):
        self.deleteHighlight()
        if not self.relation.isValid() or not self.referencingFeature.isValid():
            return
        
        self.featureHighlight = QgsHighlight(self.iface.mapCanvas(), self.referencingFeature.geometry(), self.relation.referencingLayer())
        settings = QSettings()
        color = QColor( settings.value("/Map/highlight/color", QGis.DEFAULT_HIGHLIGHT_COLOR.name()))
        alpha = int(settings.value("/Map/highlight/colorAlpha", QGis.DEFAULT_HIGHLIGHT_COLOR.alpha()))
        bbuffer = float(settings.value("/Map/highlight/buffer", QGis.DEFAULT_HIGHLIGHT_BUFFER_MM))
        minWidth = float(settings.value("/Map/highlight/minWidth", QGis.DEFAULT_HIGHLIGHT_MIN_WIDTH_MM))
        
        self.featureHighlight.setColor(color)
        color.setAlpha(alpha)
        self.featureHighlight.setFillColor(color)
        self.featureHighlight.setBuffer(bbuffer)
        self.featureHighlight.setMinWidth(minWidth)
        self.featureHighlight.show()

        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(self.deleteHighlight)
        timer.start(3000)

    def deleteHighlight(self):
        if self.featureHighlight:
            del self.featureHighlight
        self.featureHighlight = None
