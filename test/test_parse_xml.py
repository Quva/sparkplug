
from nose.tools import assert_true

from sparkplug.parsers import xml
from sparkplug.helpers import TagInfo

from sparkplug import SparkPlug

def test_parse_event_v2_xml():
    
    message = xml.load(open("test/test_event_v2.xml", "r"))
    
    plug = SparkPlug()

    plug.post(message, isDryrun=True)

def test_parse_variables_v2_xml():
    
    message = xml.load(open("test/test_variables_v2.xml", "r"))
    
    plug = SparkPlug()

    plug.post(message, isDryrun=True)
