import math
import zmq

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.gridspec as gridspec
import logging

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

import json


class Visualizer:

    def __init__(self):
        self.ctx = zmq.Context()
        self.sock = self.ctx.socket(zmq.SUB)
        self.sock.connect("tcp://127.0.0.1:1234")
        self.sock.subscribe("")  # Subscribe to all topics
        self.keep_alive = True


        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title='Frequency Amplitude',size=(800, 600))

        self.update_speed_ms = 50
        self.window_size = 4


        self._init_pens()
        self._init_ssvep_plot()

        timer = QtCore.QTimer()
        timer.timeout.connect(self.display)
        timer.start(self.update_speed_ms)
        QtGui.QApplication.instance().exec_()

    def spin(self):
        '''
        Keeps the Controller listening and recieving all incoming topics, 
        in this case will constantly be listening to comands from Signal Filter and Processing Relay 
        '''
        print("Starting reciever loop . . . ")
        print("Listening for output value")

        while self.keep_alive:
            msg = self.sock.recv_string()
            # print(f"Calculated SSVEP: {msg}")
            print(msg)


    def display(self):
        data = self.sock.recv_string()


        print(data)
        ssvepData = json.loads(data)
        # ssvepData = dict(data)
        print(ssvepData)
        avgSSVEP = [0,0,0,0]

        count = 0
        for ssvepVal in ssvepData:
            avgSSVEP[count] = ssvepData[ssvepVal]
            count+=1

        self.band_bar.setOpts(height=avgSSVEP)

        self.app.processEvents()

    def _init_pens(self):
        self.pens = list()
        self.brushes = list()
        colors = ['#A54E4E', '#A473B6', '#5B45A4', '#2079D2', '#32B798', '#2FA537', '#9DA52F', '#A57E2F', '#A53B2F']
        for i in range(len(colors)):
            pen = pg.mkPen({'color': colors[i], 'width': 2})
            self.pens.append(pen)
            brush = pg.mkBrush(colors[i])
            self.brushes.append(brush)

    def _init_ssvep_plot(self):
        self.ssvep_plot = self.win
        self.band_plot = self.win.addPlot(row=4//2, col=1, rowspan=4//2)
        self.band_plot.showAxis('left', False)
        self.band_plot.setMenuEnabled('left', False)
        self.band_plot.showAxis('bottom', False)
        self.band_plot.setMenuEnabled('bottom', False)
        self.band_plot.setTitle('SSVEP Plot')
        y = [0, 0, 0, 0]
        x = [10, 15, 20, 25]
        self.band_bar = pg.BarGraphItem(x=x, height=y, width=0.8, pen=self.pens[0], brush=self.brushes[0])
        self.band_plot.addItem(self.band_bar)


if __name__ == "__main__":

    try:
        vis = Visualizer()
    except BaseException as e:
        logging.warning('Exception', exc_info=True)
    # vis.spin()
