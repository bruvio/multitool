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
        plotdata_window.setMinimumSize(QtCore.QSize(417, 328))
        plotdata_window.setMaximumSize(QtCore.QSize(417, 328))
        self.centralwidget = QtWidgets.QWidget(plotdata_window)
        self.centralwidget.setObjectName("centralwidget")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(9, 9, 67, 16))
        self.label_4.setObjectName("label_4")
        self.textEdit_pulselist = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_pulselist.setGeometry(QtCore.QRect(9, 30, 196, 161))
        self.textEdit_pulselist.setObjectName("textEdit_pulselist")
        self.calcmean_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.calcmean_checkBox.setGeometry(QtCore.QRect(211, 30, 94, 20))
        self.calcmean_checkBox.setObjectName("calcmean_checkBox")
        self.smooth_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.smooth_checkBox.setGeometry(QtCore.QRect(211, 197, 73, 20))
        self.smooth_checkBox.setObjectName("smooth_checkBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.smooth_checkBox)
        self.selectfile = QtWidgets.QPushButton(self.centralwidget)
        self.selectfile.setGeometry(QtCore.QRect(9, 223, 101, 25))
        self.selectfile.setObjectName("selectfile")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(211, 225, 87, 20))
        self.checkBox.setObjectName("checkBox")
        self.plotbutton = QtWidgets.QPushButton(self.centralwidget)
        self.plotbutton.setGeometry(QtCore.QRect(9, 254, 112, 25))
        self.plotbutton.setObjectName("plotbutton")
        self.savefigure_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.savefigure_checkBox.setGeometry(QtCore.QRect(211, 256, 96, 20))
        self.savefigure_checkBox.setObjectName("savefigure_checkBox")
        self.search_window = QtWidgets.QTextEdit(self.centralwidget)
        self.search_window.setGeometry(QtCore.QRect(211, 56, 197, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_window.sizePolicy().hasHeightForWidth())
        self.search_window.setSizePolicy(sizePolicy)
        self.search_window.setMinimumSize(QtCore.QSize(1, 0))
        self.search_window.setObjectName("search_window")
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

