# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotdata.ui'
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

class Ui_plotdata_window(object):
    def setupUi(self, plotdata_window):
        plotdata_window.setObjectName(_fromUtf8("plotdata_window"))
        plotdata_window.resize(417, 328)
        self.centralwidget = QtGui.QWidget(plotdata_window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.formLayout = QtGui.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_4)
        self.textEdit_pulselist = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_pulselist.setObjectName(_fromUtf8("textEdit_pulselist"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.textEdit_pulselist)
        self.selectfile = QtGui.QPushButton(self.centralwidget)
        self.selectfile.setObjectName(_fromUtf8("selectfile"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.selectfile)
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.checkBox)
        self.plotbutton = QtGui.QPushButton(self.centralwidget)
        self.plotbutton.setObjectName(_fromUtf8("plotbutton"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.plotbutton)
        self.smooth_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.smooth_checkBox.setObjectName(_fromUtf8("smooth_checkBox"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.smooth_checkBox)
        self.savefigure_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.savefigure_checkBox.setObjectName(_fromUtf8("savefigure_checkBox"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.savefigure_checkBox)
        plotdata_window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(plotdata_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 417, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        plotdata_window.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(plotdata_window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        plotdata_window.setStatusBar(self.statusbar)

        self.retranslateUi(plotdata_window)
        QtCore.QMetaObject.connectSlotsByName(plotdata_window)

    def retranslateUi(self, plotdata_window):
        plotdata_window.setWindowTitle(_translate("plotdata_window", "plot time traces", None))
        self.label_4.setText(_translate("plotdata_window", "<html><head/><body><p><span style=\" font-weight:600;\">Pulse list</span></p></body></html>", None))
        self.selectfile.setText(_translate("plotdata_window", "select dataset", None))
        self.checkBox.setText(_translate("plotdata_window", "edit_JSON", None))
        self.plotbutton.setText(_translate("plotdata_window", "plot time traces", None))
        self.smooth_checkBox.setText(_translate("plotdata_window", "smooth", None))
        self.savefigure_checkBox.setText(_translate("plotdata_window", "save Figure", None))

