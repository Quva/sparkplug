# -*- coding: utf-8 -*-

# Quva Oy, 2015
# Contributors: Timo Erkkilä, timo.erkkila@quva.fi


import requests
import bz2
import base64

from sparkplug.validators import validate, Schemas

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
        

    def __check(self, message, schema):
        
        res, errors = validate(message, schema)
        
        if res != True:
            raise Exception(str(errors))
            

    def validate(self, message):
        self.post(message, isDryrun=True)

        
    def post(self, message, isDryrun=False, compress=False, skipCheck=False):

        if skipCheck:
            print("WARNING: message checking disabled!")
        else:
            self.__check(message, Schemas.messageSchema)
        
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
            self.__check(message, Schemas.eventMessageSchema)
            

        response = self.__post(message, isDryrun=isDryrun, compress=compress)
        
        return response

    def __postVariables(self, message, isDryrun=False, compress=False, skipCheck=False):

        # Check that measurements json is valid
        if skipCheck:
            pass
        else:
            self.__check(message, Schemas.variablesMessageSchema)

        response = self.__post(message, isDryrun=isDryrun, compress=compress)

        return response

    def __postAnalysisRequest(self, message, isDryrun=False, compress=False, skipCheck=False):
        
        if skipCheck:
            pass
        else:
            self.__check(message, Schemas.analysisRequestMessageSchema)

        response = self.__post(message, isDryrun=isDryrun, compress=compress)

        return response

    def __postEventUpdateNotification(self, message, isDryrun=False, compress=False, skipCheck=False):

        if skipCheck:
            pass
        else:
            self.__check(message, Schemas.eventUpdateNotificationMessageSchema)
            
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
        
        
