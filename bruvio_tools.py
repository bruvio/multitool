# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window_old.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(318, 297)
        MainWindow.setMinimumSize(QtCore.QSize(318, 297))
        MainWindow.setMaximumSize(QtCore.QSize(318, 297))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.exit_button = QtWidgets.QPushButton(self.centralwidget)
        self.exit_button.setGeometry(QtCore.QRect(210, 200, 75, 25))
        self.exit_button.setToolTip("")
        self.exit_button.setWhatsThis("")
        self.exit_button.setObjectName("exit_button")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(100, 10, 171, 22))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 40, 101, 151))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.edge2d_button = QtWidgets.QPushButton(self.layoutWidget)
        self.edge2d_button.setToolTip("")
        self.edge2d_button.setWhatsThis("")
        self.edge2d_button.setObjectName("edge2d_button")
        self.verticalLayout.addWidget(self.edge2d_button)
        self.magsurf_button = QtWidgets.QPushButton(self.layoutWidget)
        self.magsurf_button.setToolTip("")
        self.magsurf_button.setWhatsThis("")
        self.magsurf_button.setObjectName("magsurf_button")
        self.verticalLayout.addWidget(self.magsurf_button)
        self.eqdsk_button = QtWidgets.QPushButton(self.layoutWidget)
        self.eqdsk_button.setToolTip("")
        self.eqdsk_button.setWhatsThis("")
        self.eqdsk_button.setObjectName("eqdsk_button")
        self.verticalLayout.addWidget(self.eqdsk_button)
        self.readdata_button = QtWidgets.QPushButton(self.layoutWidget)
        self.readdata_button.setToolTip("")
        self.readdata_button.setWhatsThis("")
        self.readdata_button.setObjectName("readdata_button")
        self.verticalLayout.addWidget(self.readdata_button)
        self.title_2 = QtWidgets.QLabel(self.centralwidget)
        self.title_2.setGeometry(QtCore.QRect(120, 230, 201, 22))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.title_2.setFont(font)
        self.title_2.setObjectName("title_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 318, 20))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionOpen_PDF_guide = QtWidgets.QAction(MainWindow)
        self.actionOpen_PDF_guide.setObjectName("actionOpen_PDF_guide")
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionOpen_PDF_guide)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "bruvio tools"))
        self.exit_button.setText(_translate("MainWindow", "Exit"))
        self.title.setText(_translate("MainWindow", "bruvio tools"))
        self.edge2d_button.setText(_translate("MainWindow", "Edge2d"))
        self.magsurf_button.setText(_translate("MainWindow", "MagSurf"))
        self.eqdsk_button.setText(_translate("MainWindow", "EQDSK"))
        self.readdata_button.setText(_translate("MainWindow", "plot data"))
        self.title_2.setText(_translate("MainWindow", "by Bruno Viola (bruno.viola@ukaea.uk)"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionOpen_PDF_guide.setText(_translate("MainWindow", "Open PDF guide"))

