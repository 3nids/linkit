# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_linker.ui'
#
# Created: Thu Mar 29 17:05:12 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_linker(object):
    def setupUi(self, linker):
        linker.setObjectName(_fromUtf8("linker"))
        linker.resize(198, 101)
        linker.setWindowTitle(QtGui.QApplication.translate("linker", "Link It", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout_3 = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.idParent = QtGui.QLineEdit(self.dockWidgetContents)
        self.idParent.setObjectName(_fromUtf8("idParent"))
        self.gridLayout_3.addWidget(self.idParent, 1, 2, 1, 2)
        self.selectButton = QtGui.QToolButton(self.dockWidgetContents)
        self.selectButton.setText(QtGui.QApplication.translate("linker", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton.setObjectName(_fromUtf8("selectButton"))
        self.gridLayout_3.addWidget(self.selectButton, 2, 2, 1, 1)
        self.deleteButton = QtGui.QToolButton(self.dockWidgetContents)
        self.deleteButton.setText(QtGui.QApplication.translate("linker", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.gridLayout_3.addWidget(self.deleteButton, 2, 0, 1, 1)
        self.cancelButton = QtGui.QToolButton(self.dockWidgetContents)
        self.cancelButton.setText(QtGui.QApplication.translate("linker", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.gridLayout_3.addWidget(self.cancelButton, 2, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setText(QtGui.QApplication.translate("linker", "Item ID", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        linker.setWidget(self.dockWidgetContents)

        self.retranslateUi(linker)
        QtCore.QMetaObject.connectSlotsByName(linker)

    def retranslateUi(self, linker):
        pass

