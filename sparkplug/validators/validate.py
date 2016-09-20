
from cerberus import Validator

from .schemas import Schemas

def validateMessage(message):
      
      validateMessageWithSchema(message, Schemas.latest.getSchemaForMessageType("message"))
      
      header = message["message_header"]
      
      ver = header.get("message_version", "default")

      messageType = header["message_type"]

      schemas = getattr(Schemas, ver, None)

      if schemas is None:
            raise Exception("Unknown schema version: {}".format(ver))
      
      schema = schemas.getSchemaForMessageType(messageType)

      validateMessageWithSchema(message, schema)
      
                            
def validateMessageWithSchema(obj, schema):
  
      v = Validator(schema, allow_unknown=False)
      res = v.validate(obj)

      if res is not True:
            raise Exception(str(v.errors))
  
