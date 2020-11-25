
import json
import unittest

from nose.tools import (assert_almost_equals, assert_equal, assert_equals,
                        assert_true, raises)
from sparkplug import SparkPlug
from sparkplug.validators.validate import SchemaValidationException


class SparkPlugV3EventTest(unittest.TestCase):

    plug = SparkPlug()

    def test_event_measurement_success(self):
        message = self.plug.loadJSON("test/v3/event_measurements.json")
        assert_equal(message["message_header"]["message_version"], "v3")
        assert_equal(message["message_body"]
                     ["event_id"], "event_id_1")
        assert_equal(message["message_body"]["variable_ids"]
                     [0]["variable_id"], "test_var_1")
        assert_equal(message["message_body"]["variable_ids"]
                     [0]["variable_id"], "test_var_1")
        assert_equal(message["message_body"]["variable_ids"]
                     [0]["measurements"][0]["value"], 1.2)
        assert_equal(message["message_body"]["variable_ids"]
                     [0]["measurements"][0]["time"], "2020-11-25T14:32:16+3:00")
        self.plug.validate(message)

    @raises(SchemaValidationException)
    def test_event_measurements_missing_event_id(self):

        message = self.plug.loadJSON("test/v3/event_measurements_missing_event_id.json")
        self.plug.validate(message)

    @raises(SchemaValidationException)
    def test_event_measurements_missing_variables(self):

        message = self.plug.loadJSON("test/v3/event_measurements_missing_measurements.json")
        self.plug.validate(message)

    def test_event_meta_data_success(self):
        message = self.plug.loadJSON("test/v3/event_metadata.json")
        assert_equal(message["message_header"]["message_version"], "v3")
        assert_equal(message["message_body"]["event_id"], "event_id_1" )
        assert_equal(message["message_body"]["metadata"][0]["key"], "key_1" )
        assert_equal(message["message_body"]["metadata"][1]["value"], "value_2" )
        self.plug.validate(message)

    @raises(SchemaValidationException)
    def test_event_meta_data_success(self):
        message = self.plug.loadJSON("test/v3/event_metadata_missing_metadata.json")
        self.plug.validate(message)
