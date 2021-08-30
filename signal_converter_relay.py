import time
import numpy as np
import threading
from brainflow.data_filter import DataFilter
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams
from brainflow import BoardShim


class DataThread(threading.Thread):

    def __init__(self, myBoard: BoardShim, brainStateVal: int = 1):
        threading.Thread.__init__(self)
        self.myBoard = myBoard
        self.myBoard = myBoard

        self.myBoardID = self.myBoard.get_board_id()
        # self.exg_channels = chanCount
        # self.eeg_channels = self.myBoard.get_eeg_channels(self.myBoardID)
        self.exg_channels = self.myBoard.get_exg_channels(self.myBoardID)
        self.samplingRate = self.myBoard.get_sampling_rate(self.myBoardID)
        self.keep_alive = True
        self.brainStateVal = brainStateVal
        self.brain_state_model = self.prepare_model()  # CHECK THIS MAYBE IT WORKS
        self.prediction = None
        self.killed = False

    def suicide(self):
        """
        Kills the thread
        :return:
        """
        self.keep_alive = False
        self.killed = True

    def prepare_model(self):
        if self.brainStateVal not in [0, 1]:
            print('Please input 0 for relaxation and 1 for concentration')
            return

        if self.brainStateVal == 0:  # relaxation
            state_params = BrainFlowModelParams(BrainFlowMetrics.RELAXATION.value,
                                                BrainFlowClassifiers.REGRESSION.value)
            my_params = (state_params)
            # note in the example they used KNN not REGRESSION but in the widget, they use regression
        else:
            state_params = BrainFlowModelParams(BrainFlowMetrics.CONCENTRATION.value,
                                                BrainFlowClassifiers.REGRESSION.value)

        brainstate_model = MLModel(state_params)
        try:
            brainstate_model.prepare()
        except:
            pass

        return brainstate_model

    def predict_from_model(self, feature_vector, mymodel):
        # get band powers
        self.prediction = mymodel.predict(feature_vector)
        return self.prediction

    def release_model(self, mymodel):
        mymodel.release()

    def run(self):
        print(self.brainStateVal)
        if self.brainStateVal not in [0, 1]:
            print('Please pick concentration or relaxation model. \n '
                  '0: Relaxation \n'
                  '1: Concentration \n'
                  'Default is (0) Relaxation')
            return

        modelString = ('Relaxation', 'Concentration')
        print(f"Preparing model for {modelString[self.brainStateVal]}")

        win_size = 5
        sleeptime = 1
        points_per_update = win_size * self.samplingRate
        # print("length eeg channels: ", len(self.eeg_channels))
        print("length exg channels: ", len(self.exg_channels))
        print(self.samplingRate)
        while self.keep_alive:
            time.sleep(sleeptime)

            # get the board data ; doesnt remove data from the internal buffer
            # data = self.myBoard.getCurrentData(int(points_per_update)) # only for BoardComms object
            data = self.myBoard.get_current_board_data((int(points_per_update)))

            if data.shape[1] < points_per_update:
                print(data.shape)
                continue

            # USING BRAINFLOW'S RELAXATION/CONCENTRATION ML PREDICTION
            # They recommend 4s of data
            # bands = DataFilter.get_avg_band_powers(data, self.eeg_channels, self.samplingRate, True)
            bands = DataFilter.get_avg_band_powers(data, self.exg_channels, self.samplingRate, True)
            feature_vector = np.concatenate((bands[0], bands[1]))

            brain_state_prediction = self.predict_from_model(feature_vector, self.brain_state_model)

            self.prediction = brain_state_prediction

            # print(f"brainStateVal: {str(self.brainStateVal)}")
            # avian_main_gui.AVIAN_MainWindow.modStateProgressBar(brain_state_prediction)
            print(
                f"{modelString[self.brainStateVal]} prediction: {brain_state_prediction}")  ###########################

        # releasing model at the end
        self.release_model(self.brain_state_model)
