import sys
from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets

car_svg = """<?xml version="1.0" encoding="iso-8859-1"?>
<!-- Generator: Adobe Illustrator 19.0.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="0 0 511.999 511.999" style="enable-background:new 0 0 511.999 511.999;" xml:space="preserve">
<rect x="31.9" y="207.98" style="fill:{c};" width="448.197" height="152.071"/>
<polygon style="fill:#86CBED;" points="408.067,55.912 103.933,55.912 79.922,207.978 432.077,207.978 "/>
<g>
	<rect x="95.931" y="31.9" style="fill:{c};" width="320.145" height="24.01"/>
	<circle style="fill:{c};" cx="480.097" cy="143.949" r="24.01"/>
	<circle style="fill:{c};" cx="31.9" cy="143.949" r="24.01"/>
</g>
<g>
	<rect x="31.9" y="400.063" style="fill:#575756;" width="72.027" height="80.034"/>
	<rect x="408.07" y="400.063" style="fill:#575756;" width="72.027" height="80.034"/>
</g>
<rect x="7.891" y="354.412" style="fill:#CBBBA0;" width="496.215" height="45.651"/>
<rect x="207.98" y="384.061" style="fill:#FFFFFF;" width="96.047" height="48.021"/>
<g>
	<rect x="63.915" y="247.992" style="fill:#F9B233;" width="40.022" height="64.028"/>
	<rect x="408.07" y="247.992" style="fill:#F9B233;" width="40.022" height="64.028"/>
</g>
<g>
	<rect x="103.938" y="247.992" style="fill:#FFFFFF;" width="88.04" height="64.028"/>
	<rect x="320.03" y="247.992" style="fill:#FFFFFF;" width="88.04" height="64.028"/>
</g>
<rect x="143.949" y="344.154" style="fill:#1D1D1B;" width="224.099" height="15.782"/>
<g>
	<rect x="215.987" y="304.132" style="fill:#FFFFFF;" width="80.034" height="15.782"/>
	<rect x="215.987" y="272.117" style="fill:#FFFFFF;" width="80.034" height="15.782"/>
	<rect x="215.987" y="240.101" style="fill:#FFFFFF;" width="80.034" height="15.782"/>
</g>
<g>
	<rect x="95.931" y="24.01" style="fill:#1D1D1B;" width="320.145" height="15.782"/>
	<path style="fill:#1D1D1B;" d="M391.947,191.971h-15.782c0-17.715-14.412-32.127-32.127-32.127s-32.127,14.412-32.127,32.127
		H296.13c0-26.417,21.491-47.909,47.909-47.909S391.947,165.554,391.947,191.971z"/>
	<path style="fill:#1D1D1B;" d="M15.782,359.933h96.155v-15.782H0v63.803h24.01v80.035h87.813v-80.035h80.148v-15.782H15.782
		V359.933z M96.043,472.207H39.792v-64.253h56.25v64.253H96.043z"/>
	<path style="fill:#1D1D1B;" d="M400.063,359.933h96.155v32.24H320.027v15.782h80.148v80.035h87.813v-80.035h24.01v-63.803H400.063
		V359.933z M472.207,472.207h-56.25v-64.253h56.25V472.207z"/>
	<path style="fill:#1D1D1B;" d="M56.025,319.915h143.838v-79.81H56.025V319.915z M184.081,304.133h-72.258v-48.246h72.258V304.133z
		 M71.806,255.887h24.236v48.246H71.806V255.887z"/>
	<path style="fill:#1D1D1B;" d="M455.975,240.105H312.137v79.81h143.838v-79.81H455.975z M327.918,255.887h72.258v48.246h-72.258
		L327.918,255.887L327.918,255.887z M440.194,304.133h-24.236v-48.246h24.236V304.133z"/>
	<path style="fill:#1D1D1B;" d="M31.901,175.852c9.352,0,17.776-4.045,23.617-10.478l13.018,34.714H24.01v135.947h15.782V215.869
		h432.416v120.165h15.782V200.087h-44.526l13.018-34.714c5.84,6.433,14.266,10.478,23.617,10.478
		c17.59,0,31.901-14.311,31.901-31.901s-14.309-31.901-31.9-31.901c-13.346,0-24.798,8.241-29.551,19.901l-0.004-0.004l-0.045,0.128
		c-0.35,0.871-0.667,1.759-0.941,2.666l-14.547,41.222l-20.2-127.94H97.19L76.989,175.966l-14.527-41.155
		c-0.291-0.972-0.629-1.924-1.008-2.856l-0.003-0.009l0,0c-4.753-11.655-16.205-19.895-29.549-19.895
		C14.311,112.049,0,126.36,0,143.95S14.311,175.852,31.901,175.852z M480.098,127.831c8.888,0,16.119,7.231,16.119,16.119
		c0,8.888-7.231,16.119-16.119,16.119c-8.888,0-16.119-7.23-16.119-16.119C463.979,135.061,471.21,127.831,480.098,127.831z
		 M110.675,63.803h137.433v16.233h-16.119v15.782h48.021V80.036h-16.119V63.803h137.433l21.519,136.286H89.157L110.675,63.803z
		 M31.901,127.831c8.888,0,16.119,7.231,16.119,16.119c0,8.888-7.231,16.119-16.119,16.119s-16.119-7.23-16.119-16.119
		C15.782,135.061,23.013,127.831,31.901,127.831z"/>
</g>
<g>
	
		<rect x="138.063" y="100.474" transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 160.1062 318.1972)" style="fill:#FFFFFF;" width="15.781" height="50.932"/>
	
		<rect x="164.073" y="89.023" transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 194.5969 360.5152)" style="fill:#FFFFFF;" width="15.781" height="101.864"/>
	
		<rect x="184.078" y="148.637" transform="matrix(-0.7071 -0.7071 0.7071 -0.7071 214.6056 408.8033)" style="fill:#FFFFFF;" width="15.781" height="22.637"/>
</g>
<g>
	<rect x="120.056" y="336.032" style="fill:#1D1D1B;" width="15.782" height="32.015"/>
	<rect x="376.17" y="336.032" style="fill:#1D1D1B;" width="15.782" height="32.015"/>
	<path style="fill:#1D1D1B;" d="M311.911,439.968H200.087v-63.803h111.824V439.968z M215.869,424.186h80.261v-32.24h-80.261
		L215.869,424.186L215.869,424.186z"/>
	<rect x="223.983" y="400.179" style="fill:#1D1D1B;" width="16.007" height="15.782"/>
	<rect x="247.992" y="400.179" style="fill:#1D1D1B;" width="16.007" height="15.782"/>
	<rect x="272.011" y="400.179" style="fill:#1D1D1B;" width="16.007" height="15.782"/>
</g>
<g>
</g>
<g>
</g>
<g>
</g>
<g>
</g>
<g>
</g>
<g>
</g>
<g>
</g>
<g>
</g>
<g>
</g>
<g>
</g>
<g>
</g>
<g>
</g>
<g>
</g>
<g>
</g>
<g>
</g>
</svg>"""


