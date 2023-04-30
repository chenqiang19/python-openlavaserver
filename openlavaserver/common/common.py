import os
import re
import sys
import stat
import pexpect
import datetime
import subprocess

__all__ = ('printError', 'printWarning', )

def printError(message):
    """
    Print error message with red color.
    """
    print('\033[1;31m' + str(message) + '\033[0m')

def printWarning(message):
    """
    Print warning message with yellow color.
    """
    print('\033[1;33m' + str(message) + '\033[0m')

def stringToInt(inputString):
    """
    Switch the input string into ASCII number.
    """
    int_num = ''
    for char in inputString:
        num = ord(char)
        int_num = str(int_num) + str(num)
    int_num = int(int_num)
    return(int_num)

def subprocess_popen(command, mystdin=subprocess.PIPE, mystdout=subprocess.PIPE, mystderr=subprocess.PIPE):
    """
    Run system command with subprocess.Popen, get returncode/stdout/stderr.
    """
    SP = subprocess.Popen(command, shell=True, stdin=mystdin, stdout=mystdout, stderr=mystderr)
    (stdout, stderr) = SP.communicate()
    return(SP.returncode, stdout, stderr)