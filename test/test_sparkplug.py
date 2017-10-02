
import unittest
import json
from nose.tools import raises, assert_equal, assert_equals, assert_true, assert_almost_equals

from sparkplug import SparkPlug

class SparkPlugTest(unittest.TestCase):

    plug = SparkPlug()

    def test_linestate_v1_json(self):

        message = self.plug.loadJSON("test/test_linestate_v1.json")
        assert_equal(message["message_header"]["message_version"], "v2")
        self.plug.validate(message)

    def test_linestate_v1_no_measurements_json(self):

        message = self.plug.loadJSON("test/test_linestate_v1_no_measurements.json")
        self.plug.validate(message)

    def test_event_message_v2_json(self):

        message = self.plug.loadJSON("test/test_event_v2.json")
        self.plug.validate(message)

        assert_equals(message["message_body"]["event"]["job_id"], "123")
        assert_equals(message["message_body"]["event"]["run_id"], "456")

        # Assert converter functions for backwards compatibility
        assert_equals(message["message_body"]["event"]["process_id"], message["message_body"]["event"]["event_properties"]["Prod_machine"])
        assert_equals(message["message_body"]["event"]["product_id"], message["message_body"]["event"]["event_properties"]["Product_global_code"])
        assert_equals(message["message_body"]["event"]["event_produced_time"], message["message_body"]["event"]["event_properties"]["Time_material_produced"])

        firstMeas = message["message_body"]["event"]["measurement_data"][0]

        assert_true(firstMeas["measurement_threshold_min"] is None)
        assert_true(firstMeas["measurement_target"] is None)
        assert_almost_equals(firstMeas["measurement_threshold_max"], 2.5)

        secondMeas = message["message_body"]["event"]["measurement_data"][1]

        assert_true(secondMeas["measurement_threshold_min"] is None)
        assert_true(secondMeas["measurement_target"] is None)
        assert_true(secondMeas["measurement_threshold_max"] is None)

    def test_event_list_message_v2_json(self):

        message = self.plug.loadJSON("test/test_event_list_v2.json")
        self.plug.validate(message)

        assert_equals(len(message["message_body"]["events"]), 2)
        assert_equals(message["message_body"]["events"][0]["job_id"], "123")
        assert_equals(message["message_body"]["events"][0]["run_id"], "456")

    def test_event_message_v2_xml(self):

        message = self.plug.loadXML("test/test_event_v2.xml")
        self.plug.validate(message)

        assert_equals(message["message_body"]["event"]["job_id"], "123")
        assert_equals(message["message_body"]["event"]["run_id"], "456")


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