def get_im_by_color(hex_color):
    car_svg_new = car_svg.format(c=hex_color)
    car_im = QtGui.QImage.fromData(bytearray(car_svg_new, encoding='utf-8'))
    car_im = car_im.smoothScaled(64, 64)
    return car_im


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
        MainWindow.setWindowTitle(_translate("MainWindow", "Машинка"))


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.car_im = get_im_by_color(QtGui.QColor(255, 0, 0).name())
        self.setupUi(self)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.centralWidget().setMouseTracking(True)
        self.centralWidget().mouseMoveEvent = self.mouseMoveEvent
        self.im_label = QtWidgets.QLabel(self)
        self.update_im_color(QtGui.QColor(255, 0, 0))

    def update_im_color(self, color: QtGui.QColor):
        self.car_im = get_im_by_color(color.name())
        self.im_label.setPixmap(QtGui.QPixmap(self.car_im))
        self.im_label.resize(self.car_im.width(), self.car_im.height())

    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        x, y = (min(x, self.width() - self.im_label.width()),
                min(y, self.height() - self.im_label.height()))
        self.im_label.move(x, y)
        super().mouseMoveEvent(event)

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key_Space:
            color = QtGui.QColor(*(randint(0, 255) for _ in range(3)))
            self.update_im_color(color)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
