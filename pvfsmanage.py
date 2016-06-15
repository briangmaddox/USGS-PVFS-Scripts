#! /usr/bin/env python

import os
import sys
import string 
from setuppvfs import *
from settingmanager import *
from pvfsinput import *
from pvfsdestruction import *


#simple script wrapper for dealing with pvfs volumes
def mainfunc():
    "A simple script for managing pvfs volumes"
    if os.getuid() != 0:
        print "You must be root to run this script"
        sys.exit()
    #read/create the setup data
    setting = SettingManager(1)
    inputc = PVFSInput()
    setup = SetupPVFS()
    end = 1
    while end:
        print """ What would you like to do:
                  0.  Exit.
                  1.  Destroy pvfs all nodes.
                  2.  Create Volumes.
                  Enter your choice: """
        try:
            end = int(raw_input(""))
        except Exception:
            print "Please try to enter only numbers betwee 0 and 2"
            end = 3
        if end == 1:
            PVFSDestroy(setting.getNList())
        elif end == 2:
            inputc.getInput(setting.getNList())  #get the volume info
            for x in inputc.getList():
                setup.setupVolume(x)
    print "Bye!"
    sys.exit()

mainfunc()
            
    
