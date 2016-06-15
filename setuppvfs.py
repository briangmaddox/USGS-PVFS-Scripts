

#A setup class that turns volumes structs into acutal volumes. 

import os
import string
import commands

#This class sets a particular volume
class SetupPVFS:
    "PVFS volume setup class"
    #main constructor for the class
    def __init__(self):
        "Main class constructor"
        if os.getuid() != 0:
            raise Exception("You must be root to use this class")
    
    #function to setup a volume given a volume struct
    def setupVolume(self, inputVol):
        """Function to try to setup a volume
        inputVol is a pvfsvolume struct"""
        #setup the mgr
        if not self.setupMgr(inputVol):
            raise Exception("Unable to start mgr " + inputVol.mgr.nodeName)
        #start the iods
        if not self.setupIOD(inputVol):
            raise Exception("Unable to start iods ")
        #start the clients
        if not self.setupClients(inputVol):
            raise Exception("Unable to start clients")
    
    #function to setup the mgrs
    def setupMgr(self, inputVol):
        "Function to start the mgr on a machine"
        method = inputVol.mgr.methodOf
        path  = inputVol.mgr.pathTo
        cmd1 = method + " " + inputVol.mgr.nodeName + " " + path+ "makemgr.py "
        cmd1 = cmd1 + "/pvfs-meta "
        for x in inputVol.iods:
            cmd1 = cmd1 + x.nodeName + " "
        #execute the command
        output = commands.getoutput(cmd1)
        if len(output):
            #error
            return 0
        else:
            return 1
    
    #function to setup the iods
    def setupIOD(self, inputVol):
        "Function to startup iods on each iod machine"
        for x in inputVol.iods:
            method = x.methodOf
            path = x.pathTo
            cmd1 = method + " "+ x.nodeName + " " + path + "makeiod.py "
            cmd1 = cmd1 + "/data/pvfs-data"
            #execute the command
            output = commands.getoutput(cmd1)
            if len(output):
                return 0
        return 1 #all iods supposably started.
    
    #function to setup the clients
    def setupClients(self, inputVol):
        "Function to starup clients on each client"
        for x in inputVol.clients:
            method = x.methodOf
            path = x.pathTo
            cmd1 = method + " " + x.nodeName + " " + path + "makeclient.py "
            cmd1 = cmd1 + inputVol.mgr.nodeName + " /pvfs-meta /mnt/pvfs-"
            cmd1 = cmd1 + inputVol.mgr.nodeName + " " + x.pathTo
            print cmd1
            #execut the command
            output = commands.getoutput(cmd1)
            if len(output):
                print output
                return 0
        return 1 #no errors










