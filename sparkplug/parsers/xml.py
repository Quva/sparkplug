
import xmltodict
import copy

from collections import OrderedDict

from sparkplug.helpers import TagInfo

def _convert_elem_inplace(D, key, tagInfo):
    observedType = type(D[key])
    tag = tagInfo.getTag(key)
    expectedType = tag.type
    #print(observedType, key)

    valueOnError = None

    if not isinstance(D[key], expectedType):
        #print("key '{}' of type {} having value '{}' DOES NOT map to proper type {}".format(key,
        #                                                                                    observedType,
        #                                                                                    D[key],
        #                                                                                    expectedType))
        if expectedType == tagInfo.numberType:
            #print(" => Converting to float")
            try:
                D[key] = float(D[key])
            except:
                D[key] = valueOnError
        elif expectedType == tagInfo.stringType:
            #print(" => Converting to string")
            try:
                D[key] = str(D[key])
            except:
                D[key] = valueOnError
        elif expectedType == tagInfo.boolType:
            #print(" => Converting to bool")
            if D[key] not in ["true","false"]:
                raise Exception("in order to convert value " +
                                "'{}' to bool it needs to be either 'true' or 'false'".format(key))
            try:
                D[key] = (True if D[key] == "true" else False)
            except:
                D[key] = valueOnError
                #print(key, D[key])
        elif expectedType == tagInfo.listType:
            # Fallback of list is string
            #print(" => Converting to list of one")
            try:
                D[key] = [D[key]]
            except:
                D[key] = valueOnError
        else:
            raise Exception("Conversion rule for type {} for key {} does not exist!".format(expectedType,
                                                                                            key))

        
    # Properties objects should contain only key-value pairs of strings
    if key in ["event_properties", "measurement_properties", "variable_properties"]:
        D[key] = dict(filter(lambda t: isinstance(t[1], str) or isinstance(t[1], basestring), D[key].items()))

        
def _convert_dict_inplace_recursively(D, tagInfo):

    keys = copy.deepcopy(list(D.keys()))
    #print(keys)
    
    for key in keys:

        if key.startswith("@"):
            #print("Found key that starts with @: '{}' -> '{}'. Deleting...".format(key, D[key]))
            del D[key]
            continue

        if key not in tagInfo.keys():
            #print("Key '{}' is unknown".format(key))
            continue

        _convert_elem_inplace(D, key, tagInfo)

        if isinstance(D[key], TagInfo.objectType):
            #print("Key '{}' maps to an object".format(key))
            _convert_dict_inplace_recursively(D[key], tagInfo)

        if isinstance(D[key], tagInfo.listType):
            for elem in D[key]:
                if isinstance(elem, tagInfo.objectType):
                    _convert_dict_inplace_recursively(elem, tagInfo)
                
                

def loads(s):

    tagInfo = TagInfo()

    message = xmltodict.parse(s)
    
    message = message["message"]

    #print(message)
    
    _convert_dict_inplace_recursively(message, tagInfo)
    
    return message

    
def load(f):    
    return loads(f.read())

    
