# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_connect_layer.ui'
#
# Created: Thu Mar 29 16:39:45 2012
#      by: PyQt4 UI code generator 4.8.5
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
        connectLayer.resize(382, 120)
        connectLayer.setWindowTitle(QtGui.QApplication.translate("connectLayer", "Link It :: connect layer", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(connectLayer)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(connectLayer)
        self.label.setText(QtGui.QApplication.translate("connectLayer", "Connect layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.layerCombo = QtGui.QComboBox(connectLayer)
        self.layerCombo.setObjectName(_fromUtf8("layerCombo"))
        self.gridLayout.addWidget(self.layerCombo, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(connectLayer)
        self.label_2.setText(QtGui.QApplication.translate("connectLayer", "Save linked item ID in field", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.fieldCombo = QtGui.QComboBox(connectLayer)
        self.fieldCombo.setObjectName(_fromUtf8("fieldCombo"))
        self.gridLayout.addWidget(self.fieldCombo, 1, 1, 1, 1)
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
        pass

