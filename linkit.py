"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module
"""


from PyQt4.QtCore import QUrl, Qt
from PyQt4.QtGui import QIcon, QAction, QDesktopServices
from qgis.core import QgsMapLayerRegistry

from core.mysettings import MySettings
from gui.connectlayerdialog import ConnectLayerDialog
from gui.linker import Linker


class LinkIt():

    def __init__(self, iface):
        self.iface = iface
        self.settings = MySettings()

    def initGui(self):
        self.iface.mapCanvas().layersChanged.connect(self.connect)
        # connect layer
        self.connectLayerAction = QAction(QIcon(":/plugins/linkit/icons/connect.png"), "Connect layer", self.iface.mainWindow())
        self.connectLayerAction.triggered.connect(self.connectLayerDialog)
        self.iface.addPluginToMenu("&Link It", self.connectLayerAction)
        # help
        self.helpAction = QAction(QIcon(":/plugins/linkit/icons/help.png"), "Help", self.iface.mainWindow())
        self.helpAction.triggered.connect(lambda: QDesktopServices().openUrl(QUrl("https://github.com/3nids/linkit/wiki")))
        self.iface.addPluginToMenu("&Link It", self.helpAction)
                  
    def unload(self):
        self.iface.removePluginMenu("&Link It", self.connectLayerAction)
        self.iface.removePluginMenu("&Link It", self.helpAction)
        self.iface.removeToolBarIcon(self.connectLayerAction)

    def connectLayerDialog(self):
        if ConnectLayerDialog().exec_():
            self.connect()
        
    def connect(self):
        layerid = self.settings.value("layer")
        layer = QgsMapLayerRegistry.instance().mapLayer(layerid)
        if layer is not None:
            self.linker = Linker(self.iface, layer)
            layer.browserCurrentItem.connect(self.linker.itemChanged)
            layer.browserNoItem.connect(self.linker.clear)
            layer.layerDeleted.connect(self.linker.unload)

            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.linker)
