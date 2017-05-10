import sys
import subprocess
import platform
import os

def get_size():
    rows, columns = os.popen('stty size', 'r').read().split()
    return rows, columns

def clear():
    if platform.system() == "Windows":
        subprocess.call("cls", shell=True)
    else:
        subprocess.call("clear", shell=True)

def cls():
    #print("\x1b[2J\x1b[H")
    #sys.stderr.write("\x1b[2J\x1b[H")
    clear()

def pause(msg='press return to continue...'):
    _ = input(msg)