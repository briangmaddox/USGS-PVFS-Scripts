#This is a simple storage class for
#for pvfs volumes


class PVFSVolume:
    "Simple storage struct for pvfs volumes"
    #main constructor for the class
    def __init__(self):
        self.mgr = 0  #set the manager to zero for now
        self.iods = [] #set the iods to a empty list
        self.clients = [] #set the clients to empty list
