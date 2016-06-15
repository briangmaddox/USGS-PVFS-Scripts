#A base class to get pvfs volumes for input
#The base class just uses menu console stuff

import os
import commands
import string
import pvfsvolume

class PVFSInput:
    """ Base class to get pvfs volume info. 
    Overload it get input your own way. """
    
    #main constructor for the class inits the list
    def __init__(self):
        self.plist = []
    
    #function to return the input list
    def getList(self):
        "function to return the interal list of volumes"
        return self.plist
    
    #function to get input from the user and
    #return a list of pvfs volumes to be setup
    #(the list is also stored interally)
    def getInput(self, nodeList):
        "function gets input from user. nodeList is a list of availble nodes"
        #check the nodelist
        if len(nodeList) == 0:
            raise Exception("PVFSInput::getInput nodelist invalid")
        
        #try it the simple way
        nvols = 0
        while not nvols:
            try:
                nvols =int(raw_input("Enter the # of volumes to create: "))
                if nvols <= 0:
                    print "What kind of answer is that! Good job smarticus"
            except Exception:
                print "You would think that # indicates to enter a NUMBER!"
        
        #loop through and build the list
        while nvols:
            mgrix = -1
            while mgrix == -1:
                try:
                    self.printList(nodeList)   # print the list
                    mgrix=int(raw_input("Please pick a index for mgr node: "))
                    if mgrix < 0 or mgrix >= len(nodeList):
                        print "Choose a valid INDEX!"
                        mgrix = -1
                    elif not self.checkMGR(nodeList[mgrix].nodeName):
                        print "MGR was already chosen before"
                except Exception, e:
                    print "Index means number! " + str(e)
            
            #ok get the iods
            iodixs = []
            while not len(iodixs):
                try:
                    self.printList(nodeList)     #print the list
                    tempstring=raw_input("Enter (space delimit) iods indexs: ")
                    tokens = string.split(tempstring)
                    if not len(tokens):
                        print "Look you are making this hard."
                    else:
                        for x in tokens:
                            try:
                                iodixs.append(int(x))
                            except Exception:
                                print "Ignoring " + x
                        if not len(tokens):
                            print "This program was tested by trained monkeys"
                        else:
                            #check the iods
                            truth = 1
                            for x in iodixs:
                                if not self.checkIOD(nodeList[x].nodeName):
                                    truth = 0
                            if not truth:
                                print "Some iods have been used before!"
                                iodixs = []
                except Exception, e:
                    print "Typing is a real world skill " + str(e)
            
            #get the clients
            print "Assuming you want all nodes to be clients of each volume"
            self.plist.append(pvfsvolume.PVFSVolume());
            self.plist[len(self.plist)-1].mgr = nodeList[mgrix]
            for x in iodixs:
                self.plist[len(self.plist)-1].iods.append(nodeList[x])
            for x in nodeList:
                self.plist[len(self.plist)-1].clients.append(x)
            nvols = nvols -1
        #close the nvols while
        return self.plist
    
    
    #function to print the list of nodes availible in the system
    def printList(self, nodeList):
        "Function to print the list of nodes"
        rng = range(len(nodeList))
        for x in rng:
            print str(x) + ". " + nodeList[x].nodeName
    
    #function to check to see if the mgr node has been use before
    def checkMGR(self, mgrname):
        "Function to see if a mgr node has been used before"
        for x in self.plist:
            if x.mgr == mgrname:
                return 0
        return 1
    
    #function to check a iod
    def checkIOD(self, iodname):
        "Function to see if a iod node has been used before"
        for x in self.plist:
            for y in x.iods:
                if y == iodname:
                    return 0
        return 1
