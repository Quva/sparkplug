
from collections import OrderedDict

class Tag(object):

    def __init__(self, name=None, type=None, isOptional=False):
        
        self.name = name
        self.type = type
        self.isOptional = isOptional

class TagInfo(object):

    numberType = (int, long, float)
    stringType = basestring
    objectType = (dict, OrderedDict)
    listType   = list
    boolType   = bool
    noneType   = type(None)

    def __init__(self):
        
        self.__tagByName = dict([

                ("message_header", Tag(type=self.objectType, isOptional=False)),
                ("message_type", Tag(type=self.stringType, isOptional=False)),
                ("message_id", Tag(type=self.stringType, isOptional=False)),
                ("message_sender_id", Tag(type=self.stringType, isOptional=False)),
                ("message_recipient_id", Tag(type=self.stringType, isOptional=False)),
                ("message_reply", Tag(type=self.objectType, isOptional=False)),
                ("message_body", Tag(type=self.objectType, isOptional=False)),
                
                ("event", Tag(type=self.objectType, isOptional=False)),
                ("event_id", Tag(type=self.stringType, isOptional=False)),
                ("event_type", Tag(type=self.stringType, isOptional=False)),
                ("event_start_time", Tag(type=self.stringType, isOptional=False)),
                ("event_stop_time", Tag(type=self.stringType, isOptional=False)),
                ("event_properties", Tag(type=self.objectType, isOptional=True)),
                ("event_links_to", Tag(type=self.listType, isOptional=True)),

                ("measurements", Tag(type=self.listType, isOptional=False)),
                ("measurement_time", Tag(type=self.stringType, isOptional=False)),
                ("measurement_quality", Tag(type=self.numberType, isOptional=True)),
                ("measurement_num_value", Tag(type=self.numberType, isOptional=True)),
                ("measurement_txt_value", Tag(type=self.stringType, isOptional=True)),
                ("measurement_properties", Tag(type=self.objectType, isOptional=True)),

                ("variables", Tag(type=self.listType, isOptional=False)),
                ("variable_name", Tag(type=self.stringType, isOptional=False)),
                ("variable_source_id", Tag(type=self.stringType, isOptional=False)),
                ("variable_is_txt", Tag(type=self.boolType, isOptional=True)),
                ("variable_unit", Tag(type=self.stringType, isOptional=True)),
                ("variable_description", Tag(type=self.stringType, isOptional=True)),
                ("variable_properties", Tag(type=self.objectType, isOptional=True)),

                ("request_analysis", Tag(type=self.boolType, isOptional=True)),
                ("analysis", Tag(type=self.objectType, isOptional=False)),
                ("analysis_properties", Tag(type=self.objectType, isOptional=False)),
                ("days_back", Tag(type=self.stringType, isOptional=False)),
                ("event_property_similarity_key", Tag(type=self.stringType, isOptional=False))

                ])
        
        
    def getTag(self, name):
        return self.__tagByName[name]

    def keys(self):
        return self.__tagByName.keys()
