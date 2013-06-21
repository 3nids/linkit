"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module
"""

from PyQt4.QtCore import Qt, pyqtSlot
from PyQt4.QtGui import QDockWidget
from qgis.core import QgsFeatureRequest, QgsFeature

from ..core.mysettings import MySettings
from ..ui.ui_linker import Ui_linker
from maptoolgetfeature import MapToolGetFeature


class Linker(QDockWidget, Ui_linker):
    def __init__(self, iface, layer):
        self.iface = iface
        self.layer = layer
        self.provider = layer.dataProvider()
        self.canvas = self.iface.mapCanvas()
        self.settings = MySettings()
        QDockWidget.__init__(self)
        self.setupUi(self)
        self.cancelButton.hide()
        self.setEnabled(False)

    def unload(self):
        self.iface.removeDockWidget(self)

    def fieldIndex(self):
        return self.provider.fieldNameIndex(self.settings.value('field'))

    def itemChanged(self, fid):
        self.clear()
        self.setEnabled(True)
        self.fid = fid
        f = QgsFeature()
        if self.layer.getFeatures(QgsFeatureRequest().setFilterFid(fid)).nextFeature(f):
            currentValue = f.attribute(self.settings.value('field')).toString()
            self.linkedItemID.setText(currentValue)

    def clear(self):
        self.setEnabled(False)
        self.fid = False
        self.linkedItemID.clear()

    @pyqtSlot(name="on_selectButton_clicked")
    def on_selectButton_clicked(self):
        canvas = self.iface.mapCanvas()
        self.mapTool = MapToolGetFeature(canvas, self.layer)
        self.mapTool.featureIdentified.connect(self.featureIdentified)
        canvas.setMapTool(self.mapTool)
        canvas.mapToolSet.connect(self.toolChanged)
        self.selectButton.hide()
        self.cancelButton.show()

    @pyqtSlot(name="on_deleteButton_clicked")
    def on_deleteButton_clicked(self):
        self.linkedItemID.clear()

    @pyqtSlot(name="on_cancelButton_clicked")
    def on_cancelButton_clicked(self):
        self.canvas.unsetMapTool(self.mapTool)
        self.selectButton.show()
        self.cancelButton.hide()
        self.canvas.mapToolSet.disconnect(self.toolChanged)

    def toolChanged(self, tool):
        self.on_cancelButton_clicked()

    @pyqtSlot(str, name="on_linkedItemID_textChanged")
    def on_linkedItemID_textChanged(self, new):
        new = new.toInt()[0]
        if new == 0:
            new = None
        self.provider.changeAttributeValues({ self.fid : {self.fieldIndex() : new } })
        self.iface.mapCanvas().refresh()

    def featureIdentified(self, new):
        self.linkedItemID.setText("%u" % new)
        self.on_cancelButton_clicked()
