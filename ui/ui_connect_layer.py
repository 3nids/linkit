# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_connect_layer.ui'
#
# Created: Fri Jun 21 15:11:54 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_connectLayer(object):
    def setupUi(self, connectLayer):
        connectLayer.setObjectName(_fromUtf8("connectLayer"))
        connectLayer.resize(427, 111)
        self.gridLayout = QtGui.QGridLayout(connectLayer)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(connectLayer)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.layer = QtGui.QComboBox(connectLayer)
        self.layer.setObjectName(_fromUtf8("layer"))
        self.gridLayout.addWidget(self.layer, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(connectLayer)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.field = QtGui.QComboBox(connectLayer)
        self.field.setObjectName(_fromUtf8("field"))
        self.gridLayout.addWidget(self.field, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(connectLayer)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(connectLayer)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), connectLayer.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), connectLayer.reject)
        QtCore.QMetaObject.connectSlotsByName(connectLayer)

    def retranslateUi(self, connectLayer):
        connectLayer.setWindowTitle(QtGui.QApplication.translate("connectLayer", "Link It :: connect layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("connectLayer", "Connect layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("connectLayer", "Save linked item ID in field", None, QtGui.QApplication.UnicodeUTF8))

