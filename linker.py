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
from ui_linker import Ui_linker

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

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
		
	def layer(self):
		return self.settings.value("layer")
		
	def itemChanged(self,fid):
		self.clear()
		self.setVisible(True)
		self.fid      = fid
		self.idFieldPos     = self.provider.fieldNameIndex('id')
		self.parentFieldPos = self.provider.fieldNameIndex('id_parent')
		f = QgsFeature()
		if self.provider.featureAtId(fid,f,True,[self.parentFieldPos]) is True:
			fieldmap = f.attributeMap()
			idParent = fieldmap[self.parentFieldPos].toString()
			self.idParent.setText(idParent)		
		
	def clear(self):
		self.setVisible(False)
		self.fid = False
		self.idParent.clear()

	@pyqtSignature("on_selectButton_clicked()")
	def on_selectButton_clicked(self):	
		canvas = self.iface.mapCanvas()
		self.getNeighbor = getNeighbor(canvas)
		QObject.connect(self.getNeighbor , SIGNAL("canvasClickedWithModifiers") , self.onCanvasClicked ) 
		canvas.setMapTool(self.getNeighbor)
		QObject.connect( canvas, SIGNAL( "mapToolSet(QgsMapTool *)" ), self.toolChanged)
		self.selectButton.hide()
		self.cancelButton.show()

	@pyqtSignature("on_deleteButton_clicked()")
	def on_deleteButton_clicked(self):	
		self.idParent.clear()
	
	@pyqtSignature("on_cancelButton_clicked()")
	def on_cancelButton_clicked(self):	
		canvas = self.iface.mapCanvas()
		canvas.unsetMapTool(self.getNeighbor)
		self.selectButton.show()
		self.cancelButton.hide()
		QObject.disconnect( canvas, SIGNAL( "mapToolSet(QgsMapTool *)" ), self.toolChanged)

	def toolChanged(self, tool):
		self.on_cancelButton_clicked()

	@pyqtSignature("on_idParent_textChanged(QString)")
	def on_idParent_textChanged(self,new):
		new = new.toInt()[0] # If new is empty (string), then a NULL value is stored based on SQL rule
		self.provider.changeAttributeValues( { self.fid : {self.parentFieldPos : QVariant(new) } } )

	def onCanvasClicked(self, point, button, modifiers):
		if button != Qt.LeftButton:
			return
		canvas = self.iface.mapCanvas()
		point = canvas.mapRenderer().mapToLayerCoordinates(self.layer, point)

		pixTolerance = 10
		mapTolerance = pixTolerance * canvas.mapUnitsPerPixel()
		rect = QgsRectangle(point.x()-mapTolerance,point.y()-mapTolerance,point.x()+mapTolerance,point.y()+mapTolerance)

		self.provider.select([self.idFieldPos], rect, True, True)
		subset = []
		f = QgsFeature()
		while (self.provider.nextFeature(f)):
			subset.append(f)
		if len(subset) > 1:
			QMessageBox.warning( self, "Link It", QApplication.translate("LinkIt", "Two items have been selected. Please select only one item.", None, QApplication.UnicodeUTF8) )
			return
		if len(subset) == 1:
			fieldmap=subset[0].attributeMap()
			self.idParent.setText(fieldmap[self.idFieldPos].toString())
			self.on_cancelButton_clicked()
			canvas.refresh()


class getNeighbor(QgsMapToolEmitPoint):
	def __init__(self, canvas):
		QgsMapToolEmitPoint.__init__(self, canvas)

	def canvasPressEvent(self, mouseEvent):
		point = self.toMapCoordinates( mouseEvent.pos() )
		self.emit( SIGNAL( "canvasClickedWithModifiers" ), point, mouseEvent.button(), mouseEvent.modifiers() )

