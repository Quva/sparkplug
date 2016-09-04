
from cerberus import Validator

from .schemas import Schemas

def validateMessage(message):
      
      validateMessageWithSchema(message, Schemas.latest.messageSchema)

      header = message["message_header"]
      
      ver = header.get("message_version", "latest")
      
      messageType = header["message_type"]
      
      if messageType in ["event", "event-update"]:
            validateMessageWithSchema(message, getattr(Schemas, ver).eventMessageSchema)
            
      elif messageType == "variables":
            validateMessageWithSchema(message, getattr(Schemas, ver).variablesMessageSchema)
            
      else:
            raise Exception("Wrong message_type " +
                            "({})".format(header["message_type"]))
      
                            
def validateMessageWithSchema(obj, schema):
  
      v = Validator(schema)
      res = v.validate(obj)

      if res is not True:
            raise Exception(str(v.errors))
  
