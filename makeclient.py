#! /usr/bin/env python

#simple script to set up the iod node
import commands
import string
import os
import sys

#lifted from killpvfs.py
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

#function to start the client
def setupClient(hostname, metadir, mountdir, scriptdir):
    'Function to start the pvsf client'
    try:
        #assume that it is the current working dir
        try:
            sys.path.append(scriptdir)
            import pvfstabmanager
        except ImportError:
            print "Error: could not locate pvfstabmanager module"
            sys.exit()
        
        #create the manager
        mang = pvfstabmanager.PvfsTabManager()
        mang.addMGR(hostname, metadir, mountdir)

        if len(commands.getoutput('grep pvfs /proc/modules')) == 0:
            result = commands.getoutput('/sbin/insmod pvfs') #insert the module
            if string.find(result, 'Using') == -1:
                print "Error: Unable to load the pvfs module"
                print result
                sys.exit()
            del result
        if findPID('/usr/local/sbin/pvfsd') == -1:
            #deamon not running so start it
            result = commands.getoutput('/usr/local/sbin/pvfsd')
            if len(result):
                print "Error: Unable to start the pvfsd daemon"
                sys.exit()
            del result
        #mount the pvfs volume
        mountcmd = '/sbin/mount.pvfs '+hostname+':' + metadir+" " + mountdir
        result = commands.getoutput(mountcmd)             #mount the pvfs dir
        if len(result):
            print "Error: Unabled to mount the pvfs volume"
            sys.exit()
    except Exception, e:
        print str(e)
        print "Error: Unable to create client"
        sys.exit()

def mainfun():
    
    if len(sys.argv) < 4:
        print "Usage: " + sys.argv[0]
        print " [mgr node] [metadir] [mountdir] <scriptdir>"
        sys.exit()
    
    if os.getuid() != 0:
        print "Error: You must be root to run this script"
        sys.exit()
    
    #try to import the pvfstab manager
    if len(sys.argv) == 5:
        scriptdir = sys.argv[4]
    else:
        scriptdir = os.getcwd()
    #check the mnt point
    if os.access(sys.argv[3], os.F_OK) != 1:
        os.mkdir(sys.argv[3])
    #check the device
    if os.access('/dev/pvfsd', os.F_OK) != 1:
        result = commands.getoutput('mknod /dev/pvfsd c 60 0')
        if len(result):
            print "Error: could not create mknod pvfsd device"
            sys.exit()
        del result
    
    setupClient(sys.argv[1], sys.argv[2], sys.argv[3], scriptdir) #set up iod


mainfun()
