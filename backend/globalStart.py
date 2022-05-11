from sys import platform
from linux_run import LR
from win_run import WR
import os
import time

class gStart:

    def __init__(self, board, port=''):

        self.board = board
        self.port = port
        if platform == "linux" or platform == "linux2":
            pass

        elif platform == "darwin": # for OSX
            pass

        elif platform == "win32":

            callString_A = "python backend"+os.sep+"client.py "+"--board-id "+str(board)
            if port!='':
                callString_A+=" --serial-port "+str(port)
            fullCallA = f'start "Client" cmd /k "{callString_A}"'
            os.system(fullCallA)

            # time.sleep(2)

    def startSigProcessing(self):

        callString_B = "python backend"+os.sep+"sfpr.py "+"--master-id "+str(self.board)
        #TODO: add logic for more metrics 
        fullCallB = f'start "SFPR" cmd /k "{callString_B}"'
        os.system(fullCallB)

    def startOutput(self, isSelf=True, filePath='', args=''):
        if isSelf:
            pass
        else:
            callString = "python "+str(filePath)+" "+str(args)
            os.system()
    
if __name__ == "__main__":
    gStart(-1)