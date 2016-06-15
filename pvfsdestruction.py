#Simple function for destorying pvfs on a set of all nodes.

import sys
import string
import commands


def PVFSDestroy(NodeInfos):
    """ PVFSDestroy(NodeInfos)
        A function to destroy pvfs on nodes
        NodeInfos is a list of nodeinfo structs """
    for x in NodeInfos:
        cmd = x.methodOf + " " + x.nodeName + " " + x.pathTo + "killpvfs.py"
        print "Executing " + cmd
        result = commands.getoutput(cmd)
        if len(result) != 0:
            print "Error destroying pvfs: " + result
            sys.exit()
    print "Destruction completed"
