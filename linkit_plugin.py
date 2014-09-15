"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module
"""


from PyQt4.QtCore import QUrl, Qt, QObject
from PyQt4.QtGui import QIcon, QAction, QDesktopServices

from linkit.core.mysettings import MySettings
from linkit.gui.linkmanagerdialog import LinkManagerDialog
from linkit.gui.linkerdock import LinkerDock
from linkit.gui.mysettingsdialog import MySettingsDialog

import resources


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

    def initGui(self):
        self.iface.projectRead.connect(self.createActions)
        self.iface.newProjectCreated.connect(self.createActions)

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
        self.showDockAction.triggered(self.linkerDock.setVisible)
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
        self.iface.removePluginMenu("&Link It", self.showDockAction)
        self.iface.removePluginMenu("&Link It", self.linkManagerAction)
        self.iface.removePluginMenu("&Link It", self.settingsAction)
        self.iface.removePluginMenu("&Link It", self.helpAction)
        self.iface.removeDockWidget(self.linkerDock)


