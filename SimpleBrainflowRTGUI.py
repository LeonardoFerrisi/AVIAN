from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowError
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations
import time

class Gui:

    def setupUi(self, MainWindow, application):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(655, 319)

        self.app = application

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.graphicsWindow = pg.GraphicsLayoutWidget(self.centralwidget, show=True, title='Time Series Plot')
        self.graphicsWindow.setBackground('w')
        self.graphicsWindow.setGeometry(QtCore.QRect(10, 20, 621, 151))
        self.graphicsWindow.setObjectName("graphicsWindow")

        self.plots = list()
        self.curves = list()
        p = self.graphicsWindow.addPlot(row=1, col=0)
        p.showAxis('left', False)
        p.setMenuEnabled('left', False)
        p.showAxis('bottom', False)
        p.setMenuEnabled('bottom', False)
        p.setTitle('TimeSeries Plot')
        self.plots.append(p)
        curve = p.plot()
        self.curves.append(curve)

        # some metrics
        self.exg_channels = BoardShim.get_exg_channels(-1)
        self.sampling_rate = BoardShim.get_sampling_rate(-1)
        self.update_speed_ms = 50
        self.window_size = 4
        self.num_points = self.window_size * self.sampling_rate


        # Start the board
        # params = BrainFlowInputParams()
        # self.board_shim = BoardShim(-1, params)
        # self.board_shim.prepare_session()
        # self.board_shim.start_stream(450000, '')

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 200, 221, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(400, 200, 221, 61))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 655, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 220, 71, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(320, 220, 70, 20))
        self.label_2.setObjectName("label_2")

        self.pushButton.clicked.connect(self.startAction)
        self.pushButton_2.clicked.connect(self.stopAction)

        self.retranslateUi(MainWindow)

        self.running = False

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(self.update_speed_ms)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def startAction(self):
        params = BrainFlowInputParams()
        self.board_shim = BoardShim(-1, params)
        self.board_shim.disable_board_logger()
        self.board_shim.prepare_session()
        self.board_shim.start_stream(450000, '')
        self.startTime = time.time()
        self.running = True
        # timer = QtCore.QTimer()
        # timer.timeout.connect(self.update)
        # timer.start(self.update_speed_ms)


    def stopAction(self):
        self.running = False
        self.board_shim.stop_stream()
        self.board_shim.release_session()


    def update(self):
        if self.running == True:
            data = self.board_shim.get_current_board_data(self.num_points)
            for count, channel in enumerate(self.exg_channels):
                if channel == 1:
                    # plot timeseries
                    DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
                    DataFilter.perform_bandpass(data[channel], self.sampling_rate, 51.0, 100.0, 2,
                                                FilterTypes.BUTTERWORTH.value, 0)
                    DataFilter.perform_bandpass(data[channel], self.sampling_rate, 51.0, 100.0, 2,
                                                FilterTypes.BUTTERWORTH.value, 0)
                    DataFilter.perform_bandstop(data[channel], self.sampling_rate, 50.0, 4.0, 2,
                                                FilterTypes.BUTTERWORTH.value, 0)
                    DataFilter.perform_bandstop(data[channel], self.sampling_rate, 60.0, 4.0, 2,
                                                FilterTypes.BUTTERWORTH.value, 0)
                    self.curves[count].setData(data[channel].tolist())
                    time_elapsed = float(time.time()-self.startTime)
                    self.label_2.setText("[" + str(round(time_elapsed,3)) + "]")
                else:
                    pass

            self.app.processEvents()

        else:
            pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Simple Brainflow GUI"))
        self.pushButton.setText(_translate("MainWindow", "start"))
        self.pushButton_2.setText(_translate("MainWindow", "stop"))
        self.label.setText(_translate("MainWindow", "Time Elapsed:"))
        self.label_2.setText(_translate("MainWindow", "[ ]"))


from pyqtgraph import GraphicsWindow

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication([])
    MainWindow = QtWidgets.QMainWindow()
    ui = Gui()
    ui.setupUi(MainWindow, app)
    MainWindow.show()
    QtGui.QApplication.instance().exec_()
    # sys.exit(app.exec_())
