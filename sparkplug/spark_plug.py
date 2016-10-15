# -*- coding: utf-8 -*-

# Quva Oy, 2015
# Contributors: Timo Erkkilä, timo.erkkila@quva.fi

import requests
import bz2
import base64
import json
from sparkplug.parsers import xml

from sparkplug.validators import validateMessage
from sparkplug.converters import convertMessageInPlace

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

    def loadJSON(self, fileName, doValidate=False):
        return self.__load(json.load, open(fileName, "r"), doValidate=doValidate)

    def loadXML(self, fileName, doValidate=False):
        return self.__load(xml.load, open(fileName, "r"), doValidate=doValidate)

    def loadJSONString(self, payload, doValidate=False):
        return self.__load(json.loads, payload, doValidate=doValidate)
        
    def loadXMLString(self, payload, doValidate=False):
        return self.__load(xml.loads, payload, doValidate=doValidate)
        
    def __load(self, load_f, loadable, doValidate=False):
        
        message = load_f(loadable)
        
        convertMessageInPlace(message)
        
        if doValidate:
            self.validate(message)
            
        return message
        
    def validate(self, message):
        self.post(message, isDryrun=True)

        
    def post(self, message, isDryrun=False, skipValidation=False, compress=False):
        
        if not skipValidation:
            validateMessage(message)
            
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
        
        
