from sys import platform
from linux_run import LR
from win_run import WR

def RUN():
    if platform == "linux" or platform == "linux2":
        linux = LR()

    elif platform == "darwin":
        pass

    elif platform == "win32":
        windows = WR()
        
if __name__ == "__main__":
    RUN()