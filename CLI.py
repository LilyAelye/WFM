#@
# CLI | WFS
#@
from imported import cli_run
import importlib
import os
import threading
from consolemenu import clear_terminal
from colorama import Style, Fore
import subprocess
global msg
msg = ""
term_open = True

def run_oc(cm :str):
    global msg
    msg = msg + "\n"
    def append_to_msg(text):
            global msg
            msg = msg+text + " \n "
    if cm == "boot":
        global os
        msg = msg+ f"{Fore.GREEN} Running server {Fore.RESET}"
        subprocess.call(['python3', 'runpy_k.py'])  # Adjust as necessary

       
        return True
    elif cm == 'help':
    
        msg = msg+ "" \
        "boot - Boots the WFS server. \n" \
        "help - Shows this message \n" \
        "set - 2 parameters - Sets a setting of WFS. \n" \
        ""
        return True
    elif cm.startswith('help'):
        split = cm.split(" ")
        
        append_to_msg(f"{Fore.BLUE}[help]{Fore.RESET} \n")
        if split[1] == "set":
            append_to_msg(
            "SET [param] [value] \n"\
            "Changes a parameter to the value provided \n" \
            f"{Fore.BLUE}")
            append_to_msg("parameters that can be modified:")
            append_to_msg("port [Default: 2704] - The internet port used to host.")
            append_to_msg('sd [Default: share/] - Changes the share directory but do not put quotes or ""' + " or '' ")
            append_to_msg(f"{Fore.RESET}")
        elif split[1] == "boot":
            append_to_msg(
                "boot\n"\
                "Starts the WFS Web fileshare" \
                " "
            )
        else:
            append_to_msg("Command not found in help.")
            return False
        return True
    elif cm.startswith('set '):
        seqs = cm.split(" ")
        print(seqs)
        if seqs[1] == 'port':
             print("port")
             config = 'config/FSConfig.conf'
             import os
             ln = 0
             text_to_strip = ""
             content = ""
             line_text = ""
             if os.path.exists(config):
                  with open(config,'r') as f:
                    
                    for line in f:
                        ln=ln +1
                        
                        if line.startswith('port='):
                            print(ln)
                            line_text = line
                            text_to_strip = f"port={str(seqs[2] or '2704') or '2704'}"
                            
                            
                            break
                        else:
                            line_text = ""
                            text_to_strip = f"port={str(seqs[2] or '2704') or '2704'}"
                  with open(config,'r') as f3:
                      for seq in f3.readlines():
                          content = content + seq 
                  with open(config,'w') as f2:
                      #f2.seek(0)
                      f2.write(content.replace(line_text, text_to_strip + '\n'))
                      print(line_text, text_to_strip)
                      #f2.truncate()
                      append_to_msg(f"{Fore.GREEN} Succesfully set port to {str(seqs[2]) or "2704"} {Fore.RESET}")
                      return True
        
        msg = msg+"\n"
    elif cm == "exit":
        global term_open
        term_open = False
    return False

    

while term_open:
        clear_terminal()
        
        print(f"" \
        "Welcome to the WFS CLI. \n \n" \
        "Latest output: \n" \
        f"{msg}{Style.RESET_ALL}" \
        "\n" \
        f"To use any commands please enter it or use '{Fore.BLUE}help{Fore.RESET}' to get help.\n")
        Command = input('' \
        f'{Fore.BLUE}WFS{Fore.RESET} {Fore.YELLOW}>{Fore.LIGHTMAGENTA_EX} ' \
        ' ')
        msg = "> "+Command
        origin = msg
        color = run_oc(Command)
        msg = msg.strip(origin)
        origin = f"{color and Fore.GREEN or Fore.RED} {origin} {Fore.RESET}"
        origin = origin + msg
        if Command != "":
            if color == False:
                origin = origin + f"\n {Fore.RED} Invalid command found! {Fore.RESET} Please type '{Fore.BLUE}help{Fore.RESET}' to get help. \n"
            msg = f"{origin} {Fore.RESET}"

