import os
from build import pre_setupdep
pre_setupdep()

from colorama import (Fore, Back, Style)
from consolemenu import clear_terminal
from time import sleep
class setup_server():
    def lookup_for_directory(self,name):

        path = os.path.abspath(__file__.strip('setup.py'))+"/"+name
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            print(f"{Back.CYAN + Fore.LIGHTMAGENTA_EX} {path} {Style.RESET_ALL} is validated.")

    def lookup_for_file(self,file, contain):
        path = os.path.abspath(__file__.strip('setup.py'))+"/"+file
        if not os.path.exists(path):
            with open(path,'w') as f:
                f.write(contain)
        else:
            print(f"{Back.CYAN + Fore.LIGHTMAGENTA_EX} {file} {Style.RESET_ALL} was validated.")

    def setup_now(self):

        self.lookup_for_directory('config')
        self.lookup_for_directory('share')
        self.lookup_for_directory('templates')
        self.lookup_for_directory('static')
        self.lookup_for_directory('JS')

        self.lookup_for_file('config/WFMUSER.json', '''
                            {
                                "default":{
                                    "crf":true,
                                    "caf":true,
                                    "password":"0",
                                    "login_enabled":true
                                }
                            }
                        ''')

        self.lookup_for_file('config/FSConfig.conf', '''
            port=2704
            share_directory=share/
        ''')

        self.lookup_for_file('config/SA.conf', '''
            name="ADMIN"
            password="ADM90X!"
        ''')



        sleep(0.25)
        clear_terminal()
        print(f"{Fore.GREEN} Setup & checks are complete. {Fore.RESET}")