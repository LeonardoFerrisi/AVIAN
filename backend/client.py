import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations
import time
import argparse


class Comms:
    '''
    Class for communciation between a wireless EEG amplifier and the computer
    '''

    def __init__(self, boardID=-1, serialPort='', useArgs=True):
        BoardShim.enable_dev_board_logger()
        board_id = boardID
        serial_port=''
        
        if useArgs:
            parser = argparse.ArgumentParser()
            parser.add_argument('--board-id', type=int, help='board id, right now either -1, 0 or 22 for synth, cython or muse2', required=False, default=-1)
            parser.add_argument('--serial-port', type=str, help='serial port for connecting to a board', required=False, default='')
            args = parser.parse_args()
            board_id = args.board_id
            serial_port = args.serial_port
        else:
            board_id = boardID
            serial_port = serialPort
            
        params = BrainFlowInputParams()
        params.serial_port = serial_port
        self.board = BoardShim(board_id=board_id, input_params=params) 
        


    def start(self, inf=False, timeSleep=20):
        '''
        Starts a stream of EEG data from the board
        @param inf: Determines whether we want to run infinitely or not
        @param timeSleep: Determines the amount of time we want to wait before ending data stream. Only works if param inf is False
        '''

        self.board.prepare_session()
        self.board.start_stream(45000, 'streaming_board://225.1.1.1:6677')

        if not inf:
            self.stop(delay=timeSleep)

    def stop(self, delay=0):
        '''
        Stops the stream of EEG data from the board and releases the session
        @param delay: The amount fo seconds to delay  stopping the board by
        '''
        if delay > 0:
            BoardShim.log_message(LogLevels.LEVEL_INFO.value,
                                  'start sleeping in the main thread')
        time.sleep(delay)
        self.board.stop_stream()
        self.board.release_session()


if __name__ == "__main__":

    comms = Comms()
    # comms = Comms(boardID = 22, serialPort='COM3', useArgs=False)

    # comms = Comms(0, '/dev/ttyUSB0')

    # comms = Comms(boardID = 0, serialPort='COM4')
    # comms = Comms(boardID = -1)

    comms.start(inf=True)
    end = input("PRESS ENTER TO EXIT")
    comms.stop()
