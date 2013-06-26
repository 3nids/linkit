"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module
"""


from PyQt4.QtCore import QUrl, Qt
from PyQt4.QtGui import QIcon, QAction, QDesktopServices
from qgis.core import QgsMapLayerRegistry, QgsFeature, QgsFeatureRequest, QgsProject

from core.link import Link, getLink
from gui.linkmanagerdialog import LinkManagerDialog
from gui.linkerdock import LinkerDock

import resources


class LinkIt():
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        QgsProject.instance().readProject.connect(self.createActions)
        # connect layer
        self.linkManagerAction = QAction(QIcon(":/plugins/linkit/icons/connect.png"), "Links managers", self.iface.mainWindow())
        self.linkManagerAction.triggered.connect(self.linkManagerDialog)
        self.iface.addPluginToMenu("&Link It", self.linkManagerAction)
        # help
        self.helpAction = QAction(QIcon(":/plugins/linkit/icons/help.png"), "Help", self.iface.mainWindow())
        self.helpAction.triggered.connect(lambda: QDesktopServices().openUrl(QUrl("https://github.com/3nids/linkit/wiki")))
        self.iface.addPluginToMenu("&Link It", self.helpAction)
                  
    def unload(self):
        self.iface.removePluginMenu("&Link It", self.linkManagerAction)
        self.iface.removePluginMenu("&Link It", self.helpAction)

    def linkManagerDialog(self):
        LinkManagerDialog().exec_()

    def createActions(self):
        for layer in QgsMapLayerRegistry.instance().mapLayers().values():
            link = getLink(layer)
            if link.check():
                link.createAction()

    def linkit(self, destinationLayerId, destinationField, sourceLayerId, featureId):
        destinationLayer = QgsMapLayerRegistry.instance().mapLayer(destinationLayerId)
        if destinationLayer is None:
            return
        sourceLayer = QgsMapLayerRegistry.instance().mapLayer(sourceLayerId)
        if sourceLayer is None:
            return
        f = QgsFeature()
        if destinationLayer.getFeatures(QgsFeatureRequest().setFilterFid(featureId).setFlags(QgsFeatureRequest.NoGeometry)).nextFeature(f) is False:
            return
        self.linkerDock = LinkerDock(self.iface.mapCanvas(), destinationLayer, destinationField, sourceLayer, f)
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.linkerDock)
        destinationLayer.layerDeleted.connect(lambda: self.iface.removeDockWidget(self.linkerDock))
