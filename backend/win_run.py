import os
import time
from _boardInfo import getBoardFromInput, getPortFromInput
# TODO: Add options menu to select boards to stream from, COM ports, serial ports if need be, etc...


class WR:
    def __init__(self):

        ascii_logo = '''                                             
                                °°                             
                              °@@@@@@°                          
                            *@@@@@@@@@@°                        
                          @@@@@@@@@@@@@@                       
                        °@@@@@@@oo@@@@@@@°                     
                        °@@@@@@@    @@@@@@@°                    
                        @@@@@@#      #@@@@@@                    
                      #@@@@@@        @@@@@@#                   
                      @@@@@@O@@@@@@@@@@@@@@@                   
                      .@@@@@@O@@@@@@@@@@@@@@@o                  
                  *@@O@@@@@@O@@@@@@@@@@@@@@@@@@*               
                o@@@@@O@@@@@@       .@@@@@@@@@@@@o             
              .@@@@@@@*@@@@@@@      @@@@@@@@@@@@@@@.           
              *@@@@@@@°  @@@@@@@.  .@@@@@@@  °@@@@@@@*          
            *@@@@@@#    .@@@@@@@*#@@@@@@@     #@@@@@@*         
            @@@@@@o       O@@@@@@@@@@@@O       o@@@@@@         
            #@@@@@@O**°°°*o#@@@@@@@@@@@@Oo*°°°**O@@@@@@O        
            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
            °#@@@@@@@@@@@@@@@@@@#*.o@@@@@@@@@@@@@@@@@@#°        
                °*OO#####O*°          °*O#####OO*°             
                
                [Mind] --> [Computer] --> [Machine]
    '''

        print("Welcome to Trinity v0.12!")
        print(ascii_logo)
        start = input("Press <ENTER> to start!\n")

        time.sleep(1)
        
        # Get board information

        board = getBoardFromInput()
        
        time.sleep(1)
        
        port = getPortFromInput(board)
        

        print("Now opening Communications Client, please hold ...\n")

        # TODO: Insert logic to specify board
        callString_A = "python client.py "+"--board-id "+str(board)
        if port!='':
          callString_A+=" --serial-port "+str(port)
        fullCallA = f'start "Client" cmd /k "{callString_A}"'
        os.system(fullCallA)

        time.sleep(1)

        # TODO: Insert logic to specifc metric and other features of signal processing

        print("Now opening Signal Filtering and Processing Relay , please hold ...\n")

        time.sleep(2)
        callString_B = "python sfpr.py "+"--master-id "+str(board)
        #TODO: add logic for more metrics 
        fullCallB = f'start "SFPR" cmd /k "{callString_B}"'
        os.system(fullCallB)

        time.sleep(1)

        # TODO: Insert logic to select which program should listen to SFPR

        print("Now opening Concentration output , please hold ...\n")

        time.sleep(1)

        os.system('start "Concentration OUT" cmd /k "python out.py"')

        exit = input("Press <ENTER> again to exit")
