# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Cryptobots\backtest_tools\GUI\main.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(375, 273)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.BGroup = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.BGroup.setGeometry(QtCore.QRect(60, 190, 201, 31))
        self.BGroup.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Ok)
        self.BGroup.setObjectName("BGroup")
        self.groupBox1 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox1.setGeometry(QtCore.QRect(10, 10, 341, 151))
        self.groupBox1.setObjectName("groupBox1")
        self.comboBox1 = QtWidgets.QComboBox(self.groupBox1)
        self.comboBox1.setGeometry(QtCore.QRect(10, 90, 291, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.comboBox1.setFont(font)
        self.comboBox1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox1.setAutoFillBackground(False)
        self.comboBox1.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.comboBox1.setObjectName("comboBox1")
        self.comboBox1.addItem("")
        self.comboBox1.addItem("")
        self.comboBox1.addItem("")
        self.label1 = QtWidgets.QLabel(self.groupBox1)
        self.label1.setGeometry(QtCore.QRect(10, 20, 331, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label1.setFont(font)
        self.label1.setMouseTracking(True)
        self.label1.setAutoFillBackground(False)
        self.label1.setInputMethodHints(QtCore.Qt.ImhNone)
        self.label1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label1.setTextFormat(QtCore.Qt.AutoText)
        self.label1.setScaledContents(False)
        self.label1.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label1.setWordWrap(True)
        self.label1.setObjectName("label1")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 375, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox1.setTitle(_translate("MainWindow", "Stratégie"))
        self.comboBox1.setItemText(0, _translate("MainWindow", "Big Will multi"))
        self.comboBox1.setItemText(1, _translate("MainWindow", "Trix simple"))
        self.comboBox1.setItemText(2, _translate("MainWindow", "Trix Multi"))
        self.label1.setText(_translate("MainWindow", "Selectionner la stratégie de trading:"))

