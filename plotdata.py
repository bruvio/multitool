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
        plotdata_window.resize(300, 268)
        self.centralwidget = QtGui.QWidget(plotdata_window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.savefigure_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.savefigure_checkBox.setObjectName(_fromUtf8("savefigure_checkBox"))
        self.gridLayout.addWidget(self.savefigure_checkBox, 1, 1, 1, 1)
        self.plotbutton = QtGui.QPushButton(self.centralwidget)
        self.plotbutton.setObjectName(_fromUtf8("plotbutton"))
        self.gridLayout.addWidget(self.plotbutton, 3, 0, 1, 1)
        self.textEdit_pulselist = QtGui.QTextEdit(self.centralwidget)
        self.textEdit_pulselist.setObjectName(_fromUtf8("textEdit_pulselist"))
        self.gridLayout.addWidget(self.textEdit_pulselist, 1, 0, 1, 1)
        self.selectfile = QtGui.QPushButton(self.centralwidget)
        self.selectfile.setObjectName(_fromUtf8("selectfile"))
        self.gridLayout.addWidget(self.selectfile, 2, 0, 1, 1)
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 2, 1, 1, 1)
        plotdata_window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(plotdata_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 20))
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
        self.savefigure_checkBox.setText(_translate("plotdata_window", "save Figure", None))
        self.plotbutton.setText(_translate("plotdata_window", "plot time traces", None))
        self.selectfile.setText(_translate("plotdata_window", "select dataset", None))
        self.checkBox.setText(_translate("plotdata_window", "edit_JSON", None))

