


"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It
QGIS module
"""

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog, QTableWidgetItem, QIcon
from qgis.core import QgsMapLayerRegistry, QgsMapLayer

from ..core.link import Link, getLink

from linkeditordialog import LinkEditorDialog

from ..ui.ui_linkmanager import Ui_LinkManager


class LinkManagerDialog(QDialog, Ui_LinkManager):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        icon = QIcon(":/plugins/linkit/icons/plus.png")
        self.addButton.setIcon(icon)
        self.removeButton.setIcon(QIcon(":/plugins/linkit/icons/minus.png"))
        self.editButton.setIcon(QIcon(":/plugins/linkit/icons/edit.png"))

        self.addButton.clicked.connect(self.newLink)
        self.removeButton.clicked.connect(self.removeLink)
        self.editButton.clicked.connect(self.editLink)
        self.tableWidget.itemSelectionChanged.connect(self.selectionChanged)
        self.displayRows()
        self.selectionChanged()

    def selectionChanged(self):
        enable = len(self.tableWidget.selectedItems()) > 0
        self.removeButton.setEnabled(enable)
        self.editButton.setEnabled(enable)

    def removeLink(self):
        self.getSelectedLink().delete()
        self.displayRows()

    def editLink(self):
        if LinkEditorDialog(self.getSelectedLink()).exec_():
            self.displayRows()

    def getSelectedLink(self):
        items = self.tableWidget.selectedItems()
        itemData = items[0].data(Qt.UserRole)
        return Link(itemData[0], itemData[1], itemData[2], itemData[3])

    def newLink(self):
        if LinkEditorDialog().exec_():
            self.displayRows()

    def displayRows(self):
        self.tableWidget.clearContents()
        for r in range(self.tableWidget.rowCount() - 1, -1, -1):
            self.tableWidget.removeRow(r)
        for layer in QgsMapLayerRegistry.instance().mapLayers().values():
            if layer.type() == QgsMapLayer.VectorLayer:
                link = getLink(layer)
                if not link.check():
                    continue

                r = self.tableWidget.rowCount()
                self.tableWidget.insertRow(r)

                item = QTableWidgetItem(link.name)
                item.setData(Qt.UserRole, (link.name,
                                           link.destinationLayer.id(),
                                           link.destinationField,
                                           link.sourceLayer.id()))
                self.tableWidget.setItem(r, 0, item)
                item = QTableWidgetItem(link.destinationLayer.name())
                self.tableWidget.setItem(r, 1, item)
                item = QTableWidgetItem(link.destinationField)
                self.tableWidget.setItem(r, 2, item)
                item = QTableWidgetItem(link.sourceLayer.name())
                self.tableWidget.setItem(r, 3, item)

        self.tableWidget.resizeColumnsToContents()











