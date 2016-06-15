#This is a simple class for managing pvfstab entries
#It will create the file if it does not exist and
#if it does then will append manager entries to the pvfstab
#by Chris Bilderback

#for file editing
import commands
import string
import os

class PvfsTabManager:
    "Manages the pvfstab on a system."
    
    #class constructor does nothing but checks to
    #see that the user has proper uid to run this
    def __init__(self):
        if os.getuid() != 0:
            raise Exception("You must be root to edit pvfstab")
        self.__fp = 0   #set the file pointer to 0
    
    #this function clears the pvfstab on a system
    def clearTab(self):
        self.__fp = open('/etc/pvfstab', 'w')
        self.__fp.close()
        del self.__fp
        self.__fp = 0
    
    #this function is called to add a pvfs mgr to the
    #system's pvfstab
    def addMGR(self, mgrName, metaDir, mountDir):
        "Adds a manager to the systems pvfstab"
        #check to see if the file exists
        if os.access('/etc/pvfstab', os.F_OK) != 1:
            self.__fp = open('/etc/pvfstab', 'w')
            self.__writeTab(mgrName, metaDir, mountDir)
            self.__fp.close()
            del self.__fp
            self.__fp = 0
        else:
            if self.__parseTab(mgrName) == 0:
                #it was not in the tab
                self.__fp = open('/etc/pvfstab', 'a')
                self.__writeTab(mgrName, metaDir, mountDir)
                self.__fp.close()
                del self.__fp
                self.__fp = 0
            else:
                #it was in the tab
                self.__replace(mgrName, metaDir, mountDir)
    
    #PRIVATE:
    #This "private" function just writes the line in the tab
    def __writeTab(self, mgrName, metaDir, mountDir):
        templine  = mgrName + ":" + metaDir + " " + mountDir
        templine2 = " pvfs port=3000 0 0\n"
        self.__fp.write(templine + templine2)
    
    #This function parses the tab (calls grep) to see if the
    #mgr is in the tab
    #it has been assumed that you have checked for existance
    #before calling this
    def __parseTab(self, mgrName):
        output = commands.getoutput("grep " + mgrName + " /etc/pvfstab")
        if len(output) == 0:
            return 0
        else:
            return 1
    
    #This function replaces a entry in the pvfs tab with
    #a given mgr
    def __replace(self, mgrName, metaDir, mountDir):
        self.__fp = open('/etc/pvfstab', 'r')     #open for reading
        tlist = self.__fp.readlines()             #read all the lines into list
        self.__fp.close()
        del self.__fp
        self.__fp = open('/etc/pvfstab', 'w')     #open and truncate
        for x in tlist:
            if string.find(x, mgrName) == -1:
                #it is not here so write the line
                self.__fp.write(x)
            else:
                self.__writeTab(mgrName, metaDir, mountDir)
        self.__fp.close()
        del self.__fp
        self.__fp = 0
