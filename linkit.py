"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module

"""

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from linker import linker
from settings import LinkItSettings
from connect_layer import connectLayer

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class LinkIt():

	def __init__(self, iface):
		self.iface = iface
		self.settings = LinkItSettings()
	
	def initGui(self):
		self.connectLayerDlg = connectLayer(self.iface)
		# run connection when new layers are loaded
		QObject.connect(self.iface.mapCanvas() , SIGNAL("layersChanged ()") , self.connect ) 
		
		# CONNECTLAYERS
		self.connectLayerAction = QAction("Connect layer", self.iface.mainWindow())
		# connect the action to the run method
		QObject.connect(self.connectLayerAction, SIGNAL("triggered()"), self.connectLayerDlg.exec_)
		QObject.connect(self.connectLayerDlg,    SIGNAL("accepted()"),  self.connect)
		# Add toolbar button and menu item
		self.iface.addToolBarIcon(self.connectLayerAction)
		self.iface.addPluginToMenu("&Link It", self.connectLayerAction)
				
	def unload(self):
		self.iface.removePluginMenu("&Link It",self.connectLayerAction)
		self.iface.removeToolBarIcon(self.connectLayerAction)
		
	def connect(self):
		self.layer = next( ( layer for layer in self.iface.legendInterface().layers() if layer.id() == self.settings.value("layer") ), False )
		if self.layer is not False:
			self.linker = linker(self.iface,self.layer)
			QObject.connect( self.layer , SIGNAL("browserCurrentItem(int)") , self.linker.itemChanged )
			QObject.connect( self.layer , SIGNAL("browserNoItem()")         , self.linker.clear )
			QObject.connect( self.layer , SIGNAL("layerDeleted()")          , self.linker.unload )
