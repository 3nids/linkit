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

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
class LinkItSettings():
	def __init__(self):
		# load settings
		self.pluginName = "LinkIt"
		self.settings = QSettings(self.pluginName,self.pluginName)
		self.globalDefaultValue = {}                                    
		self.projectDefaultValue = {"layer": "", "field": ""}
	
	def value(self,setting):
		if setting in self.globalDefaultValue:
			return self.settings.value( setting, self.globalDefaultValue[setting] )
		elif setting in self.projectDefaultValue:
			return QgsProject.instance().readEntry( self.pluginName, setting , self.projectDefaultValue[setting] )[0]
		else:
			raise NameError('IntersectIt has no setting %s' % setting)
		
	def setValue(self,setting,value):
		if setting in self.globalDefaultValue:
			self.settings.setValue( setting, value )
		elif setting in self.projectDefaultValue:
			QgsProject.instance().writeEntry( self.pluginName, setting , value )
		else:
			raise NameError('IntersectIt has no setting %s' % setting)
