import sys
from PyQt5 import QtCore, QtGui, QtWidgets


ufo_svg = """<?xml version="1.0" encoding="iso-8859-1"?>
<!-- Generator: Adobe Illustrator 19.0.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="0 0 280.058 280.058" style="enable-background:new 0 0 280.058 280.058;" xml:space="preserve">
<g>
	<path style="fill:#324D5B;" d="M140.027,214.41c-14.491,0-26.253,11.761-26.253,26.253s11.761,26.253,26.253,26.253
		c14.491,0,26.253-11.761,26.253-26.253S154.518,214.41,140.027,214.41z M210.034,196.91c-14.491,0-26.253,11.752-26.253,26.253
		s11.761,26.253,26.253,26.253c14.491,0,26.253-11.752,26.253-26.253S224.525,196.91,210.034,196.91z M70.02,196.91
		c-14.491,0-26.253,11.752-26.253,26.253s11.761,26.253,26.253,26.253s26.253-11.752,26.253-26.253S84.511,196.91,70.02,196.91z"/>
	<path style="fill:#F4B459;" d="M59.536,129.859c44.376-27.346,116.325-27.346,160.709,0s44.376,71.678,0,99.025
		s-116.334,27.346-160.709,0S15.152,157.206,59.536,129.859z"/>
	<path style="fill:#324D5B;" d="M41.02,81.222c54.675-32.466,143.339-32.466,198.032,0c54.675,32.466,54.675,85.102,0,117.568
		c-54.693,32.474-143.356,32.474-198.032,0C-13.673,166.324-13.673,113.688,41.02,81.222z"/>
	<path style="fill:#E4E7E7;" d="M140.027,13.142c48.331,0,87.509,39.178,87.509,87.509s-39.178,70.007-87.509,70.007
		s-87.509-21.676-87.509-70.007S91.696,13.142,140.027,13.142z"/>
	<path style="fill:#3DB39E;" d="M189.898,160.768c1.698-5.154,2.634-10.659,2.634-16.364v-43.755
		c0-28.992-23.505-52.505-52.505-52.505c-28.992,0-52.505,23.505-52.505,52.505v43.754c0,5.706,0.945,11.21,2.634,16.364
		c14.15,6.668,31.319,9.888,49.871,9.888C158.57,170.656,175.739,167.436,189.898,160.768z"/>
	<path style="fill:#FFFFFF;" d="M140.027,83.147c14.491,0,26.253,11.752,26.253,26.253c0,14.509-11.761,26.261-26.253,26.261
		c-14.491,0-26.253-11.752-26.253-26.261C113.774,94.9,125.535,83.147,140.027,83.147z"/>
	<path style="fill:#324D5B;" d="M140.027,100.649c4.839,0,8.751,3.92,8.751,8.751c0,4.839-3.912,8.751-8.751,8.751
		s-8.751-3.912-8.751-8.751C131.276,104.57,135.188,100.649,140.027,100.649z"/>
</g>
</svg>
"""
ufo_im = QtGui.QImage.fromData(bytearray(ufo_svg, encoding='utf-8'))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Управление НЛО"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.step = 10
        self.keys = []
        self.setupUi(self)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(ufo_im)))
        self.ufo = QtWidgets.QLabel(self)
        self.ufo.resize(64, 64)
        ufo_pixmap = QtGui.QPixmap(ufo_im)
        ufo_pixmap = ufo_pixmap.scaled(self.ufo.width(), self.ufo.height(),
                                       QtCore.Qt.KeepAspectRatio)
        self.ufo.setPixmap(ufo_pixmap)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        key = a0.key()
        self.keys.append(key)

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        for key in self.keys:
            if key == QtCore.Qt.Key_Up:
                self.ufo.move(self.ufo.x(), self.ufo.y() - self.step)
            elif key == QtCore.Qt.Key_Right:
                self.ufo.move(self.ufo.x() + self.step, self.ufo.y())
            elif key == QtCore.Qt.Key_Down:
                self.ufo.move(self.ufo.x(), self.ufo.y() + self.step)
            elif key == QtCore.Qt.Key_Left:
                self.ufo.move(self.ufo.x() - self.step, self.ufo.y())
        self.keys.remove(a0.key())
        if self.ufo.x() > self.width():
            self.ufo.move(-self.ufo.width(), self.ufo.y())
        elif self.ufo.x() + self.ufo.width() < 0:
            self.ufo.move(self.width(), self.ufo.y())
        if self.ufo.y() > self.height():
            self.ufo.move(self.ufo.x(), -self.ufo.height())
        elif self.ufo.y() + self.ufo.height() < 0:
            self.ufo.move(self.ufo.x(), self.height())


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
