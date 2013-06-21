"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module
"""

from PyQt4.QtCore import QMetaType
from PyQt4.QtGui import QDialog

from ..qgiscombomanager import VectorLayerCombo, FieldCombo
from ..qgissettingmanager import SettingDialog

from ..core.mysettings import MySettings
from ..ui.ui_connect_layer import Ui_connectLayer


class ConnectLayerDialog(QDialog, Ui_connectLayer, SettingDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.settings = MySettings()
        SettingDialog.__init__(self, self.settings)

        self.layerCombo = VectorLayerCombo(self.layer, lambda: self.settings.value("layer"))
        self.fieldCombo = FieldCombo(self.field, self.layerCombo,
                                     lambda: self.settings.value("field"), QMetaType.Int)

