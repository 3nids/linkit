
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QColor
from linkit.qgissettingmanager import *

pluginName = "linkit"


class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, pluginName)
        self.addSetting("drawButton", "bool", "global", True)
        self.addSetting("rubberColor", "Color", "global", QColor(0, 0, 255, 150), {"alpha": True})
        self.addSetting("rubberWidth", "double", "global", 2)
        self.addSetting("dockVisible", "bool", "global", False)
        self.addSetting("dockArea", "integer", "global", int(Qt.LeftDockWidgetArea))
        self.addSetting("drawEnabled", "bool", "global", False)
