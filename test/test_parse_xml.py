
from nose.tools import assert_true

from sparkplug.parsers import xml
from sparkplug.helpers import TagInfo

from sparkplug import SparkPlug

def test_parse_xml():
    
    message = xml.load("test/test_event.xml")
    
    plug = SparkPlug()

    plug.post(message, isDryrun=True)


    
