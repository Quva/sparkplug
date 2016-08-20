# -*- coding: utf-8 -*-

# Quva Oy, 2015
# Contributors: Timo Erkkilä, timo.erkkila@quva.fi


import requests
import bz2
import base64

from sparkplug.helpers import TagInfo, dictContains

class SparkPlug(object):
  
    def __init__(self,
                 url="http://localhost:8161",
                 username=None,
                 password=None):

        # Collect input arguments
        self.url = url
        self.username = username
        self.password = password

        # Derive auth for POST
        self.__auth = (self.username, self.password)

        # Derive url for POST
        self.__url = url

        self.__tagInfo = TagInfo()
        
    def __checkMessage(self, message):

        if not isinstance(message, TagInfo.objectType):
            raise Exception("message needs to be of " +
                            "type {}, but found {} instead".format(TagInfo.objectType,
                                                                   type(message)))

        self.__checkFields(message, "message",
                           ["message_header",
                            "message_body"])
        
        header = message["message_header"]

        self.__checkFields(header, "message_header",
                           ["message_type",
                            "message_sender_id",
                            "message_recipient_id",
                            "message_id",
                            "message_reply"])

    def __checkEvent(self, message):

        body = message['message_body']
        
        # Event message body needs to have event and measurements fields
        self.__checkFields(body, "message_body", 
                           ["event",
                            "measurements",
                            "request_analysis"])

        measurements = body["measurements"]
        
        if "event" in body:
            event = body["event"]
            
            self.__checkFields(event, "event",
                               ["event_id",
                                "event_type",
                                "event_start_time",
                                "event_stop_time",
                                "event_properties",
                                "event_links_to"])
    

            # If event properties are present, check them
            if dictContains(event, "event_properties"):
                event_properties = event["event_properties"]
            
                self.__checkProperties(event_properties, "event_properties")
                
        for measurementIdx, measurement in enumerate(measurements):
            
            self.__checkFields(measurement, "measurement", 
                               ["variable_name",
                                "variable_source_id",
                                "measurement_time",
                                "measurement_quality",
                                "measurement_num_value",
                                "measurement_txt_value",
                                "measurement_properties"])

            if not (dictContains(measurement, "measurement_num_value") ^
                    dictContains(measurement, "measurement_txt_value")):
                
                raise Exception("Measurement " +
                                "has to contain either " +
                                "'measurement_txt_value' or 'measurement_num_value': " +
                                "{}".format(measurement))
                
    def __checkVariables(self, message):
        
        body = message['message_body']
        
        self.__checkField(body, "message_body", "variables")
        
        variables = body["variables"]
        
        for variable in variables:

            self.__checkFields(variable, "variable", 
                               ["variable_source_id",
                                "variable_name",
                                "variable_is_txt",
                                "variable_unit",
                                "variable_description",
                                "variable_properties"])
            
            if dictContains(variable, "variable_properties"):
                variable_properties = variable["variable_properties"]
                self.__checkProperties(variable_properties, "variable_properties")

    def __checkAnalysisRequest(self, message):

        body = message["message_body"]

        self.__checkField(body, "message_body", "analysis")

        analysis = body["analysis"]

        self.__checkField(analysis, "analysis", "analysis_properties")

        analysis_properties = analysis["analysis_properties"]

        self.__checkFields(analysis_properties, "analysis_properties", 
                           ["event_id",
                            "event_type",
                            "days_back",
                            "event_property_similarity_key"])

    def __checkEventUpdateNotification(self, message):

        body = message["message_body"]
        
        self.__checkFields(body, "message_body", ["keyspace", "event_id"])
        
    def __checkFields(self, message, messageName, expectedFields):

        # Check that exactly the expected keys are present and nothing more
        for observedField in message.keys():
            if observedField not in expectedFields:
                raise Exception("{}['{}'] ".format(messageName, observedField) + 
                                "not expected!")

        for expectedField in expectedFields:
            self.__checkField(message, messageName, expectedField) 

    def __checkField(self, message, messageName, fieldName):
        
        tag = self.__tagInfo.getTag(fieldName)

        if tag.isOptional: 
            if (dictContains(message, fieldName) and 
                not (isinstance(message[fieldName], tag.type) or 
                     isinstance(message[fieldName], TagInfo.noneType))):
                
                raise Exception("{}['{}'] needs to be a of ".format(messageName, fieldName) +
                                "type {}, but {} found".format(tag.type,
                                                               type(message[fieldName])))
            
        else:
            
            if not dictContains(message, fieldName):
                raise Exception("{} is missing field '{}': {}"\
                                    .format(messageName, fieldName, message.keys()))

            if not isinstance(message[fieldName], tag.type):
                raise Exception("{}['{}'] needs to be a of ".format(messageName, fieldName) +
                                "type {}, but {} found".format(tag.type,
                                                               type(message[fieldName])))

    def __checkProperties(self, properties, propName):

        # Check that every property maps to a string
        for fieldName in properties.keys():
            self.__checkProperty(properties, propName, fieldName)
            

    def __checkProperty(self, properties, propName, fieldName):
        
        if not isinstance(properties[fieldName], TagInfo.stringType):
            raise Exception("Property {}['{}'] needs to be a of ".format(propName, fieldName) +
                            "type {}, but {} found".format(TagInfo.stringType,
                                                           type(properties[fieldName])))

    def validate(self, message):
        self.post(message, isDryrun=True)
        
    def post(self, message, isDryrun=False, compress=False, skipCheck=False):

        if skipCheck:
            print("WARNING: message checking disabled!")
        else:
            self.__checkMessage(message)
        
        header = message["message_header"]

        if header["message_type"] in ["event", "event-update"]:
            response = self.__postEvent(message, isDryrun=isDryrun, compress=compress, skipCheck=skipCheck)

        elif header["message_type"] == "variables":
            response = self.__postVariables(message, isDryrun=isDryrun, compress=compress, skipCheck=skipCheck)

        elif header["message_type"] == "analysis-request-event":
            response = self.__postAnalysisRequest(message, isDryrun, compress=compress, skipCheck=skipCheck)

        elif header["message_type"] == "event-update-notification":
            response = self.__postEventUpdateNotification(message, isDryrun, compress=compress, 
                                                          skipCheck=skipCheck)

        else:
            raise Exception("Wrong message_type " +
                            "({})".format(header["message_type"]))

        return response

    def __postEvent(self, message, isDryrun=False, compress=False, skipCheck=False):

        # Check that measurements json is valid
        if skipCheck:
            pass
        else:
            self.__checkEvent(message)
            

        response = self.__post(message, isDryrun=isDryrun, compress=compress)
        
        return response

    def __postVariables(self, message, isDryrun=False, compress=False, skipCheck=False):

        # Check that measurements json is valid
        if skipCheck:
            pass
        else:
            self.__checkVariables(message)

        response = self.__post(message, isDryrun=isDryrun, compress=compress)

        return response

    def __postAnalysisRequest(self, message, isDryrun=False, compress=False, skipCheck=False):
        
        if skipCheck:
            pass
        else:
            self.__checkAnalysisRequest(message)

        response = self.__post(message, isDryrun=isDryrun, compress=compress)

        return response

    def __postEventUpdateNotification(self, message, isDryrun=False, compress=False, skipCheck=False):

        if skipCheck:
            pass
        else:
            self.__checkEventUpdateNotification(message)

        response = self.__post(message, isDryrun=isDryrun, compress=compress)

        return response

    def __post(self, message, isDryrun=False, compress=False):

        if not isDryrun:

            import warnings
            warnings.filterwarnings("ignore")
            
            if compress:
                self.__compress(message)

            response = requests.post(self.__url,
                                     json=message,
                                     auth=self.__auth,
                                     verify=False)

        else:

            response = "Validation passed"

        return response


    def __compress(self, message):
        
        body = message['message_body']
        
        message['message_body'] = base64.b64encode(bz2.compress(message['message_body']))
        
        
