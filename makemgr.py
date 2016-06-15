#! /usr/bin/env python

#simple script to write the pvfs meta data directory

import commands
import string
import os
import sys

#Function to create the .pvfsdir file.
def writePVFSDir(pvfsdir):
    'Function to write the .pvfsdir file'
    if os.access(pvfsdir + '/.pvfsdir', os.F_OK) != 1: #check existance
        out = open(pvfsdir + '/.pvfsdir', 'w')         #create it
        out.close()                                    #close it
        del out                                        #done with out for now
    pvfdirstat = os.stat(pvfsdir + '/.pvfsdir')        #get the stat for inode
    out = open(pvfsdir + '/.pvfsdir', 'w')             #open the file
    out.write(str(pvfdirstat[1]) + '\n')               #write the inode
    out.write('0\n0\n0040777\n3000\n')                 #other goop (ownership)
    hostn = commands.getoutput('hostname -s')
    out.write(hostn + '\n')
    out.write(pvfsdir + '\n')
    out.write('/\n')
    out.close()                                   #done

#Function to create the .iodtab
def writeIODtab(pvfsdir, iodlist):
    'Function to create the .iodtab'
    out = open(pvfsdir + '/.iodtab', 'w')
    for x in iodlist:
        out.write(x + ":7000\n")
    out.close()


#Main body of the script
def mainfun():
    if len(sys.argv) < 3:
        print "Usage: " + sys.argv[0] + " [meta-dir] [iodnodes]"
        sys.exit()
    
    #check for root
    if os.getuid() != 0:
        print "Error: You must be root to run this script!"
        sys.exit();
    
    #ok get the info
    pvfsdir = sys.argv[1]
    iodlist = sys.argv[2:]

    if os.access(pvfsdir, os.F_OK) != 1: #check existance
        os.mkdir(pvfsdir)                #create the directory
    
    writePVFSDir(pvfsdir)                #write the .pvfsdir file
    writeIODtab(pvfsdir, iodlist)        #write the iod tabl 

    #start the manaager
    out = commands.getoutput('/usr/local/sbin/mgr')
    if len(out):
        print "Error: could not start manager"

mainfun()  #run the script
