"""
Denis Rouzaud
denis.rouzaud@gmail.com
* * * * * * * * * * * *
Link It 
QGIS module

"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from ui_connect_layer import Ui_connectLayer

from settings import LinkItSettings
from layer_field_combo import layerCombo,fieldCombo,layerFieldCombo

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

# create the dialog to connect layers
class connectLayer(QDialog, Ui_connectLayer ):
	def __init__(self,iface):
		self.iface = iface
		QDialog.__init__(self)
		self.setupUi(self)
		# load settings
		self.settings = LinkItSettings()
		
		linkLayerCombo = layerCombo( self.layerCombo, lambda: self.settings.value("layer") )
		linkFieldCombo = fieldCombo( self.fieldCombo, lambda: self.settings.value("field"), QMetaType.Int )
		self.layerManager = layerFieldCombo(iface.mapCanvas(), self, linkLayerCombo, [linkFieldCombo])
		
		QObject.connect(self , SIGNAL( "accepted()" ) , self.applySettings)
				
	def showEvent(self, e):			
		self.layerManager.onDialogShow()		
				
	def applySettings(self):
		self.settings.setValue( "field" , self.fieldCombo.currentText() )
		if self.layerManager.getLayer() is False: layerId = ''
		else: layerId = self.layerManager.getLayer().id()
		self.settings.setValue( "layer" , layerId )
