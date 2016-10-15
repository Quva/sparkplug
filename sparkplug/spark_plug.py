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

        
    def load(self, fileName):
        if fileName.lower().endswith("json"):
            message = self.loadJSON(fileName)
        elif fileName.lower().endswith("xml"):
            message = self.loadXML(fileName)

        return message
            
            
    def loadJSON(self, fileName):
        return self.__load(json.load, open(fileName, "r"))

    def loadXML(self, fileName):
        return self.__load(xml.load, open(fileName, "r"))

    def loadJSONString(self, payload):
        return self.__load(json.loads, payload)
        
    def loadXMLString(self, payload):
        return self.__load(xml.loads, payload)
        
    def __load(self, load_f, loadable):
        
        message = load_f(loadable)
        
        convertMessageInPlace(message)
        
        return message

    
    def validate(self, message):
        validateMessage(message)
        
    def compressInPlace(self, message):
        body = message['message_body']
        message['message_body'] = base64.b64encode(bz2.compress(message['message_body']))
        
    def post(self, message):

        import warnings
        warnings.filterwarnings("ignore")
            
        response = requests.post(self.__url,
                                 json=message,
                                 auth=self.__auth,
                                 verify=False)
        
        return response
        
    
