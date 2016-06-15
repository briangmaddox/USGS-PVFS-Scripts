#This is a simple class (and struct) for managing nodes in the
#cluster and paths to which they can get to the
#the pvfs setup scripts.

import os
import commands
import socket
import string

class NodeInfo:
    "A simple structure for defining node info"
    #class constructor
    def __init__(self, nodeName="", pathTo="", methodOf="", needP=0):
        """nodeName = hostname of node
           pathTo = path to setup scripts on hostname
           methodOf = the method (executable) to access (rsh or ssh)
           needP = do we need a password? (not implemented yet)"""
        self.nodeName = nodeName
        self.pathTo = pathTo
        self.methodOf = methodOf
        self.needP = needP



class SettingManager:
    "A manager class for node settings"
    
    #class constructor
    def __init__(self, reParse):
        "reParse is whether to reparse the setting file"
        self.nlist=[]
        if os.access("settings.cfg", os.F_OK) != 1 and reParse:
            self.getInput()         #read the local settings
        elif reParse:
            self.parseSetting()     #parse the existing
       
    
    #This function returns a list of node info for the settings
    def getNList(self):
        "Returns a list of node info structures."
        return self.nlist
    
    #This function reads the settings file and generates a list  
    def parseSetting(self):
        "Reads the settings.cfg file in the local dir"
        counter = 0
        fp = open("settings.cfg", 'r')
        #read the entire file
        templist = fp.readlines()
        fp.close()
        if (len(templist) % 4) != 0 or len(templist) == 0:
            raise Exception("Settings file appears corrupted")
        while counter < len(templist):
            templinelist = string.split(templist[counter]);  
            name = self.__getName(templinelist)                #get the name
            del templinelist
            templinelist = string.split(templist[counter+1])
            pathto = self.__getPath(templinelist)              #get the path
            del templinelist
            templinelist = string.split(templist[counter+2])
            method = self.__getMethod(templinelist)            #get the method
            del templinelist
            templinelist = string.split(templist[counter+3])
            npass = self.__getNpass(templinelist)              #get the pass
            del templinelist
            #put it in the list
            self.nlist.append(NodeInfo(name, pathto, method, npass))
            del name                                           #delete temps
            del pathto
            del method
            del npass
            counter = counter + 4
    
    #This function reads settings from the console and writes the
    #settings file
    def getInput(self):
        "Console input for settings file"
        counter = 0
        numrecs = 0
        while numrecs == 0:
            try:
                numrecs = int(raw_input('Enter the number of hosts: '))
            except (ValueError, EOFError):
                print "Enter a valid number of hosts!"  #just go around again
        del self.nlist   #delete the list
        self.nlist = []
        while counter < numrecs:
            name = self.__InputName()                   #get the name
            pathTo = self.__InputPath()                 #get the path
            method = self.__InputMethod()               #get the method
            npass = self.__InputNpass()                 #get the pass
            self.nlist.append(NodeInfo(name, pathTo, method, npass))
            del name
            del pathTo
            del method
            del npass
            counter = counter + 1
        self.WriteFile()                              #write the file
    
    #PRIVATE
    #this function parses out the name of a host
    def __getName(self, templinelist):
        "Function to parse hostname out of a list"
        if len(templinelist) != 2:
            raise Exception("Hostname string is invalid")
        return templinelist[1]
    
    #this function parses out the path
    def __getPath(self, templinelist):
        "Function to parse path out of a list"
        if len(templinelist) != 2:
            raise Exception("Path string is invalid")
        return templinelist[1]
    
    #This function parses out the method
    def __getMethod(self, templinelist):
        "Function to parse method out of a list"
        if len(templinelist) != 2:
            raise Exception("Path string is invalid")
        return templinelist[1]
    
    #This function parses out the npass
    def __getNpass(self, templinelist):
        "Function to parse npass out of a list"
        if len(templinelist) != 2:
            raise Exception("Path string is invalid")
        try:
            retval = int(templinelist[1])
        except ValueError:
            raise Exception("Npass is invalid in settings file");
        return retval
    
    #This function that asks for the hostname 
    def __InputName(self):
        "Function that asks for user for the hostname of a system"
        flag = 0
        while not flag:
            try:
                hostname = raw_input("Please enter the hostname: ")
                socket.gethostbyname_ex(hostname)
                flag = 1
            except Exception:
                print "Unkown hostname, please try again"
        return hostname
    
    #This function that asks for the path on the host
    def __InputPath(self):
        "Function that asks for the path to scripts on host"
        inputdir = raw_input("Enter path to scripts on host (default cwd): ")
        if len(inputdir) == 0:
            del inputdir
            inputdir = os.getcwd()
        if string.find(inputdir, '/') != len(inputdir)-1:
            inputdir = inputdir + '/'
        return inputdir
    
    #This function asks for the method of accessing the host
    def __InputMethod(self):
        "Function that asks for a method of access to a host"
        method = raw_input("Enter method to access host (default rsh): ")
        if len(method) == 0:
            del method
            method = "rsh"
        return method
    
    #This function asks if a user needs a password to access
    def __InputNpass(self):
        "Not implemented yet"
        return 0
    
    #Function to write the settings file to disk
    def WriteFile(self):
        "Function to write the settings file to disk"
        fp = open("settings.cfg", 'w')
        for counter in self.nlist:        
            fp.write('Name: ' + counter.nodeName + '\n')
            fp.write('PathTo: ' + counter.pathTo + '\n')
            fp.write('Method: ' + counter.methodOf + '\n')
            fp.write('NeedP: ' + str(counter.needP) + '\n')
        fp.close()
