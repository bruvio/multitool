# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eqdsk_window.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_eqdsk_window(object):
    def setupUi(self, eqdsk_window):
        eqdsk_window.setObjectName(_fromUtf8("eqdsk_window"))
        eqdsk_window.resize(284, 223)
        self.centralwidget = QtGui.QWidget(eqdsk_window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.savefigure_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.savefigure_checkBox.setObjectName(_fromUtf8("savefigure_checkBox"))
        self.gridLayout.addWidget(self.savefigure_checkBox, 0, 1, 1, 1)
        self.plotbutton = QtGui.QPushButton(self.centralwidget)
        self.plotbutton.setObjectName(_fromUtf8("plotbutton"))
        self.gridLayout.addWidget(self.plotbutton, 2, 0, 1, 1)
        self.selectfile = QtGui.QPushButton(self.centralwidget)
        self.selectfile.setObjectName(_fromUtf8("selectfile"))
        self.gridLayout.addWidget(self.selectfile, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.KG1L_radio_2 = QtGui.QRadioButton(self.groupBox_2)
        self.KG1L_radio_2.setToolTip(_fromUtf8(""))
        self.KG1L_radio_2.setWhatsThis(_fromUtf8(""))
        self.KG1L_radio_2.setObjectName(_fromUtf8("KG1L_radio_2"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.KG1L_radio_2)
        self.KG1H_radio_2 = QtGui.QRadioButton(self.groupBox_2)
        self.KG1H_radio_2.setToolTip(_fromUtf8(""))
        self.KG1H_radio_2.setWhatsThis(_fromUtf8(""))
        self.KG1H_radio_2.setObjectName(_fromUtf8("KG1H_radio_2"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.KG1H_radio_2)
        self.gridLayout.addWidget(self.groupBox_2, 1, 1, 1, 1)
        self.eqdsk_exit = QtGui.QPushButton(self.centralwidget)
        self.eqdsk_exit.setObjectName(_fromUtf8("eqdsk_exit"))
        self.gridLayout.addWidget(self.eqdsk_exit, 2, 1, 1, 1)
        eqdsk_window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(eqdsk_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 284, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        eqdsk_window.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(eqdsk_window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        eqdsk_window.setStatusBar(self.statusbar)

        self.retranslateUi(eqdsk_window)
        QtCore.QMetaObject.connectSlotsByName(eqdsk_window)

    def retranslateUi(self, eqdsk_window):
        eqdsk_window.setWindowTitle(_translate("eqdsk_window", "eqdsk tools", None))
        self.savefigure_checkBox.setText(_translate("eqdsk_window", "save Figure", None))
        self.plotbutton.setText(_translate("eqdsk_window", "plot time traces", None))
        self.selectfile.setText(_translate("eqdsk_window", "select eqdsk", None))
        self.KG1L_radio_2.setText(_translate("eqdsk_window", "KG1L", None))
        self.KG1H_radio_2.setText(_translate("eqdsk_window", "KG1H", None))
        self.eqdsk_exit.setText(_translate("eqdsk_window", "exit", None))

