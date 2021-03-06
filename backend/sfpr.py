import socket
import argparse
from threading import local
import time
import numpy as np

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations, NoiseTypes

from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams

import math
import socket
import zmq
import sys

"""
SFPR: Signal Filtering and Processing Relay
"""
class SFPR:

    # def __init__(self, masterboardId : int, useArgs : bool=True):

    #     # Initilize the board for usage in local
    #     board_id = -2
    #     params = BrainFlowInputParams()
    #     params.ip_port = 6677
    #     params.other_info = -1 # board id of master board (is a synth board)
        
    #     # On off switches for what to use (use the builtin methods to change them!)
    #     self.doFocus = False
    #     self.doSSVEPbool = False
    #     self.doRelaxation = False
        
    #     if useArgs:
    #         parser = argparse.ArgumentParser()
    #         parser.add_argument('--master-id', type=int, help='board id, right now either -1, 0 or 22 for synth, cython or muse2', required=False, default=-1)
    #         parser.add_argument('--do-focus', type=str, help='true or false value for whether or not we want focus metric', required=False, default='True')
    #         #TODO: add more args for more metrics
    #         args = parser.parse_args()
    #         params.other_info = str(args.master_id) # board id of master board (is a synth board)
    #         if args.do_focus == 'True':
    #             self.doFocus = True    
            
    #     params.ip_address = '225.1.1.1'
    #     self.board_recv = BoardShim(board_id, input_params=params)

    #     self.master_board_id = masterboardId

    #     self.eeg_channels = BoardShim.get_eeg_channels(
    #         int(self.master_board_id))
    #     self.sampling_rate = BoardShim.get_sampling_rate(
    #         int(self.master_board_id))
    #     print(f"MASTER ID: {self.master_board_id}")
    #     self.nfft = DataFilter.get_nearest_power_of_two(self.sampling_rate)
    #     # Init stream
    #     self.initStream = False

    #     # Data holders
    #     self.wholeData = 0
    #     self.currentData = 0

    #     # Relays - activate or deactivate these depending on what we want to measure
    #     self.relays = {'focus': False, 'relaxation': False, 'alpha': False,
    #                    'beta': False, 'gamma': False, 'delta': False, 'theta': False}

    #     # For sending commands to output (Module 3)
    #     # ZMQ Attempt
    #     self.ctx = zmq.Context()
    #     self.sock = self.ctx.socket(zmq.PUB)
    #     self.sock.bind("tcp://*:1234")
    #     ################

    #     # for controlling loop
    #     self.inf = False

    #     # predictions if using ml
    #     self.prediction = 0.0

    def __init__(self, useArgs : bool=True):

        # Initilize the board for usage in local
        board_id = -2
        params = BrainFlowInputParams()
        params.ip_port = 6677
        # params.other_info = str(masterboardId) # board id of master board (is a synth board)
        
        # On off switches for what to use (use the builtin methods to change them!)
        self.doFocus = False
        self.doSSVEPbool = False
        self.doRelaxation = False
        
        if useArgs:
            parser = argparse.ArgumentParser()
            parser.add_argument('--master-id', type=int, help='board id, right now either -1, 0 or 22 for synth, cython or muse2', required=False, default=-1)
            parser.add_argument('--do-focus', type=str, help='true or false value for whether or not we want focus metric', required=False, default='True')
            #TODO: add more args for more metrics
            args = parser.parse_args()
            params.other_info = str(args.master_id) # board id of master board (is a synth board)
            if args.do_focus == 'True':
                self.doFocus = True    
            
        params.ip_address = '225.1.1.1'
        self.board_recv = BoardShim(board_id, input_params=params)

        self.master_board_id = params.other_info

        self.eeg_channels = BoardShim.get_eeg_channels(
            int(self.master_board_id))
        self.sampling_rate = BoardShim.get_sampling_rate(int(self.master_board_id))
        self.nfft = DataFilter.get_nearest_power_of_two(self.sampling_rate)
        # Init stream
        self.initStream = False

        # Data holders
        self.wholeData = 0
        self.currentData = 0

        # Relays - activate or deactivate these depending on what we want to measure
        self.relays = {'focus': False, 'relaxation': False, 'alpha': False,
                       'beta': False, 'gamma': False, 'delta': False, 'theta': False}

        # For sending commands to output (Module 3)
        # ZMQ Attempt
        self.ctx = zmq.Context()
        self.sock = self.ctx.socket(zmq.PUB)
        self.sock.bind("tcp://*:1234")
        ################

        # for controlling loop
        self.inf = False

        # predictions if using ml
        self.prediction = 0.0
        

    def recieve(self, isInf=True, runOnce=False):
        '''
        Recieves the stream of EEG data from a designated port {params.ip_address}:{params.ip_port}
        @param isInf: Determines whether or not we want to be running a infinite loop 
        @param runOnce: Determine whether or not we want to run only once (isInf cannot be on)
        '''
        self.board_recv.prepare_session()
        self.board_recv.start_stream(45000)

        self.inf = isInf # Whether or not loop runs forever

        time.sleep(5)

        # switches #####################
        modelPrepared = False

        keep_alive = self.inf

        sendOverSocket = True

        socketPrepared = False

        #############################

        useML = self.doFocus # Right now only checks for measuring ML metric for concentration
        useSVVEP = self.doSSVEPbool

        ### Timer
        
        ###

        self.prepareMLModel('focus')
        modelPrepared = True
        
        while keep_alive:

            time.sleep(5)

            # self.wholeData = self.board_recv.get_board_data()

            self.currentData = self.board_recv.get_current_board_data(
                self.sampling_rate*5)

            if self.currentData.size == 0:
                print("still empty")
                # print(self.currentData)

            else:
                
                # APPLY essential filters #######################

                # Do NOTCH filter
                
                try: 
                    for count, channel in enumerate(self.eeg_channels):
                        DataFilter.remove_environmental_noise(self.currentData[channel], self.sampling_rate, NoiseTypes.SIXTY.value)
                    # print("NOTCH FILTER SUCCESSFULLY APPLIED")
                
                except:
                    print("NOTCH FILTER FAILED TO EXECUTE")


                #################################################

                if useML:
                    bands = DataFilter.get_avg_band_powers(
                    self.currentData, self.eeg_channels, self.sampling_rate, True)
                    # print('Bands size: %f' % len(bands))
                    feature_vector = np.concatenate((bands[0], bands[1]))

                    if modelPrepared == False:
                        self.prepareMLModel('focus')
                        modelPrepared = True
                    else:
                        # print('Bands: ', bands)
                        # print('Feature Vector: ', str(feature_vector))

                        self.prediction = self.concentration.predict(
                            feature_vector)
                        print("Concentration Lvl: %f" % self.prediction) 

                        if sendOverSocket:
                            toSend = str(self.prediction)
                            output = f"Calculated Focus value:{toSend}"
                            self.sock.send_string(output)

                if useSVVEP:

                    # Do all SSVEP values for 4 squares we want 
                    wantedSSVEPValues = [10, 15, 20, 25] # wanted values in HZ

                    self.doSSVEP(num_channels=self.eeg_channels, currentData=self.currentData, samplingRate=self.sampling_rate, sendOverSocket=sendOverSocket, valuesWeWant=wantedSSVEPValues)

                    # FORMAT: doSSVEP(num_channels, currentData, samplingRate, sendOverSocket, valuesWeWant : list):

                    # For sending SSVEP values out


        if runOnce and not isInf:
            self.runOnce()


    def runML(self):
        pass

    def doSSVEP(self, num_channels, currentData, samplingRate, sendOverSocket, valuesWeWant : list):
        '''
        Takes parameters from reciever function and sfpr class in order to get SSVEP values from a list

        @param num_channels: The number of eeg_channels our board has
        @param currentData: The current data being streamed from our board
        @param samplingRate: The sampling rate of our board
        @param sendOverSocket: Boolean value of whether or not we want to send over socket
        @param valuesWeWant: A list containing values of SSVEP we want to scan for (SSVEP values are in Hertz)
        '''


        # create dict of all _ssvepTotals
        
        _ssvepTotals = {}

        for value in valuesWeWant:
            _ssvepTotals[value] = 0.0
        
        # print(_ssvepTotals)
        
        ##################################

        # Detrend data and get PSD welch from every single channel

        for i in num_channels:

            DataFilter.detrend(currentData[i], DetrendOperations.LINEAR.value)

            psd = DataFilter.get_psd_welch(currentData[i], self.nfft, self.nfft // 2, samplingRate,
                        WindowFunctions.BLACKMAN_HARRIS.value)


            for ssvepVal in valuesWeWant:
                toAdd = DataFilter.get_band_power(psd, float(ssvepVal - 1.0), float(ssvepVal + 1.0)) # gets a range of + or minus 1.0
                currentValue = _ssvepTotals[ssvepVal]
                _ssvepTotals[ssvepVal] = currentValue+toAdd
                # print('SSVEP VALUE: ', ssvepVal, ', Current lvl: ', _ssvepTotals[ssvepVal])

        # print('SSVEP TOTALS [ pre averaged ]: ', _ssvepTotals)

        for ssvepValue in _ssvepTotals:
            averagedValue = int(ssvepValue) / len(num_channels)
            _ssvepTotals[ssvepValue] = averagedValue
        
        print('SSVEP TOTALS: ', _ssvepTotals)

        try: 
            if sendOverSocket:
                toSend = str(_ssvepTotals)
                # output = f"Calculated SSVEP values: {toSend}"
                output = toSend
                self.sock.send_string(output)
        except:
            print("Socket send FAILED")

    ###################################################################

    def activateFocus(self):
        '''
        Sets the focus value to true, any other values are true shuts them off.

        RUN THIS BEFORE YOU run recieve()
        '''
        if self.doFocus == False:
            if self.doSSVEP:
                self.doSSVEP = False
            if self.doRelaxation:
                self.doRelaxation = False
            print("\nMeasuring FOCUS value from data\n")
            self.doFocus = True


    # Theres a better way of doing this but whatever...

    def activateSSVEP(self):
        # TODO: Needs more info, activate SSVEP should as for a range of values that it can send out
        '''
        Sets the check for SSVEP value to true, any other values are true shuts them off.

        RUN THIS BEFORE YOU run recieve()
        '''
        if self.doSSVEPbool == False:
            if self.doFocus:
                self.doFocus = False
            if self.doRelaxation:
                self.doRelaxation = False
            print("\nMeasuring SSVEP value from data\n")

            self.doSSVEPbool = True

    def activateRelaxation(self):
        '''
        Sets the check for SSVEP value to true, any other values are true shuts them off.

        RUN THIS BEFORE YOU run recieve()
        '''
        if self.doRelaxation == False:
            if self.doFocus:
                self.doFocus = False
            if self.doSSVEP:
                self.doSSVEP = False

            print("\nMeasuring RELAXATION value from data\n")

            self.doRelaxation = True

    ########################################################

    def prepareMLModel(self, metric):
        '''
        Prepares the machine learning model to predict a value for. (Currently only accomadates concentration values)
        @param metric: The build in ML metric we are using. Choose among: 'focus'
        '''
        if metric == 'focus':
            MLModel.enable_dev_ml_logger()
            concentration_params = BrainFlowModelParams(
                BrainFlowMetrics.CONCENTRATION.value, BrainFlowClassifiers.REGRESSION.value)

            self.concentration = MLModel(concentration_params)
            self.concentration.prepare()

    def runOnce(self):
        '''
        Runs the SFPR only once
        '''
        self.currentData = self.board_recv.get_current_board_data(
            self.sampling_rate*5)
        bands = DataFilter.get_avg_band_powers(
            self.currentData, self.eeg_channels, self.sampling_rate, True)

        print(bands)
        print(len(bands))

    def endStream(self):
        '''
        Ends the board's data stream
        '''
        self.board_recv.stop_stream()

    def releaseSession(self):
        '''
        Releases the board stream session, in order to run board again... must re-prepare session
        '''
        self.board_recv.release_session()


if __name__ == "__main__":
    newRelay = SFPR() # USE ARGS IS BY DEFAULT TRUE
    # newRelay = SFPR(22, useArgs=False) # indicates muse 2

    # newRelay = SFPR(0)
    newRelay.activateFocus()
    # newRelay.activateSSVEP()
    # print('Do SSVEP value: ', newRelay.doSSVEP)
    newRelay.recieve()
    exit = input("Press ENTER to exit")
