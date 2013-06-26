# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_linkeditor.ui'
#
# Created: Tue Jun 25 15:53:41 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LinkEditor(object):
    def setupUi(self, LinkEditor):
        LinkEditor.setObjectName(_fromUtf8("LinkEditor"))
        LinkEditor.resize(343, 206)
        self.gridLayout_2 = QtGui.QGridLayout(LinkEditor)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.buttonBox = QtGui.QDialogButtonBox(LinkEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 7, 1, 1, 2)
        self.destinationLayer = QtGui.QComboBox(LinkEditor)
        self.destinationLayer.setObjectName(_fromUtf8("destinationLayer"))
        self.gridLayout_2.addWidget(self.destinationLayer, 2, 2, 1, 1)
        self.label_2 = QtGui.QLabel(LinkEditor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 5, 0, 1, 1)
        self.label_4 = QtGui.QLabel(LinkEditor)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 2)
        self.label = QtGui.QLabel(LinkEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.sourceLayer = QtGui.QComboBox(LinkEditor)
        self.sourceLayer.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.sourceLayer.setObjectName(_fromUtf8("sourceLayer"))
        self.gridLayout_2.addWidget(self.sourceLayer, 5, 2, 1, 1)
        self.label_5 = QtGui.QLabel(LinkEditor)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 2)
        self.destinationField = QtGui.QComboBox(LinkEditor)
        self.destinationField.setObjectName(_fromUtf8("destinationField"))
        self.gridLayout_2.addWidget(self.destinationField, 4, 2, 1, 1)
        self.linkName = QtGui.QLineEdit(LinkEditor)
        self.linkName.setObjectName(_fromUtf8("linkName"))
        self.gridLayout_2.addWidget(self.linkName, 0, 2, 1, 1)

        self.retranslateUi(LinkEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LinkEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LinkEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(LinkEditor)

    def retranslateUi(self, LinkEditor):
        LinkEditor.setWindowTitle(QtGui.QApplication.translate("LinkEditor", "Link It :: Link editor", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("LinkEditor", "Source layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("LinkEditor", "Destination layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LinkEditor", "Link name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("LinkEditor", "Destination field", None, QtGui.QApplication.UnicodeUTF8))

