# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_linker.ui'
#
# Created: Wed Jun 26 10:17:28 2013
#      by: PyQt4 UI code generator 4.9.1
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
        linker.resize(218, 143)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.formLayout = QtGui.QFormLayout(self.dockWidgetContents)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.dockWidgetContents)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.featureIdLabel = QtGui.QLabel(self.dockWidgetContents)
        self.featureIdLabel.setText(_fromUtf8(""))
        self.featureIdLabel.setObjectName(_fromUtf8("featureIdLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.featureIdLabel)
        self.label_2 = QtGui.QLabel(self.dockWidgetContents)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.linkedItemID = QtGui.QLineEdit(self.dockWidgetContents)
        self.linkedItemID.setObjectName(_fromUtf8("linkedItemID"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.linkedItemID)
        self.widget = QtGui.QWidget(self.dockWidgetContents)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cancelButton = QtGui.QToolButton(self.widget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../icons/cancel.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancelButton.setIcon(icon)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.gridLayout.addWidget(self.cancelButton, 0, 4, 1, 1)
        self.drawButton = QtGui.QToolButton(self.widget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../icons/drawline.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.drawButton.setIcon(icon1)
        self.drawButton.setObjectName(_fromUtf8("drawButton"))
        self.gridLayout.addWidget(self.drawButton, 0, 0, 1, 1)
        self.deleteButton = QtGui.QToolButton(self.widget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("../icons/delete.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon2)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.gridLayout.addWidget(self.deleteButton, 0, 2, 1, 1)
        self.selectButton = QtGui.QToolButton(self.widget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("../icons/maptool.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.selectButton.setIcon(icon3)
        self.selectButton.setObjectName(_fromUtf8("selectButton"))
        self.gridLayout.addWidget(self.selectButton, 0, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.widget)
        linker.setWidget(self.dockWidgetContents)

        self.retranslateUi(linker)
        QtCore.QMetaObject.connectSlotsByName(linker)

    def retranslateUi(self, linker):
        linker.setWindowTitle(QtGui.QApplication.translate("linker", "Link It", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("linker", "Feature ID", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("linker", "Linked ID", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("linker", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.drawButton.setText(QtGui.QApplication.translate("linker", "Draw line", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("linker", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton.setText(QtGui.QApplication.translate("linker", "Select", None, QtGui.QApplication.UnicodeUTF8))

