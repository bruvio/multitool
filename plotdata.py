# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotdata.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_plotdata_window(object):
    def setupUi(self, plotdata_window):
        plotdata_window.setObjectName("plotdata_window")
        plotdata_window.resize(417, 328)
        self.centralwidget = QtWidgets.QWidget(plotdata_window)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.textEdit_pulselist = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_pulselist.setObjectName("textEdit_pulselist")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.textEdit_pulselist)
        self.calcmean_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.calcmean_checkBox.setObjectName("calcmean_checkBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.calcmean_checkBox)
        self.smooth_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.smooth_checkBox.setObjectName("smooth_checkBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.smooth_checkBox)
        self.selectfile = QtWidgets.QPushButton(self.centralwidget)
        self.selectfile.setObjectName("selectfile")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.selectfile)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.checkBox)
        self.plotbutton = QtWidgets.QPushButton(self.centralwidget)
        self.plotbutton.setObjectName("plotbutton")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.plotbutton)
        self.savefigure_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.savefigure_checkBox.setObjectName("savefigure_checkBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.savefigure_checkBox)
        plotdata_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(plotdata_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 417, 20))
        self.menubar.setObjectName("menubar")
        plotdata_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(plotdata_window)
        self.statusbar.setObjectName("statusbar")
        plotdata_window.setStatusBar(self.statusbar)

        self.retranslateUi(plotdata_window)
        QtCore.QMetaObject.connectSlotsByName(plotdata_window)

    def retranslateUi(self, plotdata_window):
        _translate = QtCore.QCoreApplication.translate
        plotdata_window.setWindowTitle(_translate("plotdata_window", "plot time traces"))
        self.label_4.setText(_translate("plotdata_window", "<html><head/><body><p><span style=\" font-weight:600;\">Pulse list</span></p></body></html>"))
        self.calcmean_checkBox.setText(_translate("plotdata_window", "calc. mean"))
        self.smooth_checkBox.setText(_translate("plotdata_window", "smooth"))
        self.selectfile.setText(_translate("plotdata_window", "select dataset"))
        self.checkBox.setText(_translate("plotdata_window", "edit_JSON"))
        self.plotbutton.setText(_translate("plotdata_window", "plot time traces"))
        self.savefigure_checkBox.setText(_translate("plotdata_window", "save Figure"))

