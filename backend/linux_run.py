import os
import time
from subprocess import call

# THIS IS THE LINUX version of RUN

# TODO: Add options menu to select boards to stream from, COM ports, serial ports if need be, etc...


class LR:

    def __init__(self, includeLogo=True):

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

        if includeLogo:
            print(ascii_logo)
        print("Welcome to Trinity v0.12p [PRIVATE BUILD]!")

        start = input("Press <ENTER> to start!\n")

        board = ''
        metric = ''

        # get current working directory

        current_directory = os.getcwd()
        os.system(f"cd {current_directory}")
        new_dir = current_directory+os.sep+"lib"
        os.chdir(new_dir)
        print(f"Current directory: {new_dir}\n")

        time.sleep(1)

        print("Now opening Communications Client, please hold ...\n")

        # TODO: ADD logic to specify which board we want!
        # chooseBoards()

        call(['gnome-terminal', '-e', "python3 client.py"])

        time.sleep(1)

        # TODO: ADD logic to specify metric we want to look for
        # chooseMetric()

        print("Now opening Signal Filtering and Processing Relay , please hold ...\n")

        time.sleep(2)

        call(['gnome-terminal', '-e', "python3 sfpr.py"])

        time.sleep(1)

        print("Now opening Concentration output , please hold ...\n")

        time.sleep(1)

        call(['gnome-terminal', '-e', "python3 out.py"])

        exit = input("Press <ENTER> again to exit")

    def chooseBoards(self):
        pass

    def chooseMetric(self):
        pass

if __name__=="__main__":
  run = LR()