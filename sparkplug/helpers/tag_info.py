
from collections import OrderedDict
import sys
from .helpers import dictContains

class Tag(object):

    def __init__(self, name=None, type=None, isOptional=False):
        
        self.name = name
        self.type = type
        self.isOptional = isOptional

    def __str__(self):
        return "Tag(name={},type={},isOptional={})".format(self.name, self.type, self.isOptional)

class TagInfo(object):

    __pyMajorVersion = sys.version_info[0]

    if __pyMajorVersion == 2:

        numberType = (int, long, float)
        stringType = basestring
        objectType = (dict, OrderedDict)
        listType   = list
        boolType   = bool
        noneType   = type(None)
        
    elif __pyMajorVersion >= 3:

        numberType = (int, float)
        stringType = str
        objectType = (dict, OrderedDict)
        listType   = list
        boolType   = bool
        noneType   = type(None)
    

    def __init__(self):
        
        
        
        self.__tagByName = dict([
            
            ("message_header", Tag(type=self.objectType, isOptional=False)),
            ("message_type", Tag(type=self.stringType, isOptional=False)),
            ("message_id", Tag(type=self.stringType, isOptional=True)),
            ("message_sender_id", Tag(type=self.stringType, isOptional=False)),
            ("message_recipient_id", Tag(type=self.stringType, isOptional=False)),
            ("message_reply", Tag(type=self.objectType, isOptional=True)),
            ("message_version", Tag(type=self.stringType, isOptional=True)),
            
            ("message_body", Tag(type=self.objectType, isOptional=False)),

            ("event", Tag(type=self.objectType, isOptional=True)),
            ("event_id", Tag(type=self.stringType, isOptional=False)),
            ("event_type", Tag(type=self.stringType, isOptional=False)),
            ("event_start_time", Tag(type=self.stringType, isOptional=True)),
            ("event_stop_time", Tag(type=self.stringType, isOptional=True)),
            ("event_properties", Tag(type=self.objectType, isOptional=True)),
            
            ("measurements", Tag(type=self.listType, isOptional=False)),
            ("measurement_time", Tag(type=self.stringType, isOptional=False)),
            ("measurement_num_value", Tag(type=self.numberType, isOptional=True)),
            ("measurement_txt_value", Tag(type=self.stringType, isOptional=True)),
            ("measurement_properties", Tag(type=self.objectType, isOptional=True)),
            
            ("variables", Tag(type=self.listType, isOptional=False)),
            ("variable_name", Tag(type=self.stringType, isOptional=False)),
            ("variable_name_alias", Tag(type=self.stringType, isOptional=True)),
            ("variable_source_id", Tag(type=self.stringType, isOptional=False)),
            ("variable_is_txt", Tag(type=self.boolType, isOptional=True)),
            ("variable_unit", Tag(type=self.stringType, isOptional=True)),
            ("variable_description", Tag(type=self.stringType, isOptional=True)),
            ("variable_description_alias", Tag(type=self.stringType, isOptional=True)),
            ("variable_properties", Tag(type=self.objectType, isOptional=True)),
            
            ("request_analysis", Tag(type=self.boolType, isOptional=True)),
            ("analysis", Tag(type=self.objectType, isOptional=False)),
            ("analysis_properties", Tag(type=self.objectType, isOptional=False)),
            ("days_back", Tag(type=self.stringType, isOptional=False)),
            ("event_property_similarity_key", Tag(type=self.stringType, isOptional=False)),
            
            ("keyspace", Tag(type=self.stringType, isOptional=False)),
            ("event_id", Tag(type=self.stringType, isOptional=False))
            
        ])

        
        
        
    def getTag(self, name):
        
        if not dictContains(self.__tagByName, name):
            raise Exception("TagInfo does not have type information for key '{}'".format(name))
        
        return self.__tagByName[name]

    def keys(self):
        return self.__tagByName.keys()

    def __str__(self):
        return str(self.__tagByName)
