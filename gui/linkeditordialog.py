"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module
"""

from PyQt4.QtGui import QDialog
from ..qgiscombomanager import VectorLayerCombo, FieldCombo
from ..core.link import Link
from ..ui.ui_linkeditor import Ui_LinkEditor


class LinkEditorDialog(QDialog, Ui_LinkEditor):
    def __init__(self, link=None):
        QDialog.__init__(self)
        self.setupUi(self)

        self.destinationLayerCombo = VectorLayerCombo(self.destinationLayer, "", {"hasGeometry": True})
        self.destinationFieldCombo = FieldCombo(self.destinationField, self.destinationLayerCombo)
        self.sourceLayerCombo = VectorLayerCombo(self.sourceLayer, "", {"hasGeometry": True})

        if link is not None:
            self.linkName.setText(link.name)
            self.destinationLayerCombo.setLayer(link.destinationLayer)
            self.destinationFieldCombo.setField(link.destinationField)
            self.sourceLayerCombo.setLayer(link.sourceLayer)
 
    def accept(self):
        name = self.linkName.text()
        destLayer = self.destinationLayerCombo.getLayer().id()
        destField = self.destinationFieldCombo.getFieldName()
        srcLayer = self.sourceLayerCombo.getLayer().id()

        link = Link(name, destLayer, destField, srcLayer)

        if link.check():
            link.save()
            QDialog.accept(self)
