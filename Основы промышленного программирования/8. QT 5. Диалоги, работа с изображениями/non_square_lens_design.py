# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'non_square_lens.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEditK = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditK.setObjectName("lineEditK")
        self.horizontalLayout.addWidget(self.lineEditK)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEditN = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditN.setObjectName("lineEditN")
        self.horizontalLayout.addWidget(self.lineEditN)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.lineEditM = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditM.setObjectName("lineEditM")
        self.horizontalLayout.addWidget(self.lineEditM)
        self.btnDraw = QtWidgets.QPushButton(self.centralwidget)
        self.btnDraw.setObjectName("btnDraw")
        self.horizontalLayout.addWidget(self.btnDraw)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.drawCanvas = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.drawCanvas.sizePolicy().hasHeightForWidth())
        self.drawCanvas.setSizePolicy(sizePolicy)
        self.drawCanvas.setObjectName("drawCanvas")
        self.verticalLayout.addWidget(self.drawCanvas)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "???? ??????????????-????????????????"))
        self.label.setText(_translate("MainWindow", "K="))
        self.label_2.setText(_translate("MainWindow", "N="))
        self.label_3.setText(_translate("MainWindow", "M="))
        self.btnDraw.setText(_translate("MainWindow", "????????????????"))
