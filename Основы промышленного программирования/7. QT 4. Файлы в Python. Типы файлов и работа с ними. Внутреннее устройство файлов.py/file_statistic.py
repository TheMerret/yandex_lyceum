import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.btnGetStat = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGetStat.sizePolicy().hasHeightForWidth())
        self.btnGetStat.setSizePolicy(sizePolicy)
        self.btnGetStat.setObjectName("btnGetStat")
        self.gridLayout.addWidget(self.btnGetStat, 0, 2, 1, 1)
        self.lineEditFileName = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditFileName.sizePolicy().hasHeightForWidth())
        self.lineEditFileName.setSizePolicy(sizePolicy)
        self.lineEditFileName.setObjectName("lineEditFileName")
        self.gridLayout.addWidget(self.lineEditFileName, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.doubleSpinBoxMean = QtWidgets.QDoubleSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBoxMean.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxMean.setSizePolicy(sizePolicy)
        self.doubleSpinBoxMean.setMinimum(-16777215.99)
        self.doubleSpinBoxMean.setMaximum(16777215.99)
        self.doubleSpinBoxMean.setObjectName("doubleSpinBoxMean")
        self.gridLayout.addWidget(self.doubleSpinBoxMean, 3, 1, 1, 2)
        self.spinBoxMax = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxMax.sizePolicy().hasHeightForWidth())
        self.spinBoxMax.setSizePolicy(sizePolicy)
        self.spinBoxMax.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.spinBoxMax.setMinimum(-16777215)
        self.spinBoxMax.setMaximum(16777215)
        self.spinBoxMax.setObjectName("spinBoxMax")
        self.gridLayout.addWidget(self.spinBoxMax, 1, 1, 1, 2)
        self.spinBoxMin = QtWidgets.QSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxMin.sizePolicy().hasHeightForWidth())
        self.spinBoxMin.setSizePolicy(sizePolicy)
        self.spinBoxMin.setMinimum(-16777215)
        self.spinBoxMin.setMaximum(16777215)
        self.spinBoxMin.setObjectName("spinBoxMin")
        self.gridLayout.addWidget(self.spinBoxMin, 2, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Файловая статистика"))
        self.label_4.setText(_translate("MainWindow", "Среднее значение:"))
        self.btnGetStat.setText(_translate("MainWindow", "Рассчитать"))
        self.label_2.setText(_translate("MainWindow", "Максимальное значение:"))
        self.label.setText(_translate("MainWindow", "Имя файла"))
        self.label_3.setText(_translate("MainWindow", "Минимальное значение:"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.btnGetStat.clicked.connect(self.get_statistic)

    def get_file_data(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf8') as f:
                data = f.read()
        except FileNotFoundError:
            self.statusbar.showMessage(f'Файл {repr(file_name)} не найден')
            return
        return data

    def set_statistic(self, data):
        try:
            numbers = list(map(int, data.split()))
            if not numbers:
                raise ValueError
        except ValueError:
            return
        maximum = max(numbers)
        minimum = min(numbers)
        mean = sum(numbers) / len(numbers)
        self.spinBoxMax.setValue(maximum)
        self.spinBoxMin.setValue(minimum)
        self.doubleSpinBoxMean.setValue(mean)
        return maximum, minimum, mean

    @staticmethod
    def save_statistic(statistic):
        with open('output.txt', 'w', encoding='utf8') as f:
            statistic = '\n'.join(str(i) for i in statistic)
            f.write(statistic)

    def get_statistic(self):
        file_name = self.lineEditFileName.text()
        data = self.get_file_data(file_name)
        if data is None:
            return
        res = self.set_statistic(data)
        if res is None:
            self.statusbar.showMessage(f'В файле {repr(file_name)} содержаться некорректные данные')
            return
        self.save_statistic(res)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
