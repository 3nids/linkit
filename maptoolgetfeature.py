"""
Link It
QGIS plugin

Denis Rouzaud
denis.rouzaud@gmail.com
Feb. 2013
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

try:
	from qgis.gui import QgsMapToolIdentify 
except:
	from qgis.gui import QgsMapTool as QgsMapToolIdentify 	


class MapToolGetFeature(QgsMapToolIdentify):
	def __init__(self, canvas, layer):
		self.layer = layer
		self.canvas = canvas
		QgsMapToolEmitPoint.__init__(self, canvas)


	def canvasReleaseEvent(self, mouseEvent):
		try:
			results = self.identify(mouseEvent.x(),mouseEvent.y(), [self.layer], self.TopDownStopAtFirst)
			if len(results) > 0:
				self.emit( SIGNAL( "featureIdentified" ), results[0].mFeature.id() )
				
		except: # qgis < 1.9
			point = self.toMapCoordinates( mouseEvent.pos() )
			point = self.canvas.mapRenderer().mapToLayerCoordinates(self.layer, point)
			pixTolerance = 6
			mapTolerance = pixTolerance * self.canvas.mapUnitsPerPixel()
			rect = QgsRectangle(point.x()-mapTolerance,point.y()-mapTolerance,point.x()+mapTolerance,point.y()+mapTolerance)
			provider = self.layer.dataProvider()
			provider.select([], rect, True, True)
			subset = []
			f = QgsFeature()
			while (provider.nextFeature(f)):
				subset.append(f)
			if len(subset) == 0:
				return
			if len(subset) > 1:
				idx = QgsSpatialIndex()
				for f in subset:
					idx.insertFeature(f)
				nearest = idx.nearestNeighbor( point, 1 )
				layer.featureAtId(nearest[0],f, True, False)
			self.emit( SIGNAL( "featureIdentified" ), f.id() )	
