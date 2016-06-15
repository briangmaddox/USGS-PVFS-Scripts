#! /usr/bin/env python

import commands
import string
import os
import sys
import time

#function to find a pid for a command
def findPID(strcommand):                     #finds the pid of command
    'function to find a commands pid'
    foundindex = -1
    psgrep = 'ps -auwx | grep ' + strcommand #get the command
    psout = commands.getoutput(psgrep)       #grep for the command
    tokens = string.split(psout)             #split into tokens
    tokrang = range(len(tokens))             #get the number of tokens
    for x in tokrang:                        #Loop through and find the pid
        if tokens[x] == strcommand:
            if tokens[x-1] != 'grep':        #could be the one for grep though
                foundindex = x
                break
    if foundindex == -1:                     #did we not find it
        return foundindex                    #return error
    else:
        return int(tokens[foundindex-9])

#function to destroy manager stuff
def killMGR(mgrdir):
    'function to kill the mgr node stuff'
    mgrpid = findPID('/usr/local/sbin/mgr')  #find the pid
    if mgrpid != -1:
        os.kill(mgrpid, 9)                   #kill it
    
    if os.access(mgrdir, os.F_OK) == 1:      #look for the mgr dir
        commands.getoutput("rm -rf " + mgrdir)
    commands.getoutput('rm -rf /tmp/mgr*')

#function to destroy iod stuff
def killIOD():
    'function to tkill the iod node stuff'
    iodpid = findPID('/usr/local/sbin/iod')  #find the pid
    if iodpid != -1:
        os.kill(iodpid, 9)
    
    if os.access('/etc/iod.conf', os.F_OK) == 1:
        fp = open('/etc/iod.conf', 'r')      #open it to get the directory
        try:
            #find the data dir
            llist = fp.readlines()
            ioddir = []
            for x in llist:
                if string.find(x, 'datadir') != -1:
                    ioddir = string.split(x)
            if len(ioddir) == 0:
                raise Exception("Error in iod.conf")
            strcom = 'rm -rf ' + ioddir[1]   #build the command
            if len(commands.getoutput(strcom)):
                raise Exception(strcom);
            del strcom
        except Exception, e:
            print "Error: unable to remove iod dir-" + str(e)
        fp.close();
        os.unlink('/etc/iod.conf')           #delete the iodconf
    commands.getoutput('rm -rf /tmp/iolog*')


#function to destroy client info
def killClient():
    "function to destroy client info"
    
    if os.access('/etc/pvfstab', os.F_OK) == 1:
        fp = open('/etc/pvfstab', 'r')
        pvfslines = fp.readlines();                #read the all mounts 
        fp.close()
        for counter in pvfslines:
            tokens = string.split(counter)
            commands.getoutput("/bin/umount " + tokens[1])
            commands.getoutput('rm -rf ' + tokens[1])
            del tokens
        os.unlink('/etc/pvfstab')
    #pvfsd
    pvfsdpid = findPID("/usr/local/sbin/pvfsd")
    if pvfsdpid != -1:                             #check the result
        os.kill(pvfsdpid,9)
    
    #rmmod the modules
    check = commands.getoutput("grep pvfs /proc/modules")
    if len(check):
        result = commands.getoutput("/sbin/rmmod pvfs")
        if len(result):
            print "Error rmmod: " + result
            del result
    
    #rm the device
    if os.access('/dev/pvfsd', os.F_OK) == 1:
        result = commands.getoutput("rm -rf /dev/pvfsd")
        if len(result):
            print "Error dev: " + result
            del result
    #rm the logs
    commands.getoutput('rm -rf /tmp/pvfsdlog*')

    
def stopPVFS():
    'function to stop pvfs'
    if os.getuid() != 0:
        print "Error: You must be root to run this script"
        sys.exit()
    
    mgrdir = '/pvfs-meta'                           #set the default mgrdir
    if len(sys.argv) == 2:
        mgrdir = sys.argv[1]
        if mgrdir[0] != '/':
            print "Error: mgrdir is not full path"
            print "Usage:" + sys.argv[0] + " <mgrdir>"
            sys.exit()
    #try to kill the mgr on this node
    killClient()
    killIOD()
    killMGR(mgrdir)
    sys.exit()

stopPVFS()
