
import unittest
import json
from nose.tools import raises, assert_equal, assert_true

from sparkplug import SparkPlug

class SparkPlugTest(unittest.TestCase):

    plug = SparkPlug()

    def test_linestate_v1_json(self):

        message = self.plug.loadJSON("test/test_linestate_v1.json")
        self.plug.validate(message)

    def test_linestate_v1_no_measurements_json(self):

        message = self.plug.loadJSON("test/test_linestate_v1_no_measurements.json")
        self.plug.validate(message)

    def test_event_message_v2_json(self):

        message = self.plug.loadJSON("test/test_event_v2.json")
        self.plug.validate(message)

    def test_event_message_v2_json_noconversion(self):

        message = self.plug.loadJSON("test/test_event_v2_noconversion.json")
        self.plug.validate(message)
        message2 = json.load(open("test/test_event_v2_noconversion.json"))
        assert_equal(message, message2)

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

    def test_variables_message_v2_group_in_properties_json(self):

        message = self.plug.loadJSON("test/test_variables_v2_group_in_properties.json")
        self.plug.validate(message)
        assert_true(message["message_body"]["variables"]["variable_data"][0].get("variable_group", None) \
                    == "PROCESS")

    def test_variables_message_v2_xml(self):

        message = self.plug.loadXML("test/test_variables_v2.xml")
        print(message)
        self.plug.validate(message)

    #@raises(Exception)
    #def test_variables_message_v2_xml_bad_language_formatting(self):
    #    
    #    message = self.plug.loadXML("test/test_variables_v2_bad_language_formatting.xml")
    #    #print(message)
    #    self.plug.validate(message)
        
    def test_product_message_v2_json(self):

        message = self.plug.loadJSON("test/test_product_v2.json")
        self.plug.validate(message)

    def test_product_message_v2_xml(self):

        message = self.plug.loadXML("test/test_product_v2.xml")
        self.plug.validate(message)

    def test_job_message_v2_json(self):

        message = self.plug.loadJSON("test/test_job_v2.json")
        self.plug.validate(message)
