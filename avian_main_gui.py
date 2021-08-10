from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowError
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations
import time


class AVIAN_MainWindow(object):

    def setupUi(self, AVIAN_GUI, application):

        AVIAN_GUI.setObjectName("AVIAN_GUI")
        AVIAN_GUI.resize(1650, 920)
        AVIAN_GUI.setWindowIcon(QtGui.QIcon('icon.png'))

        self.app = application

        self.centralwidget = QtWidgets.QWidget(AVIAN_GUI)
        self.centralwidget.setObjectName("centralwidget")


        # Time Series
        self.TimeSeries = pg.GraphicsLayoutWidget(self.centralwidget)
        self.TimeSeries.setBackground('w')
        self.TimeSeries.setGeometry(QtCore.QRect(9, 9, 611, 851))
        self.TimeSeries.setObjectName("TimeSeries")

        # init board
        self._init_board()

        # init time series
        self._init_pens()
        self._init_time_series()


        self.BandPowers = PlotWidget(self.centralwidget)
        self.BandPowers.setGeometry(QtCore.QRect(1090, 10, 551, 511))
        self.BandPowers.setObjectName("BandPowers")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(640, 140, 75, 23))
        self.start_button.setObjectName("start_button")
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setGeometry(QtCore.QRect(720, 140, 75, 23))
        self.stop_button.setObjectName("stop_button")
        self.StateSelect = QtWidgets.QComboBox(self.centralwidget)
        self.StateSelect.setGeometry(QtCore.QRect(640, 190, 301, 21))
        self.StateSelect.setObjectName("StateSelect")
        self.StateSelect.addItem("")
        self.StateSelect.addItem("")
        self.StateSelect.addItem("")
        self.StateSelect.addItem("")
        self.StateSelect.addItem("")
        self.star_one = QtWidgets.QLabel(self.centralwidget)
        self.star_one.setGeometry(QtCore.QRect(630, 10, 241, 16))
        self.star_one.setObjectName("star_one")
        self.star_two = QtWidgets.QLabel(self.centralwidget)
        self.star_two.setGeometry(QtCore.QRect(910, 10, 171, 20))
        self.star_two.setObjectName("star_two")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(940, 40, 121, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.selectmetric = QtWidgets.QLabel(self.centralwidget)
        self.selectmetric.setGeometry(QtCore.QRect(640, 170, 181, 16))
        self.selectmetric.setObjectName("selectmetric")
        self.IS_CONNECTED = QtWidgets.QLabel(self.centralwidget)
        self.IS_CONNECTED.setGeometry(QtCore.QRect(930, 100, 121, 20))
        self.IS_CONNECTED.setObjectName("IS_CONNECTED")
        self.connect_button = QtWidgets.QPushButton(self.centralwidget)
        self.connect_button.setGeometry(QtCore.QRect(910, 70, 75, 23))
        self.connect_button.setObjectName("connect_button")
        self.disconnect_button = QtWidgets.QPushButton(self.centralwidget)
        self.disconnect_button.setGeometry(QtCore.QRect(990, 70, 75, 23))
        self.disconnect_button.setObjectName("disconnect_button")
        self.playaudio_true_button = QtWidgets.QRadioButton(self.centralwidget)
        self.playaudio_true_button.setGeometry(QtCore.QRect(820, 270, 51, 17))
        self.playaudio_true_button.setObjectName("playaudio_true_button")
        self.playaudio_false_button = QtWidgets.QRadioButton(self.centralwidget)
        self.playaudio_false_button.setGeometry(QtCore.QRect(880, 270, 51, 17))
        self.playaudio_false_button.setObjectName("playaudio_false_button")
        self.playaud_label = QtWidgets.QLabel(self.centralwidget)
        self.playaud_label.setGeometry(QtCore.QRect(640, 270, 151, 16))
        self.playaud_label.setObjectName("playaud_label")
        self.confidence = QtWidgets.QProgressBar(self.centralwidget)
        self.confidence.setGeometry(QtCore.QRect(640, 230, 331, 23))
        self.confidence.setProperty("value", 0)
        self.confidence.setObjectName("confidence")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(700, 300, 41, 91))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setOrientation(QtCore.Qt.Vertical)
        self.progressBar.setObjectName("progressBar")
        self.progressBar_2 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_2.setGeometry(QtCore.QRect(750, 300, 41, 91))
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_2.setObjectName("progressBar_2")
        self.progressBar_3 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_3.setGeometry(QtCore.QRect(800, 300, 41, 91))
        self.progressBar_3.setProperty("value", 0)
        self.progressBar_3.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_3.setObjectName("progressBar_3")
        self.progressBar_4 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_4.setGeometry(QtCore.QRect(850, 300, 41, 91))
        self.progressBar_4.setProperty("value", 0)
        self.progressBar_4.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_4.setObjectName("progressBar_4")
        self.progressBar_5 = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_5.setGeometry(QtCore.QRect(900, 300, 41, 91))
        self.progressBar_5.setProperty("value", 0)
        self.progressBar_5.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_5.setObjectName("progressBar_5")
        self.channels_label = QtWidgets.QLabel(self.centralwidget)
        self.channels_label.setGeometry(QtCore.QRect(640, 300, 51, 21))
        self.channels_label.setObjectName("channels_label")
        self.chan_1 = QtWidgets.QLabel(self.centralwidget)
        self.chan_1.setGeometry(QtCore.QRect(710, 400, 16, 16))
        self.chan_1.setObjectName("chan_1")
        self.chan_2 = QtWidgets.QLabel(self.centralwidget)
        self.chan_2.setGeometry(QtCore.QRect(760, 400, 16, 16))
        self.chan_2.setObjectName("chan_2")
        self.chan_3 = QtWidgets.QLabel(self.centralwidget)
        self.chan_3.setGeometry(QtCore.QRect(810, 400, 16, 16))
        self.chan_3.setObjectName("chan_3")
        self.chan_4 = QtWidgets.QLabel(self.centralwidget)
        self.chan_4.setGeometry(QtCore.QRect(860, 400, 16, 16))
        self.chan_4.setObjectName("chan_4")
        self.chan_5 = QtWidgets.QLabel(self.centralwidget)
        self.chan_5.setGeometry(QtCore.QRect(910, 400, 16, 16))
        self.chan_5.setObjectName("chan_5")
        self.FFT_plot = PlotWidget(self.centralwidget)
        self.FFT_plot.setGeometry(QtCore.QRect(1180, 530, 461, 341))
        self.FFT_plot.setObjectName("FFT_plot")
        self.indicator = QtWidgets.QWidget(self.centralwidget)
        self.indicator.setGeometry(QtCore.QRect(640, 40, 231, 80))
        self.indicator.setObjectName("indicator")

        self.pic = QtWidgets.QLabel(self.centralwidget)
        self.pic.setGeometry(QtCore.QRect(690, 560, 321, 291))
        self.pic.setPixmap(QtGui.QPixmap("AVIAN.png"))
        self.pic.show()
        # self.imagePlaceHolder = QtWidgets.QWidget(self.centralwidget)
        # self.imagePlaceHolder.setGeometry(QtCore.QRect(690, 560, 321, 291))
        # self.imagePlaceHolder.setObjectName("imagePlaceHolder")



        AVIAN_GUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AVIAN_GUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1650, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        AVIAN_GUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AVIAN_GUI)
        self.statusbar.setObjectName("statusbar")
        AVIAN_GUI.setStatusBar(self.statusbar)
        self.actionSave_as_CSV = QtWidgets.QAction(AVIAN_GUI)
        self.actionSave_as_CSV.setObjectName("actionSave_as_CSV")
        self.actionGithub = QtWidgets.QAction(AVIAN_GUI)
        self.actionGithub.setObjectName("actionGithub")
        self.actionDocumentation = QtWidgets.QAction(AVIAN_GUI)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.menuFile.addAction(self.actionSave_as_CSV)
        self.menuHelp.addAction(self.actionGithub)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # connect buttons
        self.start_button.clicked.connect(self.startAction)
        self.stop_button.clicked.connect(self.stopAction)


        self.retranslateUi(AVIAN_GUI)

        self.running = False

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(self.update_speed_ms)

        QtCore.QMetaObject.connectSlotsByName(AVIAN_GUI)


    def startAction(self):
        self.board_shim.prepare_session()
        self.IS_CONNECTED.setText("[ Is connected: True ]")
        self.board_shim.start_stream(450000, '')
        self.running = True

    def stopAction(self):
        self.board_shim.stop_stream()
        self.board_shim.release_session()
        self.IS_CONNECTED.setText("[ Is connected: False ]")
        self.running = False


    def _init_pens(self):
        self.pens = list()
        self.brushes = list()
        colors = ['#A54E4E', '#A473B6', '#5B45A4', '#2079D2', '#32B798', '#2FA537', '#9DA52F', '#A57E2F', '#A53B2F']
        for i in range(len(colors)):
            pen = pg.mkPen({'color': colors[i], 'width': 1})
            self.pens.append(pen)
            brush = pg.mkBrush(colors[i])
            self.brushes.append(brush)

    def _init_board(self):
        params = BrainFlowInputParams()
        self.board_id = -1
        self.exg_channels = BoardShim.get_exg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.update_speed_ms = 50
        self.window_size = 4
        self.num_points = self.window_size * self.sampling_rate
        self.board_shim = BoardShim(self.board_id, params)


    def _init_time_series(self):
        self.plots = list()
        self.curves = list()
        for i in range(len(self.exg_channels)):
            p = self.TimeSeries.addPlot(row=i, col=0)
            p.showAxis('left', False)
            p.setMenuEnabled('left', False)
            p.showAxis('bottom', False)
            p.setMenuEnabled('bottom', False)
            if i == 0:
                p.setTitle('TimeSeries Plot')
            self.plots.append(p)
            curve = p.plot(pen=self.pens[i % len(self.pens)])
            # curve.setDownsampling(auto=True, method='mean', ds=3)
            self.curves.append(curve)

    def update(self):
        if self.running:
            data = self.board_shim.get_current_board_data(self.num_points)
            for count, channel in enumerate(self.exg_channels):
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
                # time_elapsed = float(time.time()-self.startTime)
                # self.label_2.setText("[" + str(round(time_elapsed,3)) + "]")
            self.app.processEvents()
            self.statusbar.showMessage("Current data buffer size: " + str(data.size))
        else:
            pass

    def retranslateUi(self, AVIAN_GUI):
        _translate = QtCore.QCoreApplication.translate
        AVIAN_GUI.setWindowTitle(_translate("AVIAN_GUI", "AVIAN version 0.7 [Prototype]"))
        self.start_button.setText(_translate("AVIAN_GUI", "Start"))
        self.stop_button.setText(_translate("AVIAN_GUI", "Stop"))
        self.StateSelect.setItemText(0, _translate("AVIAN_GUI", "Concentration"))
        self.StateSelect.setItemText(1, _translate("AVIAN_GUI", "Relaxation"))
        self.StateSelect.setItemText(2, _translate("AVIAN_GUI", "Theta/Beta"))
        self.StateSelect.setItemText(3, _translate("AVIAN_GUI", "Alpha Threshold"))
        self.StateSelect.setItemText(4, _translate("AVIAN_GUI", "Beta Threshold"))
        self.star_one.setText(_translate("AVIAN_GUI", "* Make Sure Board is connected before Starting!"))
        self.star_two.setText(_translate("AVIAN_GUI", "** Select the board type below"))
        self.comboBox.setItemText(0, _translate("AVIAN_GUI", "Synthetic"))
        self.comboBox.setItemText(1, _translate("AVIAN_GUI", "OpenBCI [Cyton]"))
        self.comboBox.setItemText(2, _translate("AVIAN_GUI", "Muse (2016) [Requires BLED112]"))
        self.comboBox.setItemText(3, _translate("AVIAN_GUI", "Muse2 [Requires BLED112]"))
        self.selectmetric.setText(_translate("AVIAN_GUI", "Select Metric to estimate:"))

        self.IS_CONNECTED.setText(_translate("AVIAN_GUI", "[ Is connected: False ]"))

        self.connect_button.setText(_translate("AVIAN_GUI", "Connect"))
        self.disconnect_button.setText(_translate("AVIAN_GUI", "Disconnect"))
        self.playaudio_true_button.setText(_translate("AVIAN_GUI", "True"))
        self.playaudio_false_button.setText(_translate("AVIAN_GUI", "False"))
        self.playaud_label.setText(_translate("AVIAN_GUI", "Play Audio on Threshold Pass"))
        self.channels_label.setText(_translate("AVIAN_GUI", "Channels:"))
        self.chan_1.setText(_translate("AVIAN_GUI", "[1]"))
        self.chan_2.setText(_translate("AVIAN_GUI", "[2]"))
        self.chan_3.setText(_translate("AVIAN_GUI", "[3]"))
        self.chan_4.setText(_translate("AVIAN_GUI", "[4]"))
        self.chan_5.setText(_translate("AVIAN_GUI", "[5]"))
        self.menuFile.setTitle(_translate("AVIAN_GUI", "File"))
        self.menuHelp.setTitle(_translate("AVIAN_GUI", "Help"))
        self.actionSave_as_CSV.setText(_translate("AVIAN_GUI", "Save as CSV"))
        self.actionGithub.setText(_translate("AVIAN_GUI", "Github"))
        self.actionDocumentation.setText(_translate("AVIAN_GUI", "Documentation"))
from pyqtgraph import GraphicsLayoutWidget, PlotWidget


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication([])
    AVIAN_GUI = QtWidgets.QMainWindow()
    ui = AVIAN_MainWindow()
    ui.setupUi(AVIAN_GUI, app)
    AVIAN_GUI.show()
    QtGui.QApplication.instance().exec_()
