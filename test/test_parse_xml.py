
from nose.tools import assert_true

from sparkplug.parsers import xml
from sparkplug.helpers import TagInfo

from sparkplug import SparkPlug

def test_parse_xml():
    
    message = xml.load(open("test/test_event.xml", "r"))
    
    plug = SparkPlug()

    plug.post(message, isDryrun=True)


    
