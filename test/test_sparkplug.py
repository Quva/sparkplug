
import json
import unittest
from nose.tools import raises

from sparkplug import SparkPlug


class SparkPlugTest(unittest.TestCase):

    plug = SparkPlug()

    def post(self, payload):
        isDryrun = True
        return self.plug.post(payload, isDryrun)

    def test_event_message(self):

        message = json.load(
            open("test/test_event.json", 'r'))

        self.post(message)

    def test_variables_message(self):

        message = json.load(open("test/test_variables.json", 'r'))

        self.post(message)

    def test_analysis_request(self):

        message = json.load(open("test/test_analysis_request.json", 'r'))

        self.post(message)

    @raises(Exception)
    def test_empty_measurements_raises(self):

        self.post({})

    @raises(Exception)
    def test_measurements_missing_message_type(self):

        self.post({"message_apikey": "abc",
                   "message_body": []})

    @raises(Exception)
    def test_variables_missing_variables_raises(self):

        message = json.load(
            open("test/test_bad_variables.json", 'r'))

        self.post(message)

    @raises(Exception)
    def test_variables2_missing_variables_raises(self):

        message = json.load(
            open("test/test_bad_variables2.json", 'r'))

        self.post(message)