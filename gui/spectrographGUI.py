# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\spectrographGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1036, 628)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 30, 891, 321))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.Spectrograph_Window = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.Spectrograph_Window.setContentsMargins(0, 0, 0, 0)
        self.Spectrograph_Window.setObjectName("Spectrograph_Window")
        self.StdOutBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.StdOutBrowser.setGeometry(QtCore.QRect(565, 370, 411, 192))
        self.StdOutBrowser.setObjectName("textBrowser")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(90, 400, 421, 141))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.BeginScanButton = QtWidgets.QPushButton(self.widget)
        self.BeginScanButton.setObjectName("BeginScanButton")
        self.gridLayout.addWidget(self.BeginScanButton, 0, 0, 1, 1)
        self.SingleScanButton = QtWidgets.QPushButton(self.widget)
        self.SingleScanButton.setObjectName("SingleScanButton")
        self.gridLayout.addWidget(self.SingleScanButton, 0, 1, 1, 1)
        self.StopScanButton = QtWidgets.QPushButton(self.widget)
        self.StopScanButton.setObjectName("StopScanButton")
        self.gridLayout.addWidget(self.StopScanButton, 0, 2, 1, 1)
        self.PlotButton = QtWidgets.QPushButton(self.widget)
        self.PlotButton.setObjectName("PlotButton")
        self.gridLayout.addWidget(self.PlotButton, 1, 0, 1, 1)
        self.CalibrateButton = QtWidgets.QPushButton(self.widget)
        self.CalibrateButton.setObjectName("CalibrateButton")
        self.gridLayout.addWidget(self.CalibrateButton, 1, 1, 1, 1)
        self.KillButton = QtWidgets.QPushButton(self.widget)
        self.KillButton.setObjectName("KillButton")
        self.gridLayout.addWidget(self.KillButton, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1036, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Spectrograph"))
        self.BeginScanButton.setText(_translate("MainWindow", "循环扫描"))
        self.SingleScanButton.setText(_translate("MainWindow", "单次扫描"))
        self.StopScanButton.setText(_translate("MainWindow", "暂停扫描"))
        self.PlotButton.setText(_translate("MainWindow", "画图"))
        self.CalibrateButton.setText(_translate("MainWindow", "校准"))
        self.KillButton.setText(_translate("MainWindow", "关闭程序"))
        
    def printf(self, message):
        # 用于在GUI图形界面中显示输出
        self.StdOutBrowser.append(message)
        self.cursot = self.StdOutBrowser.textCursor()
        self.StdOutBrowser.moveCursor(self.cursot.End)
        QtWidgets.QApplication.processEvents()