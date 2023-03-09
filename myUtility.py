import myException as EX
import platform
import json
import os

from colorama import Style, Fore, init
from datetime import datetime
from enum import Enum

SEPARATOR = "\\" if platform.system() == "Windows" else "/"
CURRENT_DATE = datetime.now().strftime('%Y_%m_%d')
CURRENT_PATH = os.getcwd()

class LEVEL(Enum):

    DEBUG = "DEBUG"
    ERROR = "ERROR"
    INFO = "INFO"

class PATH(Enum): 

    LOG_FILE_PATH = CURRENT_PATH + SEPARATOR + "LOGS" + SEPARATOR

class FILENAME(Enum):

    OUTPUT_FILENAME = "queryFormatted.txt"
    TEST_INPUT_FILENAME = "queryTest.txt"
    LOG_FILE = f"log_{CURRENT_DATE}.txt"
    INPUT_FILENAME = "queryInput.txt"
    AST_FILENAME = "AST.json"

def writeLog(msg, level, onlyPrompt=False):

    msg = "\n" + json.dumps(msg, indent=4) if isinstance(msg, dict) or isinstance(msg, list) else str(msg)
    
    color = Fore.RED if level == LEVEL.ERROR else Fore.GREEN if level == LEVEL.DEBUG else Fore.WHITE

    if not onlyPrompt:
        with open(PATH.LOG_FILE_PATH.value + FILENAME.LOG_FILE.value, "a") as fileLog: 
            fileLog.writelines(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\t[{level.value}]\t\t{msg}\n")

    print(color + f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\t[{level.value}]\t\t{msg}", Style.RESET_ALL)

def createFolders(): 
    
    if not os.path.exists(PATH.LOG_FILE_PATH.value): mkdir(PATH.LOG_FILE_PATH.value)


init()