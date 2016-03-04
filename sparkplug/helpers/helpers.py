
import sys

def dictContains(D, key):
    
    if sys.version_info[0] == 2:
        return D.has_key(key)
    
    elif sys.version_info[0] == 3:
        return key in D
    
    else:
        raise Exception("No support for self.__dictContains for python major " +
                        "version: {}".format(sys.version_info[0]))
    
