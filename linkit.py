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

from core.mysettings import MySettings
from core.link import Link, getLink
from gui.linkmanagerdialog import LinkManagerDialog
from gui.linkerdock import LinkerDock
from gui.mysettingsdialog import MySettingsDialog

import resources


class LinkIt():
    def __init__(self, iface):
        self.iface = iface
        self.linkerDock = LinkerDock(iface)
        if MySettings().value("dockArea") == 1:
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.linkerDock)
        else:
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.linkerDock)
        self.linkerDock.hide()

    def initGui(self):
        self.iface.projectRead.connect(self.createActions)
        self.iface.newProjectCreated.connect(self.createActions)

        # connect layer
        self.linkManagerAction = QAction(QIcon(":/plugins/linkit/icons/connect.png"), "Links manager", self.iface.mainWindow())
        self.linkManagerAction.triggered.connect(self.linkManagerDialog)
        self.iface.addPluginToMenu("&Link It", self.linkManagerAction)
        # settings
        self.settingsAction = QAction(QIcon(":/plugins/linkit/icons/settings.svg"), "Settings",
                                      self.iface.mainWindow())
        self.settingsAction.triggered.connect(self.showSettings)
        self.iface.addPluginToMenu("&Link It", self.settingsAction)
        # help
        self.helpAction = QAction(QIcon(":/plugins/linkit/icons/help.png"), "Help", self.iface.mainWindow())
        self.helpAction.triggered.connect(lambda: QDesktopServices().openUrl(QUrl("http://3nids.github.io/linkit")))
        self.iface.addPluginToMenu("&Link It", self.helpAction)
                  
    def unload(self):
        self.iface.removePluginMenu("&Link It", self.linkManagerAction)
        self.iface.removePluginMenu("&Link It", self.settingsAction)
        self.iface.removePluginMenu("&Link It", self.helpAction)
        self.iface.removeDockWidget(self.linkerDock)

    def linkManagerDialog(self):
        LinkManagerDialog().exec_()

    def createActions(self):
        self.linkerDock.disconnectLayers()
        for layer in QgsMapLayerRegistry.instance().mapLayers().values():
            link = getLink(layer)
            if link.check():
                link.createAction()

    def linkit(self, destinationLayerId, destinationField, sourceLayerId, featureId):
        self.linkerDock.set(destinationLayerId, destinationField, sourceLayerId, featureId)

    def showSettings(self):
        MySettingsDialog().exec_()
