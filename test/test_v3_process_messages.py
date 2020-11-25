
import json
import unittest

from nose.tools import (assert_almost_equals, assert_equal, assert_equals,
                        assert_true, raises)
from sparkplug import SparkPlug
from sparkplug.validators.validate import SchemaValidationException


class SparkPlugV3Test(unittest.TestCase):

    plug = SparkPlug()

    def test_process_measurement_success(self):
        message = self.plug.loadJSON("test/v3/process_measurements.json")
        assert_equal(message["message_header"]["message_version"], "v3")
        assert_equal(message["message_body"]
                     ["process_id"], "test_1_process_id")
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
    def test_process_measurements_missing_process_id(self):

        message = self.plug.loadJSON("test/v3/process_measurements_missing_process_id.json")
        self.plug.validate(message)

    @raises(SchemaValidationException)
    def test_process_measurements_missing_variables(self):

        message = self.plug.loadJSON("test/v3/process_measurements_missing_variables.json")
        self.plug.validate(message)

    def test_process_meta_data_success(self):
        message = self.plug.loadJSON("test/v3/process_metadata.json")
        assert_equal(message["message_header"]["message_version"], "v3")
        assert_equal(message["message_body"]["process_id"], "test_1_process_id" )
        assert_equal(message["message_body"]["metadata"][0]["key"], "key_1" )
        assert_equal(message["message_body"]["metadata"][1]["value"], "value_2" )
        self.plug.validate(message)

    @raises(SchemaValidationException)
    def test_process_meta_data_success(self):
        message = self.plug.loadJSON("test/v3/process_metadata_missing_metadata.json")
        self.plug.validate(message)
