def getBoardFromInput():
    board_select = ''
    print("Which board do you want? Press: \n<ENTER> for synthetic,\n0 for OpenBCI Cyton,\n1 for Muse 2\n(more coming soon!)")
    board_select = input(">> ")
    print("BOARD SELECT: board:"+str(board_select)+", type: "+str(type(board_select)))
    board = 999
    
    if board_select == '0':
        board = 0
    elif board_select == '1':
        board = 22
    else:
        board = -1
    print("BOARD SELECTED: "+str(board)+", type: "+str(type(board)))
    return board

def getPortFromInput(boardID):
    serialPort = ''
    if boardID!=-1:
        print("You entered a board that requires access to a serial port! Please enter it below")
        serialPort = input(">> ")
        #TODO: Add evalutation logic to see if serial_port is valid
    return serialPort