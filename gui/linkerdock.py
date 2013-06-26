"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module
"""

from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QDockWidget, QIcon

from ..ui.ui_linker import Ui_linker
from maptoolgetfeature import MapToolGetFeature


class LinkerDock(QDockWidget, Ui_linker):
    def __init__(self, mapCanvas, destinationLayer, destinationField, sourceLayer, feature):
        self.destinationProvider = destinationLayer.dataProvider()
        self.destinationField = destinationField
        self.sourceLayer = sourceLayer
        self.featureId = feature.id()
        self.mapCanvas = mapCanvas

        QDockWidget.__init__(self)
        self.setupUi(self)
        self.cancelButton.hide()
        
        self.cancelButton.setIcon(QIcon(":/plugins/linkit/icons/cancel.svg"))
        self.deleteButton.setIcon(QIcon(":/plugins/linkit/icons/delete.svg"))
        self.drawButton.setIcon(QIcon(":/plugins/linkit/icons/drawline.svg"))
        self.selectButton.setIcon(QIcon(":/plugins/linkit/icons/maptool.svg"))

        currentValue = feature[destinationField]
        self.linkedItemID.setText("%s" % currentValue)
        
    def clear(self):
        self.setEnabled(False)
        self.fid = False
        self.linkedItemID.clear()

    @pyqtSlot(name="on_selectButton_clicked")
    def on_selectButton_clicked(self):
        self.mapTool = MapToolGetFeature(self.mapCanvas, self.sourceLayer)
        self.mapTool.featureIdentified.connect(self.featureIdentified)
        self.mapCanvas.setMapTool(self.mapTool)
        self.selectButton.hide()
        self.cancelButton.show()

    @pyqtSlot(name="on_deleteButton_clicked")
    def on_deleteButton_clicked(self):
        self.linkedItemID.clear()

    @pyqtSlot(name="on_cancelButton_clicked")
    def unsetMapTool(self, dummy=None):
        self.mapCanvas.unsetMapTool(self.mapTool)
        self.selectButton.show()
        self.cancelButton.hide()

    def toolChanged(self, tool):
        self.on_cancelButton_clicked()


    @pyqtSlot(str, name="on_linkedItemID_textChanged")
    def on_linkedItemID_textChanged(self, new):
        try:
            new = long(new)
        except ValueError:
            new = None
        fldIdx = self.destinationProvider.fieldNameIndex(self.destinationField)
        self.destinationProvider.changeAttributeValues({self.featureId: {fldIdx: new}})
        self.mapCanvas.refresh()

    def featureIdentified(self, new):
        self.linkedItemID.setText("%s" % new)
        self.unsetMapTool()
