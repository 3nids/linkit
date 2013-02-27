"""
QGIS - Layer Field Combo class

Denis Rouzaud
denis.rouzaud@gmail.com
Jan. 2012

This class is useful if you want to simply manage a layer combo with one (or several) field combos.
The field combos are filled with the column name of the currently selected layer in the layer combo.
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

# creates a layer combo:
# 	combo: the qcombobox widget
#	settingIDLambda: a lambda function returning the ID of the initially selected layer (it could look for a value in settings)
#	geomType: restrain the possible selection of layers to a certain type of geometry [not working yet]
class LayerCombo():
	def __init__(self,combo,settingIDLambda=lambda:"",geomType=None):
		self.combo = combo
		self.settingIDLambda = settingIDLambda
		self.geomType = geomType	

# creates a field combo:
# 	combo: the qcombobox widget
#	settingIDLambda: a lambda function returning the ID of the initially selected field (it could look for a value in settings)
#	checkType: restrain the possible selection to a certain type of field
class FieldCombo():
	def __init__(self,combo,settingIDLambda=lambda:"",fieldType=None):
		self.combo = combo
		self.settingIDLambda = settingIDLambda
		self.fieldType = fieldType

class LayerFieldCombo():
	def __init__(self, canvas, dialog, layerCombo, fieldsCombos=[]):
		self.canvas = canvas
		self.layerCombo = layerCombo
		self.fieldsCombos = fieldsCombos
		self.layerList = []
		# connect combos
		#self.layerChangedLambda = lambda(i): self.layerChanged(i)
		#self.fieldChangedLambda = lambda(i): self.fieldChanged(i,dialog.sender())
		#QObject.connect(self.layerCombo.combo, SIGNAL("currentIndexChanged(int)"), self.layerChangedLambda)
		QObject.connect(self.layerCombo.combo, SIGNAL("currentIndexChanged(int)"), self.layerChanged)
		for field in fields:
			#QObject.connect(field.combo, SIGNAL("currentIndexChanged(int)"), self.fieldChangedLambda)
			QObject.connect(field.combo, SIGNAL("currentIndexChanged(int)"), self.fieldChanged)
		QObject.connect(self.iface.mapCanvas() , SIGNAL("layersChanged ()") , self.canvasLayersChanged )
		
	def getLayer(self):
		i = self.layerCombo.combo.currentIndex()
		if i == 0: return False
		layerId = self.layerCombo.combo.itemData( i )
		return QgsMapLayerRegistry.instance().mapLayer( layerId )

	def canvasLayersChanged(self):
		self.layerCombo.combo.clear()
		self.layerCombo.combo.addItem("")
		for layer in self.canvas.layers():
			if layer.type() != QgsMapLayer.VectorLayer or layer.hasGeometryType() is False:
				continue
			self.layerCombo.combo.addItem( layer.name() , layer.id() )
			if layer.id() == self.layerCombo.settingIDLambda(): self.layerCombo.combo.setCurrentIndex( )
		self.updateFieldsCombo()
		#QObject.connect(self.layerCombo.combo, SIGNAL("currentIndexChanged(int)"), self.layerChanged)

	def updateFieldsCombo(self):
		for field in self.fieldsCombos:
			field.combo.clear()
			field.combo.addItem("")
			if self.getLayer() is False: continue
			for i,fieldItem in enumerate( self.getLayer().dataProvider().fieldNameMap() ):
				field.combo.addItem( fieldItem )
				if fieldItem == field.settingIDLambda():
					field.combo.setCurrentIndex(i+1)

	def layerChanged(self,i):
		error_msg = ''
		if i > 0:
			layer = self.layerList[i-1]
			# TODO CHECK GEOMETRY
			print "TODO CHECK GEOMETRY",layer.dataProvider().geometryType() , layer.geometryType()
		if error_msg != '':
			self.dimensionLayerCombo.setCurrentIndex(0)
			QMessageBox.warning( self , "Bad Layer", error_msg )
		# update field list
		self.updateFieldsCombo()

	def fieldChanged(self,i,sender):
		field = None
		for testField in self.fieldsCombos:
			if testField.combo == sender:
				 field = testField
				 break
		if field is None: raise NameError('LayerFieldCombo: cannot find field')
		if self.getLayer() is not False and i > 0:
			fieldName = field.combo.currentText()
			i = self.getLayer().dataProvider().fieldNameIndex(fieldName)
			# http://qgis.org/api/classQgsField.html#a00409d57dc65d6155c6d08085ea6c324
			# http://developer.qt.nokia.com/doc/qt-4.8/qmetatype.html#Type-enum
			if self.getLayer().dataProvider().fields()[i].type() != field.fieldType:
				QMessageBox.warning( self , "Bad field" ,  QApplication.translate("Layer Field Combo", "The field must be a %s" % field.type, None, QApplication.UnicodeUTF8) )
				field.combo.setCurrentIndex(0)	
