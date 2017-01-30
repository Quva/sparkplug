# -*- coding: utf-8 -*-

# Quva Oy, 2015
# Contributors: Timo Erkkilä, timo.erkkila@quva.fi

import requests
import bz2
import base64
import json
import sys
import logging

from sparkplug.parsers import xml
from sparkplug.validators import validateMessage
from sparkplug.converters import convertMessageInPlace


def getLogger(loggerName="SparkPlug"):
    
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger


class SparkPlug(object):
  
    def __init__(self,
                 url="http://localhost:8161",
                 username=None,
                 password=None,
                 logger=getLogger()):
        
        # Collect input arguments
        self.url = url
        self.username = username
        self.password = password
        
        # Derive auth for POST
        self.__auth = (self.username, self.password)
        
        # Derive url for POST
        self.__url = url
        
        self.__logger = logger
        

    def __logInfo(self, msg):
        if self.__logger is not None:
            self.__logger.info(msg)
            
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

        self.__logInfo("Converting message, this may take a while")
        convertMessageInPlace(message)
        self.__logInfo("Done converting message!")
        
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
        
    
