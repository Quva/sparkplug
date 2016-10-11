
from nose.tools import assert_true

from sparkplug.parsers import xml
from sparkplug.helpers import TagInfo

from sparkplug import SparkPlug

def test_parse_event_v2_xml():
    
    message = xml.load(open("test/test_event_v2.xml", "r"))
    
    plug = SparkPlug()

    plug.validate(message)

    assert_true(message["message_body"]["event"]["actions"]["preclean_variable_groups"] == ["PROCESS"])
    
def test_parse_variables_v2_xml():
    
    message = xml.load(open("test/test_variables_v2.xml", "r"))
    
    plug = SparkPlug()

    plug.validate(message)
