import serial
import socket
import zmq
import time

# import numpy as np
# import matplotlib.pyplot as plt
# from collections import deque
import serial
import re


class Controller:
    """
    Very very basic script that displays the output from sfpr
    """
    def __init__(self):

        self.ctx = zmq.Context()
        self.sock = self.ctx.socket(zmq.SUB)
        self.sock.connect("tcp://127.0.0.1:1234")
        self.sock.subscribe("")  # Subscribe to all topics
        self.keep_alive = True

        # subplit stuff

        # self.ser = serial.Serial('COM4', 9600)    

    def spin(self):
        '''
        Keeps the Controller listening and recieving all incoming topics, 
        in this case will constantly be listening to comands from Signal Filter and Processing Relay 
        '''
        print("Starting reciever loop . . . ")
        print("Listening for output value")

        while self.keep_alive:
            msg = self.sock.recv_string()
            print(msg)

            toSend = re.split('[:]', msg)[1]
            print(f"toSend:{toSend}")

            if (float(toSend) > float(0.5)):
                print("YEETUS")
                # self.ser.write("true\n")
            else:
                print("BEETUUS")
                # self.ser.write("false\n")

        self.sock.close()
        self.ctx.term()


if __name__ == "__main__":
    controller = Controller()
    controller.spin()