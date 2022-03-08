from pyqtgraph import GraphicsLayoutWidget, PlotWidget
import multiprocessing

from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowError
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations
from board_communicator import Comms
from sound import audioFeedback
import scr
import time
import webbrowser


class AVIAN_MainWindow(object):

    def setupUi(self, AVIAN_GUI, application):

        self.enableTestSignalConverter = False

        self.update_speed_ms = 50
        self.window_size = 4

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

        # # init time series
        # self._init_pens()
        # self._init_time_series()

        self.BandPowers = pg.GraphicsLayoutWidget(self.centralwidget)
        self.BandPowers.setBackground('w')
        self.BandPowers.setGeometry(QtCore.QRect(1090, 10, 551, 511))
        self.BandPowers.setObjectName("BandPowers")

        # self._init_band_powers()

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
        self.boardSelect = QtWidgets.QComboBox(self.centralwidget)
        self.boardSelect.setGeometry(QtCore.QRect(940, 40, 121, 22))
        self.boardSelect.setObjectName("comboBox")
        self.boardSelect.addItem("")
        self.boardSelect.addItem("")
        self.boardSelect.addItem("")
        self.boardSelect.addItem("")
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
        # self.playaudio_true_button.toggled.connect(self.audioOnAction)
        self.playaudio_true_button.clicked.connect(self.audioOnAction)

        self.playaudio_false_button = QtWidgets.QRadioButton(
            self.centralwidget)
        self.playaudio_false_button.setGeometry(QtCore.QRect(880, 270, 51, 17))
        self.playaudio_false_button.setObjectName("playaudio_false_button")
        # self.playaudio_false_button.toggled.connect(self.audioOffAction)
        self.playaudio_false_button.clicked.connect(self.audioOffAction)
        self.playaudio_false_button.setChecked(True)

        self.playaud_label = QtWidgets.QLabel(self.centralwidget)
        self.playaud_label.setGeometry(QtCore.QRect(640, 270, 151, 16))
        self.playaud_label.setObjectName("playaud_label")

        self.confidence = QtWidgets.QProgressBar(self.centralwidget)
        self.confidence.setGeometry(QtCore.QRect(640, 230, 331, 23))
        self.confidence.setProperty("value", 0)
        self.confidence.setObjectName("confidence")

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
        self.FFT_plot.setGeometry(QtCore.QRect(1180, 600, 450, 270))
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

        self._init_value_labels()

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

        self.connect_button.clicked.connect(self.connectAction)
        self.disconnect_button.clicked.connect(self.disconnectAction)

        self.actionSave_as_CSV.triggered.connect(self.saveToCSV)
        self.actionGithub.triggered.connect(self.sendToGithub)
        self.actionDocumentation.triggered.connect(self.sendToDocumentation)

        self.retranslateUi(AVIAN_GUI)

        self.running = False
        self.serialPort = ''
        self.connected = False

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(self.update_speed_ms)

        QtCore.QMetaObject.connectSlotsByName(AVIAN_GUI)

    def _init_value_labels(self):
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(
            QtCore.QRect(1180, 530, 461, 21))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.band_label_holder = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget)
        self.band_label_holder.setContentsMargins(0, 0, 0, 0)
        self.band_label_holder.setObjectName("band_label_holder")

        self.gamma_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.gamma_label.setObjectName("gamma_label")
        self.band_label_holder.addWidget(self.gamma_label)
        self.delta_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.delta_label.setObjectName("delta_label")
        self.band_label_holder.addWidget(self.delta_label)
        self.theta_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.theta_label.setObjectName("theta_label")
        self.band_label_holder.addWidget(self.theta_label)
        self.beta_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.beta_label.setObjectName("beta_label")
        self.band_label_holder.addWidget(self.beta_label)
        self.alpha_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.alpha_label.setObjectName("alpha_label")
        self.band_label_holder.addWidget(self.alpha_label)

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(
            QtCore.QRect(1180, 560, 461, 21))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.value_holder = QtWidgets.QHBoxLayout(
            self.horizontalLayoutWidget_2)
        self.value_holder.setContentsMargins(0, 0, 0, 0)
        self.value_holder.setObjectName("value_holder")

        self.gamma_value = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.gamma_value.setObjectName("gamma_value")
        self.value_holder.addWidget(self.gamma_value)
        self.delta_value = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.delta_value.setObjectName("delta_value")
        self.value_holder.addWidget(self.delta_value)
        self.theta_value = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.theta_value.setObjectName("theta_value")
        self.value_holder.addWidget(self.theta_value)
        self.beta_value = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.beta_value.setObjectName("beta_value")
        self.value_holder.addWidget(self.beta_value)
        self.alpha_value = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.alpha_value.setObjectName("alpha_value")
        self.value_holder.addWidget(self.alpha_value)

        self.audioOn = False  # Audio is default set to false

    def disconnectAction(self):
        if self.connected:
            self.board_shim.release_session()
            self.IS_CONNECTED.setText("[ Is connected: False ]")

    def connectAction(self):
        if not self.connected:
            # init board
            self.checkBoardSelect()
            self._init_board(boardID=self.board_id,
                             serialPort=self.serialPort)  # INIT BOARD
            self.connected = True
            self.statusbar.showMessage("CONNECTED")
            self.IS_CONNECTED.setText("[ Is connected: True ]")
            self.exg_channels = BoardShim.get_exg_channels(self.board_id)
            # init time series
            self._init_pens()
            self._init_time_series()
            self._init_band_powers()

    def _init_board(self, boardID: int = -1, serialPort: str = ''):
        # Serial is default to nothing
        self.myBoard = Comms(boardID=boardID, serial=serialPort)
        self.board_shim = self.myBoard.board
        # params = BrainFlowInputParams()
        self.board_id = boardID
        self.exg_channels = BoardShim.get_exg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.update_speed_ms = 50
        self.window_size = 4
        self.num_points = self.window_size * self.sampling_rate
        # self.board_shim = BoardShim(self.board_id, params)

        self.psd_size = DataFilter.get_nearest_power_of_two(self.sampling_rate)

    def checkBoardSelect(self):
        if self.boardSelect.currentText() == "Synthetic":
            self.board_id = -1
        elif self.boardSelect.currentText() == "OpenBCI [Cyton]":
            self.board_id = 0
            self.serialPort = 'COM3'
        elif self.boardSelect.currentText() == "Muse (2016) [Requires BLED112]" or self.boardSelect.currentText() == "Muse2 [Requires BLED112]":
            self.board_id = 22
            self.serialPort = 'COM3'
        else:
            self.board_id = -1

    def startAction(self):
        """
        Starts the board and sets running to true
        """
        if self.connected:
            self.board_shim.prepare_session()
            self.IS_CONNECTED.setText("[ Is connected: True ]")
            self.timeStart = time.time()
            self.board_shim.start_stream(450000, '')
            self.running = True

            if self.enableTestSignalConverter:
                self.mySCR = scr.SignalConverter(newBoardData=self.board_shim.get_current_board_data(self.num_points),
                                                 numEXG=self.myBoard.getEXGChannels(),
                                                 samplingRate=self.myBoard.get_samplingRate())

            if self.audioOn:
                # self.musicMaker.brainAnalyzer()
                self.__init_music_maker()
                self.musicMaker.brainAnalyzer()
                # self.runThread1 = Thread(target=self.musicMaker.musicMaker)
                # self.runThread1.start()
                # print("RUNNING MM")
                # self.runThread2 = Thread(target=self.StateProgressListener)
                # self.runThread2.start()

        # def StateProgressListener(self):
        #     try:
        #         myConfidence = self.musicMaker.prediction
        #         print("FUNCTIONING")
        #     except:
        #         print("NOT")
        else:
            self.statusbar.showMessage(
                "PLEASE CONNECT THE BOARD BEFORE YOU START")

    def modStateProgressBar(self, newValue):
        self.confidence.setProperty("value", float(round(newValue, 3)))

    def stopAction(self):
        self.statusbar.showMessage("stopping session...")
        self.dataOut = self.board_shim.get_board_data()
        self.board_shim.stop_stream()
        self.board_shim.release_session()
        self.statusbar.showMessage("session released")
        self.IS_CONNECTED.setText("[ Is connected: False ]")
        self.running = False
        self.timeElapsed = time.time() - self.timeStart
        self.statusbar.showMessage(
            "Time elapsed since start: " + str(round(self.timeElapsed, 4)) + " seconds")
        if self.audioOn:
            self.musicMaker.kill()

    def _init_pens(self):
        self.pens = list()
        self.brushes = list()
        colors = ['#A54E4E', '#A473B6', '#5B45A4', '#2079D2',
                  '#32B798', '#2FA537', '#9DA52F', '#A57E2F', '#A53B2F']
        for i in range(len(colors)):
            pen = pg.mkPen({'color': colors[i], 'width': 1})
            self.pens.append(pen)
            brush = pg.mkBrush(colors[i])
            self.brushes.append(brush)

    def __init_music_maker(self):
        """
        Initiates the music maker,
        relies on the signal converter relay, board communicator and NOMI in music maker
        :return:
        """
        # self.checkStateSelect()
        # self.musicMaker = musicMaker(self.board_shim)
        if self.StateSelect.currentText() == "Concentration":
            self.brainVal = 1
        elif self.StateSelect.currentText() == "Releaxation":
            self.brainVal = 0
        elif self.StateSelect.currentText() == "Theta/Beta":
            self.brainVal = 2
        else:
            self.brainVal = 0

        self.musicMaker = audioFeedback(
            self.myBoard, brainStateVal=self.brainVal)
        # self.musicMaker.start()
        self.musicMaker.loadWav()
        self.ourPrediction = self.musicMaker.prediction

    def runConcentration(self):
        """
        Set the brainstate to concentration
        """
        self.musicMaker.brainStateVal = 1

    def runRelaxation(self):
        """
        Set the brainstate to relaxation
        """
        self.musicMaker.brainStateVal = 0

    def _init_band_powers(self):
        """
        Initialize band power plot
        """
        self.band_plot = self.BandPowers.addPlot(row=len(self.exg_channels) // 2, col=1,
                                                 rowspan=len(self.exg_channels) // 2)
        self.band_plot.showAxis('left', True)
        self.band_plot.setMenuEnabled('left', False)
        self.band_plot.showAxis('bottom', True)
        self.band_plot.setMenuEnabled('bottom', False)
        self.band_plot.setTitle('BandPower Plot')
        y = [0, 0, 0, 0, 0]
        x = [1, 2, 3, 4, 5]
        self.band_bar = pg.BarGraphItem(
            x=x, height=y, width=0.8, pen=self.pens[0], brush=self.brushes[0])
        self.band_plot.addItem(self.band_bar)

    def _init_time_series(self):
        """
        Initialize time series plot
        """
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

            avg_bands = [0, 0, 0, 0, 0]
            for count, channel in enumerate(self.exg_channels):
                # plot timeseries
                DataFilter.detrend(
                    data[channel], DetrendOperations.CONSTANT.value)
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

                # BAND POWER PROCESSING
                if data.shape[1] > DataFilter.get_nearest_power_of_two(self.sampling_rate):
                    psd_data = DataFilter.get_psd_welch(data[channel], self.psd_size, self.psd_size // 2,
                                                        self.sampling_rate,
                                                        WindowFunctions.BLACKMAN_HARRIS.value)

                    avg_bands[0] = avg_bands[0] + \
                        DataFilter.get_band_power(psd_data, 1.0, 4.0)  # Delta
                    avg_bands[1] = avg_bands[1] + \
                        DataFilter.get_band_power(psd_data, 4.0, 7.0)  # Theta
                    avg_bands[2] = avg_bands[2] + \
                        DataFilter.get_band_power(psd_data, 7.0, 13.0)  # Alpha
                    avg_bands[3] = avg_bands[3] + \
                        DataFilter.get_band_power(psd_data, 13.0, 30.0)  # Beta
                    avg_bands[4] = avg_bands[4] + \
                        DataFilter.get_band_power(
                            psd_data, 30.0, 50.0)  # Gamma

                    self.alpha_value.setText(
                        "[" + str(round(avg_bands[2], 3)) + "]")
                    self.beta_value.setText(
                        "[" + str(round(avg_bands[3], 3)) + "]")
                    self.theta_value.setText(
                        "[" + str(round(avg_bands[1], 3)) + "]")
                    self.delta_value.setText(
                        "[" + str(round(avg_bands[0], 3)) + "]")
                    self.gamma_value.setText(
                        "[" + str(round(avg_bands[4], 3)) + "]")

            avg_bands = [int(x * 100 / len(self.exg_channels))
                         for x in avg_bands]

            # if self.brainVal == 2:

            if self.enableTestSignalConverter:
                self.mySCR.updateSCRData(data)

            self.band_bar.setOpts(height=avg_bands)
            self.app.processEvents()
            # if self.audioOn:
            #     print("AUDIO ON")
            #     self.musicMaker.musicMaker()
            # if self.audioOn:
            #     self.runMusicMaker()

            try:
                if self.enableTestSignalConverter:
                    self.mySCR.getPrediction()
                    print(self.mySCR.predictionOut)

                self.confidence.setProperty("value", float(
                    self.musicMaker.predictionOut) * 100)
            except:
                pass

            self.statusbar.showMessage(
                "Current data buffer size: " + str(data.size))
        else:
            pass

    ######################################
    def saveToCSV(self):
        DataFilter.write_file(self.dataOut, "session.csv",
                              'w')  # use a for append instead

        # recommended use with pandas.to_csv()

    def sendToGithub(self):
        # 2 opens in a new tab
        webbrowser.open("https://github.com/LeonardoFerrisi/AVIAN", new=2)

    def sendToDocumentation(self):
        webbrowser.open(
            "https://docs.google.com/document/d/1QeNviy7b-XDDSJyjOnx1HarZ4NYg62vC9swysBj7l64/edit#heading=h.l4a81ocf76sq", new=2)

    def runMusicMaker(self):
        if self.audioOn:
            self.musicMaker.musicMaker()

    def audioOnAction(self):
        print("AUDIO IS ON")
        self.audioOn = True

    def audioOffAction(self):
        print("AUDIO IS OFF")
        self.audioOn = False

    def checkAudioOn(self):
        if self.audioOn:
            self.__init_music_maker()
        else:
            print("Audio set to off, doing nothing")

    # def checkStateSelect(self):
    #     """
    #     Checks the comboBox holding the state we want to look for
    #     :return:
    #     """
    #     if self.StateSelect.currentText() == "Concentration":
    #         self.brainStateVal = 1
    #     elif self.StateSelect.currentText() == "Releaxation":
    #         self.brainStateVal = 0
    #     else:
    #         self.brainStateVal = 1

    def retranslateUi(self, AVIAN_GUI):
        _translate = QtCore.QCoreApplication.translate
        AVIAN_GUI.setWindowTitle(_translate(
            "AVIAN_GUI", "AVIAN version 0.8 [Prototype]"))
        self.start_button.setText(_translate("AVIAN_GUI", "Start"))
        self.stop_button.setText(_translate("AVIAN_GUI", "Stop"))
        self.StateSelect.setItemText(
            0, _translate("AVIAN_GUI", "Concentration"))
        self.StateSelect.setItemText(1, _translate("AVIAN_GUI", "Relaxation"))
        self.StateSelect.setItemText(2, _translate("AVIAN_GUI", "Theta/Beta"))
        self.StateSelect.setItemText(
            3, _translate("AVIAN_GUI", "Alpha Threshold"))
        self.StateSelect.setItemText(
            4, _translate("AVIAN_GUI", "Beta Threshold"))
        self.star_one.setText(_translate(
            "AVIAN_GUI", "* Make Sure Board is connected before Starting!"))
        self.star_two.setText(_translate(
            "AVIAN_GUI", "** Select the board type below"))
        self.boardSelect.setItemText(0, _translate("AVIAN_GUI", "Synthetic"))
        self.boardSelect.setItemText(
            1, _translate("AVIAN_GUI", "OpenBCI [Cyton]"))
        self.boardSelect.setItemText(2, _translate(
            "AVIAN_GUI", "Muse (2016) [Requires BLED112]"))
        self.boardSelect.setItemText(3, _translate(
            "AVIAN_GUI", "Muse2 [Requires BLED112]"))
        self.selectmetric.setText(_translate(
            "AVIAN_GUI", "Select Metric to estimate:"))

        self.IS_CONNECTED.setText(_translate(
            "AVIAN_GUI", "[ Is connected: False ]"))

        self.connect_button.setText(_translate("AVIAN_GUI", "Connect"))
        self.disconnect_button.setText(_translate("AVIAN_GUI", "Disconnect"))
        self.playaudio_true_button.setText(_translate("AVIAN_GUI", "True"))
        self.playaudio_false_button.setText(_translate("AVIAN_GUI", "False"))
        self.playaud_label.setText(_translate(
            "AVIAN_GUI", "Play Audio on Threshold Pass"))
        # self.channels_label.setText(_translate("AVIAN_GUI", "Channels:"))
        # self.chan_1.setText(_translate("AVIAN_GUI", "[1]"))
        # self.chan_2.setText(_translate("AVIAN_GUI", "[2]"))
        # self.chan_3.setText(_translate("AVIAN_GUI", "[3]"))
        # self.chan_4.setText(_translate("AVIAN_GUI", "[4]"))
        # self.chan_5.setText(_translate("AVIAN_GUI", "[5]"))

        self.gamma_label.setText(_translate("AVIAN_GUI", "GAMMA"))
        self.delta_label.setText(_translate("AVIAN_GUI", "DELTA"))
        self.theta_label.setText(_translate("AVIAN_GUI", "THETA"))
        self.beta_label.setText(_translate("AVIAN_GUI", "BETA"))

        self.alpha_label.setText(_translate("AVIAN_GUI", "ALPHA"))

        self.gamma_value.setText(_translate("AVIAN_GUI", "[ ]"))
        self.delta_value.setText(_translate("AVIAN_GUI", "[ ]"))
        self.theta_value.setText(_translate("AVIAN_GUI", "[ ]"))
        self.beta_value.setText(_translate("AVIAN_GUI", "[ ]"))
        self.alpha_value.setText(_translate("AVIAN_GUI", "[ ]"))

        self.menuFile.setTitle(_translate("AVIAN_GUI", "File"))
        self.menuHelp.setTitle(_translate("AVIAN_GUI", "Help"))
        self.actionSave_as_CSV.setText(_translate("AVIAN_GUI", "Save as CSV"))
        self.actionGithub.setText(_translate("AVIAN_GUI", "Github"))
        self.actionDocumentation.setText(
            _translate("AVIAN_GUI", "Documentation"))


if __name__ == "__main__":
    app = QtGui.QApplication([])
    AVIAN_GUI = QtWidgets.QMainWindow()
    ui = AVIAN_MainWindow()
    ui.setupUi(AVIAN_GUI, app)
    AVIAN_GUI.show()
    QtGui.QApplication.instance().exec_()
