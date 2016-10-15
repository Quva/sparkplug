
import unittest
from nose.tools import raises, assert_equal

from sparkplug import SparkPlug

class SparkPlugTest(unittest.TestCase):

    plug = SparkPlug()

    def test_event_message_v2_json(self):
        
        message = self.plug.loadJSON("test/test_event_v2.json")
        self.plug.validate(message)

    def test_event_message_v2_xml(self):

        message = self.plug.loadXML("test/test_event_v2.xml")        
        self.plug.validate(message)
                
    def test_event_message_v2_no_data_json(self):

        message = self.plug.loadJSON("test/test_event_v2_no_data.json")        
        self.plug.validate(message)
        
        
    def test_event_message_v2_no_data_xml(self):
        
        message = self.plug.loadXML("test/test_event_v2_no_data.xml")        
        self.plug.validate(message)
        
    def test_variables_message_v2_json(self):
        
        message = self.plug.loadJSON("test/test_variables_v2.json")        
        self.plug.validate(message)

    def test_variables_message_v2_xml(self):
        
        message = self.plug.loadXML("test/test_variables_v2.xml")
        self.plug.validate(message)

    def test_product_message_v2_json(self):
        
        message = self.plug.loadJSON("test/test_product_v2.json")        
        self.plug.validate(message)

    def test_product_message_v2_xml(self):
        
        message = self.plug.loadXML("test/test_product_v2.xml")        
        self.plug.validate(message)

    def test_job_message_v2_json(self):
        
        message = self.plug.loadJSON("test/test_job_v2.json")
        self.plug.validate(message)
