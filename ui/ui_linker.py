# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_linker.ui'
#
# Created: Wed Jun 26 14:22:15 2013
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
        linker.resize(242, 140)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout_3 = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout_3.setSpacing(3)
        self.gridLayout_3.setContentsMargins(0, 3, 3, 3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.frame = QtGui.QFrame(self.dockWidgetContents)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setMargin(3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.widget = QtGui.QWidget(self.frame)
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
        self.gridLayout_2.addWidget(self.widget, 3, 0, 1, 3)
        self.linkedItemID = QtGui.QLineEdit(self.frame)
        self.linkedItemID.setObjectName(_fromUtf8("linkedItemID"))
        self.gridLayout_2.addWidget(self.linkedItemID, 2, 1, 1, 2)
        self.featureIdLabel = QtGui.QLabel(self.frame)
        self.featureIdLabel.setText(_fromUtf8(""))
        self.featureIdLabel.setObjectName(_fromUtf8("featureIdLabel"))
        self.gridLayout_2.addWidget(self.featureIdLabel, 0, 1, 1, 2)
        self.gridLayout_3.addWidget(self.frame, 0, 0, 2, 2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 2, 0, 1, 1)
        linker.setWidget(self.dockWidgetContents)

        self.retranslateUi(linker)
        QtCore.QMetaObject.connectSlotsByName(linker)

    def retranslateUi(self, linker):
        linker.setWindowTitle(QtGui.QApplication.translate("linker", "Link It", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("linker", "Linked ID", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("linker", "Feature ID", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("linker", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.drawButton.setText(QtGui.QApplication.translate("linker", "Draw line", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("linker", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.selectButton.setText(QtGui.QApplication.translate("linker", "Select", None, QtGui.QApplication.UnicodeUTF8))

