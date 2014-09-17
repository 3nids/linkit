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
import resources_rc


def linkManagerDialog():
    LinkManagerDialog().exec_()


def showSettings():
    MySettingsDialog().exec_()


class LinkIt(QObject):
    def __init__(self, iface):
        QObject.__init__(self)
        self.iface = iface
        self.linkerDock = LinkerDock(iface)
        self.settings = MySettings()
        self.mapLayerActions = {}
        QgsProject.instance().relationManager().relationsLoaded.connect(self.loadRelations)
        self.loadRelations()

    def initGui(self):
        dockVisible = self.settings.value("dockVisible")
        if MySettings().value("dockArea") == 1:
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.linkerDock)
        else:
            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.linkerDock)
        self.linkerDock.setVisible(dockVisible)

        # Show dock
        self.showDockAction = QAction(QIcon(":/plugins/linkit/icons/linkit.png"), "Show link editor", self)
        self.showDockAction.setCheckable(True)
        self.showDockAction.setChecked(dockVisible)
        self.showDockAction.triggered.connect(self.linkerDock.setVisible)
        self.iface.addPluginToMenu("&Link It", self.showDockAction)
        self.iface.addToolBarIcon(self.showDockAction)
        # connect layer
        self.linkManagerAction = QAction(QIcon(":/plugins/linkit/icons/connect.png"), "Links manager", self)
        self.linkManagerAction.triggered.connect(linkManagerDialog)
        self.iface.addPluginToMenu("&Link It", self.linkManagerAction)
        # settings
        self.settingsAction = QAction(QIcon(":/plugins/linkit/icons/settings.svg"), "Settings", self)
        self.settingsAction.triggered.connect(showSettings)
        self.iface.addPluginToMenu("&Link It", self.settingsAction)
        # help
        self.helpAction = QAction(QIcon(":/plugins/linkit/icons/help.png"), "Help", self)
        self.helpAction.triggered.connect(lambda: QDesktopServices().openUrl(QUrl("http://3nids.github.io/linkit")))
        self.iface.addPluginToMenu("&Link It", self.helpAction)
                  
    def unload(self):
        self.linkerDock.deactivateMapTool()

        self.iface.removePluginMenu("&Link It", self.showDockAction)
        self.iface.removeToolBarIcon(self.showDockAction)
        self.iface.removePluginMenu("&Link It", self.linkManagerAction)
        self.iface.removePluginMenu("&Link It", self.settingsAction)
        self.iface.removePluginMenu("&Link It", self.helpAction)
        self.iface.removeDockWidget(self.linkerDock)

    def loadRelations(self):
        relations = QgsProject.instance().relationManager().referencedRelations()
        relationsIds = [relation.id() for relation in relations]
        # remove actions
        for relationId in self.mapLayerActions:
            if relationId not in relationsIds:
                QgsMapLayerActionRegistry.instance().removeMapLayerActions(self.mapLayerActions[relationId])
                del self.mapLayerActions[relationId]
        # add actions
        for relation in relations:
            if relation.id() not in self.mapLayerActions:
                action = QgsMapLayerAction("set related feature for %s" % relation.name(), relation.referencedLayer(), QgsMapLayerAction.SingleFeature)
                QgsMapLayerActionRegistry.instance().addMapLayerAction(action)
                action.triggeredForFeature.connect(self.linkIt)
                self.mapLayerActions[relation.id()] = action

    def linkIt(self, layer, feature):
        senderAction = self.sender()
        for relationId, action in self.mapLayerActions.iteritems():
            if action == senderAction:
                index = self.linkerDock.relationComboBox.findData(relationId)
                self.linkerDock.currentRelationChanged(index)
                self.linkerDock.setReferencingFeature(feature)
                self.linkerDock.relationReferenceWidget.mapIdentification()
                return





