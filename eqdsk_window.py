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
        eqdsk_window.resize(701, 424)
        eqdsk_window.setMinimumSize(QtCore.QSize(701, 424))
        eqdsk_window.setMaximumSize(QtCore.QSize(701, 424))
        self.centralwidget = QtGui.QWidget(eqdsk_window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(30, 30, 651, 351))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.lineEdit_eqdskname = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_eqdskname.setGeometry(QtCore.QRect(10, 40, 171, 21))
        self.lineEdit_eqdskname.setObjectName(_fromUtf8("lineEdit_eqdskname"))
        self.select_eqdsk = QtGui.QPushButton(self.groupBox_3)
        self.select_eqdsk.setGeometry(QtCore.QRect(190, 40, 21, 21))
        self.select_eqdsk.setObjectName(_fromUtf8("select_eqdsk"))
        self.groupBox = QtGui.QGroupBox(self.groupBox_3)
        self.groupBox.setGeometry(QtCore.QRect(230, 20, 131, 80))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.radioButton_efit = QtGui.QRadioButton(self.groupBox)
        self.radioButton_efit.setGeometry(QtCore.QRect(10, 20, 101, 20))
        self.radioButton_efit.setObjectName(_fromUtf8("radioButton_efit"))
        self.radioButton_other = QtGui.QRadioButton(self.groupBox)
        self.radioButton_other.setGeometry(QtCore.QRect(10, 50, 111, 20))
        self.radioButton_other.setObjectName(_fromUtf8("radioButton_other"))
        self.pushButton_read = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_read.setGeometry(QtCore.QRect(10, 100, 111, 25))
        self.pushButton_read.setObjectName(_fromUtf8("pushButton_read"))
        self.lineEdit_psioffset = QtGui.QLineEdit(self.groupBox_3)
        self.lineEdit_psioffset.setGeometry(QtCore.QRect(10, 130, 171, 21))
        self.lineEdit_psioffset.setObjectName(_fromUtf8("lineEdit_psioffset"))
        self.pushButton_writematrix = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_writematrix.setGeometry(QtCore.QRect(440, 40, 141, 25))
        self.pushButton_writematrix.setObjectName(_fromUtf8("pushButton_writematrix"))
        self.pushButton_lcmsmap = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_lcmsmap.setGeometry(QtCore.QRect(440, 110, 111, 25))
        self.pushButton_lcmsmap.setObjectName(_fromUtf8("pushButton_lcmsmap"))
        self.pushButton_solmap = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_solmap.setGeometry(QtCore.QRect(440, 170, 111, 25))
        self.pushButton_solmap.setObjectName(_fromUtf8("pushButton_solmap"))
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox_3)
        self.groupBox_2.setGeometry(QtCore.QRect(430, 10, 171, 191))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.pushButton_openinputfile = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_openinputfile.setGeometry(QtCore.QRect(10, 70, 111, 25))
        self.pushButton_openinputfile.setObjectName(_fromUtf8("pushButton_openinputfile"))
        self.eqdsk_exit = QtGui.QPushButton(self.groupBox_3)
        self.eqdsk_exit.setGeometry(QtCore.QRect(480, 320, 101, 21))
        self.eqdsk_exit.setObjectName(_fromUtf8("eqdsk_exit"))
        self.pushButton_lcmsmapX = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_lcmsmapX.setGeometry(QtCore.QRect(440, 140, 111, 25))
        self.pushButton_lcmsmapX.setObjectName(_fromUtf8("pushButton_lcmsmapX"))
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox_3)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 180, 360, 145))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_getmagneticdata = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_getmagneticdata.setObjectName(_fromUtf8("pushButton_getmagneticdata"))
        self.gridLayout.addWidget(self.pushButton_getmagneticdata, 0, 0, 1, 1)
        self.lineEdit_labelIN = QtGui.QLineEdit(self.groupBox_4)
        self.lineEdit_labelIN.setObjectName(_fromUtf8("lineEdit_labelIN"))
        self.gridLayout.addWidget(self.lineEdit_labelIN, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox_4)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 2, 1, 1)
        self.pushButton_writemagneticdata = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_writemagneticdata.setObjectName(_fromUtf8("pushButton_writemagneticdata"))
        self.gridLayout.addWidget(self.pushButton_writemagneticdata, 1, 0, 1, 1)
        self.lineEdit_labelOUT = QtGui.QLineEdit(self.groupBox_4)
        self.lineEdit_labelOUT.setObjectName(_fromUtf8("lineEdit_labelOUT"))
        self.gridLayout.addWidget(self.lineEdit_labelOUT, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_4)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)
        self.checkBox_normalize = QtGui.QCheckBox(self.groupBox_4)
        self.checkBox_normalize.setObjectName(_fromUtf8("checkBox_normalize"))
        self.gridLayout.addWidget(self.checkBox_normalize, 2, 0, 1, 1)
        self.checkBox_invert = QtGui.QCheckBox(self.groupBox_4)
        self.checkBox_invert.setObjectName(_fromUtf8("checkBox_invert"))
        self.gridLayout.addWidget(self.checkBox_invert, 3, 0, 1, 1)
        self.groupBox_2.raise_()
        self.groupBox.raise_()
        self.lineEdit_eqdskname.raise_()
        self.select_eqdsk.raise_()
        self.pushButton_read.raise_()
        self.lineEdit_psioffset.raise_()
        self.pushButton_writematrix.raise_()
        self.pushButton_lcmsmap.raise_()
        self.pushButton_solmap.raise_()
        self.eqdsk_exit.raise_()
        self.pushButton_lcmsmapX.raise_()
        self.groupBox_4.raise_()
        eqdsk_window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(eqdsk_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 701, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        eqdsk_window.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(eqdsk_window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        eqdsk_window.setStatusBar(self.statusbar)

        self.retranslateUi(eqdsk_window)
        QtCore.QMetaObject.connectSlotsByName(eqdsk_window)

    def retranslateUi(self, eqdsk_window):
        eqdsk_window.setWindowTitle(_translate("eqdsk_window", "eqdsk tools", None))
        self.groupBox_3.setTitle(_translate("eqdsk_window", "EQDSK", None))
        self.select_eqdsk.setText(_translate("eqdsk_window", "...", None))
        self.groupBox.setTitle(_translate("eqdsk_window", "source", None))
        self.radioButton_efit.setText(_translate("eqdsk_window", "eFit", None))
        self.radioButton_other.setText(_translate("eqdsk_window", "other", None))
        self.pushButton_read.setText(_translate("eqdsk_window", "read", None))
        self.lineEdit_psioffset.setText(_translate("eqdsk_window", "7.4032", None))
        self.pushButton_writematrix.setText(_translate("eqdsk_window", "write_input_matrix", None))
        self.pushButton_lcmsmap.setText(_translate("eqdsk_window", "run LCMSmap", None))
        self.pushButton_solmap.setText(_translate("eqdsk_window", "run SOLmap", None))
        self.groupBox_2.setTitle(_translate("eqdsk_window", "mapping tools", None))
        self.pushButton_openinputfile.setText(_translate("eqdsk_window", "open input file", None))
        self.eqdsk_exit.setText(_translate("eqdsk_window", "exit", None))
        self.pushButton_lcmsmapX.setText(_translate("eqdsk_window", "run LCMSXmap", None))
        self.groupBox_4.setTitle(_translate("eqdsk_window", "magnetic data", None))
        self.pushButton_getmagneticdata.setText(_translate("eqdsk_window", "get magnetic data", None))
        self.lineEdit_labelIN.setText(_translate("eqdsk_window", "LFE_81472", None))
        self.label.setText(_translate("eqdsk_window", "label IN", None))
        self.pushButton_writemagneticdata.setText(_translate("eqdsk_window", "write magnetic data", None))
        self.lineEdit_labelOUT.setText(_translate("eqdsk_window", "LFEexp_JET_python", None))
        self.label_2.setText(_translate("eqdsk_window", "label OUT", None))
        self.checkBox_normalize.setText(_translate("eqdsk_window", "normalize", None))
        self.checkBox_invert.setText(_translate("eqdsk_window", "invert", None))

