
import xmltodict
import copy

from collections import OrderedDict

from sparkplug.helpers import TagInfo
from sparkplug.helpers import MessageFactory            

def _convert_elem_inplace(D, key, tagInfo):
    observedType = type(D[key])
    expectedType = tagInfo.getTag(key).type
    if not isinstance(D[key], expectedType):
        #print("key '{}' of type {} DOES NOT map to proper type {}".format(key, observedType, expectedType))
        #print("Attempting conversion...")
        if expectedType == tagInfo.numberType:
            D[key] = float(D[key])
        elif expectedType == tagInfo.stringType:
            D[key] = str(D[key])
        elif expectedType == tagInfo.boolType:
            if D[key] not in ["true","false"]:
                raise Exception("in order to convert value " +
                                "'{}' to bool it needs to be either 'true' or 'false'".format(key))
            D[key] = (True if D[key] == "true" else False)
        else:
            raise Exception("Conversion rule for type {} does not exist!".format(expectedType))
    #else:
        #print("key '{}' maps to proper type {}".format(key, type(D[key])))

def _convert_dict_inplace_recursively(D, tagInfo):
    
    keys = copy.deepcopy(D.keys())

    for key in keys:

        if key.startswith("@"):
            del D[key]
            continue

        if key not in tagInfo.keys():
            #print("Key '{}' is unknown".format(key))
            continue

        _convert_elem_inplace(D, key, tagInfo)

        if isinstance(D[key], TagInfo.objectType):
            _convert_dict_inplace_recursively(D[key], tagInfo)

        if isinstance(D[key], tagInfo.listType):
            for elem in D[key]:
                if isinstance(elem, tagInfo.objectType):
                    _convert_dict_inplace_recursively(elem, tagInfo)
                
                


def load(fileName):
    
    f = open(fileName, 'r')
    
    tagInfo = TagInfo()
    
    message = xmltodict.parse(f.read())
    
    message = message["message"]

    #keys = copy.deepcopy(header.keys())

    #for key in keys:
    #    if key.startswith("@"):
    #        del header[key]
        
    _convert_dict_inplace_recursively(message, tagInfo)

    f.close()

    return message

    
