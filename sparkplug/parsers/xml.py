
import xmltodict
import copy

from collections import OrderedDict

from sparkplug.helpers import TagInfo

def _convert_elem_inplace(D, key, tagInfo):
    observedType = type(D[key])
    tag = tagInfo.getTag(key)
    expectedType = tag.type
    #print(observedType, key)
    if not isinstance(D[key], expectedType):
        #print("key '{}' of type {} having value '{}' DOES NOT map to proper type {}".format(key,
        #                                                                                    observedType,
        #                                                                                    D[key],
        #                                                                                    expectedType))
        if expectedType == tagInfo.numberType:
            #print(" => Converting to float")
            D[key] = float(D[key])
        elif expectedType == tagInfo.stringType:
            #print(" => Converting to string")
            D[key] = str(D[key])
        elif expectedType == tagInfo.boolType:
            #print(" => Converting to bool")
            if D[key] not in ["true","false"]:
                raise Exception("in order to convert value " +
                                "'{}' to bool it needs to be either 'true' or 'false'".format(key))
            D[key] = (True if D[key] == "true" else False)
            #print(key, D[key])
        elif expectedType == tagInfo.listType:
            # Fallback of list is string
            #print(" => Converting to list of one")
            D[key] = list(D[key])
        else:
            raise Exception("Conversion rule for type {} for key {} does not exist!".format(expectedType,
                                                                                            key))
    #else:
        #print("key '{}' maps to proper type {}".format(key, type(D[key])))

def _convert_dict_inplace_recursively(D, tagInfo):

    keys = copy.deepcopy(list(D.keys()))

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
                
                

def loads(s):

    tagInfo = TagInfo()

    message = xmltodict.parse(s)
    
    message = message["message"]

    _convert_dict_inplace_recursively(message, tagInfo)
    
    return message

    
def load(f):    
    return loads(f.read())

    
