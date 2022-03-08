#########################################
# MM
# For usage in AVIAN
#########################################

import time

import pygame
from threading import Thread
import os
import numpy as np
from signal_converter_relay import DataThread
from board_communicator import Comms as boardComm
# from theremin import Theremin
from numpy_ringbuffer import RingBuffer
from brainflow import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations
import pygame


class audioFeedback:

    def __init__(self, inputboard: boardComm, brainStateVal: int = 1, debugMsg=True):
        self.newBoard = inputboard
        self.brainStateVal = brainStateVal  # either concentration or relaxation
        self.prediction = None
        self.nMusicChannels = None
        self.predictionOut = None
        self.keepMMAlive = True
        self.showGatheringDataMsg = debugMsg

    def playWav(self, filename, channelNum):
        print(filename)
        # pygame.mixer.load(filename)
        pygame.mixer.Channel(channelNum).play(pygame.mixer.Sound(filename), -1)
        # try:
        #     pygame.mixer.Channel(channelNum).play(pygame.mixer.Sound(filename), -1)
        # except:
        #     pass

    def increaseVolume(self, channelNum):
        '''
        "Max Volume" on a channel
        '''
        chan = pygame.mixer.Channel(channelNum)
        chan.set_volume(0.75)

    def decreaseVolume(self, channelNum):
        '''
        Turn off Volume on a channel
        '''
        chan = pygame.mixer.Channel(channelNum)
        chan.set_volume(0)

    def loadWav(self):
        """
        Loads all the wave files (actually plays them but sets the volumes to 0)
        While waiting for neural data, plays bolero's drum beat
        Each wav file is played on a different audio channel
        Returns nMusicChannels (number of audio channels)
        Note: the audio channel number is an index into the wav file
        """
        pygame.mixer.init()
        # musicFolder = f"{os.path.sep}music"
        musicFolder = "audio"

        if self.brainStateVal == 1:  # Concentration Files
            filenames = {0: 'first_layer_c.wav', 1: 'second_layer_c.wav', 2: 'third_layer_c.wav',
                         3: 'fourth_layer_c.wav'}

        else:  # Relaxation Files, and everything else
            # filenames dict are chanNumber : wav file pairs
            filenames = {0: 'first_layer_r.wav', 1: 'second_layer_r.wav', 2: 'third_layer_r.wav',
                         3: 'fourth_layer_r.wav', 4: 'fifth_layer_r.wav'}

        self.nMusicChannels = len(filenames)
        self.playWav(
            f"{musicFolder}{os.path.sep}bolero_snare_drum.wav", self.nMusicChannels)
        self.increaseVolume(self.nMusicChannels)

        for chan in range(self.nMusicChannels):
            # self.multiplayer.loop(filename=f"{musicFolder}{filenames[chan]}", channel=chan,loopTimes=100)

            self.playWav(f"{musicFolder}{os.path.sep}{filenames[chan]}", chan)

            self.decreaseVolume(chan)

    def predToWavFeats(self, avg_prediction):
        """
        Gets prediction in MusicMaker (avg of the last 5 predictions output by brainAnalyzer)
        and gets nMusicChannels from loadWav
        For each prediction, adjusts the volume of the music channels
        Right now, the layering is fixed (First Layer, Second Layer...)
        With increasing concentration (or relaxation), more layers have volume on

        :param prediction: classifier prediction float 0-1
        :param nMusicChannels: Number of music channels integer
        :return: doesnt return anything, just adjusts volume
        """
        # if avg_prediction is not None:
        # couldnt check for nan so just looked for if the string version of it is nan
        if str(avg_prediction) != 'nan':
            thresholds = []
            # turn off the drum beat
            self.decreaseVolume(self.nMusicChannels)
            # takes the prediction of brain state and maps it to changes in the way that wav files are being played
            # thresholds = np.linspace(0.5, 0, self.nMusicChannels)
            if self.nMusicChannels == 5:  # Basically these channels all have different thresholds so different files play in different ways
                thresholds = [.93, .87, .70, .2, .00]
            elif self.nMusicChannels == 4:
                thresholds = [.9, .5, .3, .00]

            for chan in range(self.nMusicChannels):
                if avg_prediction > thresholds[chan]:
                    # print("PREDICTION IS ABOVE THRESHOLD")
                    self.increaseVolume(chan)
                else:
                    self.decreaseVolume(chan)
        # else:
        #     print("gathering data please hold")
            # pass

    def musicMaker(self):
        # def listener(self, threshold):
        """
        # listens to brain state predictions and uses it to decide how to change the music
        # listens to prediction and then averages the last 5 predictions
        # calls predToWave to adjust volumes

        :return: average prediction
        """
        # imported DataThread from signal_converter_relayOld.py

        if self.brainStateVal == 1 or self.brainStateVal == 0:

            self.bciThread = DataThread(
                self.newBoard.board, self.brainStateVal)
            state = self.brainStateVal
            # if state == 0:
            # elif
            # if
            self.bciThread.start()  # starts the thread
            # self.bciThread.run()
            pHolder = RingBuffer(2)  # prediction holder
            startTime = time.time()
            critval = 0.99
            counter = 0
            while self.keepMMAlive:

                # print('is running musicMaker')
                self.prediction = self.bciThread.prediction

                pHolder.appendleft(self.prediction)

                avg_prediction = np.mean(pHolder)
                if avg_prediction > critval:
                    counter += 1
                else:
                    counter = 0

                self.predictionOut = avg_prediction
                self.predToWavFeats(avg_prediction)

        elif self.brainStateVal == 2:

            self.runBandPowerRatio("theta", "beta")  # run theta/beta ratio

    def runBandPowerRatio(self, BP1: str, BP2: str):
        """
        Runs a loop containing the Band Power ratio and responding to it with sound
        :param BP1:
        :param BP2:
        :return:
        """
        ourBoardShim = self.newBoard.board
        samplingRate = ourBoardShim.get_sampling_rate(
            self.newBoard.board.get_board_id())
        nfft = DataFilter.get_nearest_power_of_two(samplingRate)
        windowSize = 5
        points_per_update = windowSize * samplingRate

        while self.keepMMAlive:

            if BP1 == "theta" and BP2 == "beta":

                ourData = self.newBoard.board.get_current_board_data(
                    num_samples=points_per_update)
                for channel in self.newBoard.getEXGChannels():
                    DataFilter.detrend(
                        ourData[channel], DetrendOperations.LINEAR.value)
                    psd = DataFilter.get_psd_welch(data=ourData[channel], nfft=nfft, overlap=nfft // 2,
                                                   sampling_rate=samplingRate, window=WindowFunctions.BLACKMAN_HARRIS.value)

                    band_power_theta = DataFilter.get_band_power(
                        psd=psd, freq_start=4.0, freq_end=7.0)
                    band_power_beta = DataFilter.get_band_power(
                        psd=psd, freq_start=13.0, freq_end=30.0)

    def kill(self):
        """
        Kill music maker
        :return:
        """
        pygame.mixer.stop()
        self.bciThread.suicide()
        self.keepMMAlive = False

    def start(self):
        self.initBoard()

    def initBoard(self):
        """
        Initiates board ... do we need this or does boardCommunicator take care of it?
        :param boardID: By default synthetic, can be set to the ID number of any board we want
        :param serial_port: By default nothing, can be set to the serial port taking data from your board
        """
        # run bc and scr
        # self.newBoard = boardComm(boardID, serial_port)
        self.newBoard.startStream()
        print('Now Streaming')
        # while True:
        #     pass

    def brainAnalyzer(self):
        """
        Sets up board and sends out brain state prediction
        :return:
        """
        # a = Thread(target=self.runBCIThread)
        b = Thread(target=self.musicMaker)
        # a.start()
        b.start()

    def initializeBoard(self):
        """
        Prepares the board for streaming and starts a stream
        :return:
        """
        self.newBoard.startStream()

    def update(self):
        """
        Updates the data stream from a board that is streaming
        :return:
        """


if __name__ == '__main__':
    pass
