#!/usr/bin/python
from key import *
import settings
import bot
import sys
import wallet
import history

class History:
    def __init__(self):
        print('starting...')

    def main(self):
        #interpret flags from cli
        flags = {'start': "-s", 'end': "-e"}
        for (i, arg) in enumerate(sys.argv):

            if(arg.startswith('-')):
                if(i < len(sys.argv) -1 ):
                    if(sys.argv[i+1].startswith('-')):
                        flags[arg[1:]] = arg[1:]
                    else:
                        flags[arg[1:]] = sys.argv[i + 1]
        settings.init(flags)
        history.fetchHistory(self, flags)

if __name__ == "__main__":
    objName = History()
    objName.main() 