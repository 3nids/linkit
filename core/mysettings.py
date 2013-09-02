from ..qgissettingmanager import *

pluginName = "linkit"


class MySettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, pluginName)
        self.addSetting("drawButton", "bool", "global", True)
        self.addSetting("dockArea", "integer", "global", 0)

