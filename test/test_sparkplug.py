
import json
import unittest
from nose.tools import raises

from sparkplug import SparkPlug
from sparkplug.parsers import xml

class SparkPlugTest(unittest.TestCase):

    plug = SparkPlug()

    def test_event_message_v1(self):

        message = json.load(
            open("test/test_event_v1.json", 'r'))

        self.plug.validate(message)

    def test_event_message_v1_xml(self):
        
        message = xml.load(open("test/test_event_v1.xml", "r"))
        
        self.plug.validate(message)
        
    def test_variables_message_v1(self):

        message = json.load(open("test/test_variables_v1.json", 'r'))

        self.plug.validate(message)

    @raises(Exception)
    def test_empty_measurements_v1_raises(self):

        self.plug.validate({})

    @raises(Exception)
    def test_measurements_v1_missing_message_type(self):

        self.plug.validate({"message_apikey": "abc",
                            "message_body": []})

    @raises(Exception)
    def test_message_v1_header_missing_message_sender_id(self):
        
        self.plug.validate("test/test_bad_event_v1.json")
        
    @raises(Exception)
    def test_variables_v1_missing_variables_raises(self):

        message = json.load(
            open("test/test_bad_variables_v1.json", 'r'))

        self.plug.validate(message)

    @raises(Exception)
    def test_variables2_v1_missing_variables_raises(self):

        message = json.load(
            open("test/test_bad_variables2_v1.json", 'r'))
        
        self.plug.validate(message)
        
