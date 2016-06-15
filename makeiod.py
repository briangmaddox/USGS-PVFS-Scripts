#! /usr/bin/env python

#simple script to set up the iod node
import commands
import os
import pwd
import sys


#function to create the data dir and write the iod.conf
def setIODDir(datadir):
    "Function to create the datadirectory (if it does not exist)"
    if os.access(datadir, os.F_OK) != 1:
        os.mkdir(datadir)        #create it
        os.chmod(datadir, 0700)
        try:
            tement = pwd.getpwnam('nobody')
            os.chown(datadir, tement[2], tement[3])
            del tement
        except KeyError:
            print "Error: User nobody is not on system (bad)."
            sys.exit()
    #write the pvfs table
    fp = open('/etc/iod.conf', 'w')
    fp.write('datadir ' + datadir + '\n')
    fp.write('user nobody\ngroup nobody\n')
    fp.close()

#function to 
def mainfun():
    if len(sys.argv) < 2:
        print "Usage: "+ sys.argv[0]+" [data-dir]"
        sys.exit()

    if os.getuid() != 0:
        print "Error: You must be root to run this script"
        sys.exit()
    setIODDir(sys.argv[1])   #set up the data dir
    #start the manager
    out = commands.getoutput('/usr/local/sbin/iod')
    if len(out):
        print "Error: unable to start the iod daemon"

#call the main function
mainfun()

