"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module
"""

from PyQt4.QtCore import QUrl, Qt, QObject
from PyQt4.QtGui import QIcon, QAction, QDesktopServices
from qgis.core import QgsProject
from qgis.gui import QgsMapLayerAction, QgsMapLayerActionRegistry
from linkit.core.mysettings import MySettings
from linkit.gui.linkerdock import LinkerDock
from linkit.resources_rc import *



class LinkIt(QObject):
    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface
        self.linkerDock = LinkerDock(iface)
        self.settings = MySettings()
        self.mapLayerActions = {}
        QgsProject.instance().relationManager().changed.connect(self.loadRelations)
        self.loadRelations()

    def initGui(self):
        dockVisible = self.settings.value("dockVisible")
        dockArea = self.settings.value("dockArea")
        if dockArea not in (Qt.LeftDockWidgetArea, Qt.RightDockWidgetArea, Qt.TopDockWidgetArea, Qt.BottomDockWidgetArea):
            dockArea = Qt.LeftDockWidgetArea
        self.iface.addDockWidget(dockArea, self.linkerDock)
        self.linkerDock.setVisible(dockVisible)
        self.linkerDock.visibilityChanged.connect(self.dockVisibilityChanged)
        self.linkerDock.dockLocationChanged.connect(self.saveDockLocation)

        # Show dock
        self.showDockAction = QAction(QIcon(":/plugins/linkit/icons/linkit.png"), "Show link editor", self)
        self.showDockAction.setCheckable(True)
        self.showDockAction.setChecked(dockVisible)
        self.showDockAction.triggered.connect(self.linkerDock.setVisible)
        self.iface.addPluginToMenu("&Link It", self.showDockAction)
        self.iface.addToolBarIcon(self.showDockAction)
        # help
        self.helpAction = QAction(QIcon(":/plugins/linkit/icons/help.png"), "Help", self)
        self.helpAction.triggered.connect(lambda: QDesktopServices().openUrl(QUrl("http://3nids.github.io/linkit")))
        self.iface.addPluginToMenu("&Link It", self.helpAction)
                  
    def unload(self):
        self.linkerDock.visibilityChanged.disconnect(self.dockVisibilityChanged)
        self.linkerDock.deactivateMapTool()
        self.linkerDock.close()

        self.iface.removePluginMenu("&Link It", self.showDockAction)
        self.iface.removeToolBarIcon(self.showDockAction)
        self.iface.removePluginMenu("&Link It", self.helpAction)
        self.iface.removeDockWidget(self.linkerDock)

    def loadRelations(self):
        relations = QgsProject.instance().relationManager().referencedRelations()
        newRelationsIds = [relation.id() for relation in relations]
        # remove actions
        for relationId in self.mapLayerActions.keys():
            if relationId not in newRelationsIds:
                QgsMapLayerActionRegistry.instance().removeMapLayerAction(self.mapLayerActions[relationId])
                del self.mapLayerActions[relationId]
        # add actions
        for relation in relations:
            if relation.id() not in self.mapLayerActions:
                action = QgsMapLayerAction("set related feature for %s" % relation.name(), self, relation.referencingLayer(), QgsMapLayerAction.SingleFeature)
                QgsMapLayerActionRegistry.instance().addMapLayerAction(action)
                action.triggeredForFeature.connect(self.linkIt)
                self.mapLayerActions[relation.id()] = action

    def linkIt(self, layer, feature):
        senderAction = self.sender()
        for relationId, action in self.mapLayerActions.iteritems():
            if action == senderAction:
                self.linkerDock.runForFeature(relationId, layer, feature)
                return

    def dockVisibilityChanged(self, dockVisible):
        self.showDockAction.setChecked(dockVisible)
        self.settings.setValue("dockVisible", dockVisible)

    def saveDockLocation(self, dockWidgetArea):
        self.settings.setValue("dockArea", int(dockWidgetArea))