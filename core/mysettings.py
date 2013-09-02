from PyQt4.QtGui import QColor

from ..qgissettingmanager import *

pluginName = "linkit"


class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, pluginName)
        self.addSetting("drawButton", "bool", "global", True)
        self.addSetting("dockArea", "integer", "global", 0)
        self.addSetting("rubberColor", "Color", "global", QColor(0, 0, 255, 150), {"alpha": True})
        self.addSetting("rubberWidth", "double", "global", 2)
