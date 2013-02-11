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
from qgis.gui import *

from settings import LinkItSettings
from maptoolgetfeature import MapToolGetFeature
from ui_linker import Ui_linker	


class linker( QDockWidget , Ui_linker ):
	def __init__(self,iface,layer):
		self.iface = iface		
		self.layer = layer
		self.settings = LinkItSettings()
		self.provider = layer.dataProvider()
		# UI setup
		QDockWidget.__init__(self)
		self.setupUi(self)
		self.cancelButton.hide()
		self.iface.addDockWidget(Qt.LeftDockWidgetArea,self)
		self.setVisible(False)

	def unload(self):
		self.iface.removeDockWidget(self)
		
	def fieldIndex(self):
		return self.provider.fieldNameIndex(self.settings.value('field'))

	def itemChanged(self,fid):
		self.clear()
		self.setVisible(True)
		self.fid = fid
		f = QgsFeature()
		try:
			if self.layer.featureAtId(fid,f,True,True) is True:
				currentValue = f.attribute(self.settings.value('field')).toString()
				self.linkedItemID.setText(currentValue)		
		except: # qgis <1.9
			idx = self.fieldIndex()
			if self.provider.featureAtId(fid,f,True,[idx]) is True:
				fieldmap = f.attributeMap()
				currentValue = fieldmap[idx].toString()
				self.linkedItemID.setText(currentValue)		

	def clear(self):
		self.setVisible(False)
		self.fid = False
		self.linkedItemID.clear()

	@pyqtSignature("on_selectButton_clicked()")
	def on_selectButton_clicked(self):	
		canvas = self.iface.mapCanvas()
		self.mapTool = MapToolGetFeature(canvas, self.layer)
		QObject.connect(self.mapTool , SIGNAL("featureIdentified") , self.featureIdentified ) 
		canvas.setMapTool(self.mapTool)
		QObject.connect( canvas, SIGNAL( "mapToolSet(QgsMapTool *)" ), self.toolChanged)
		self.selectButton.hide()
		self.cancelButton.show()

	@pyqtSignature("on_deleteButton_clicked()")
	def on_deleteButton_clicked(self):	
		self.linkedItemID.clear()

	@pyqtSignature("on_cancelButton_clicked()")
	def on_cancelButton_clicked(self):	
		canvas = self.iface.mapCanvas()
		canvas.unsetMapTool(self.mapTool)
		self.selectButton.show()
		self.cancelButton.hide()
		QObject.disconnect( canvas, SIGNAL( "mapToolSet(QgsMapTool *)" ), self.toolChanged)

	def toolChanged(self, tool):
		self.on_cancelButton_clicked()

	@pyqtSignature("on_linkedItemID_textChanged(QString)")
	def on_linkedItemID_textChanged(self,new):
		new = new.toInt()[0]
		if new==0: new = None
		self.provider.changeAttributeValues( { self.fid : {self.fieldIndex() : QVariant(new) } } )
		self.iface.mapCanvas().refresh()

	def featureIdentified(self, new):
		self.linkedItemID.setText("%u" % new)
		self.on_cancelButton_clicked()
