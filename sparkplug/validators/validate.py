
from cerberus import Validator

from .schemas import Schemas


class SchemaValidationException(Exception):
      """Raised when message validation failed"""
      pass

def validateMessage(message):

      validateMessageWithSchema(message, Schemas.latest.getSchemaForMessageType("message"), "latest")

      header = message["message_header"]

      ver = header.get("message_version", "default")

      messageType = header["message_type"]

      schemas = getattr(Schemas, ver, None)

      if schemas is None:
            raise Exception("Unknown schema version: {}".format(ver))

      schema = schemas.getSchemaForMessageType(messageType)

      validateMessageWithSchema(message, schema, ver)


def validateMessageWithSchema(obj, schema, ver):

      v = Validator(schema, allow_unknown=False)
      res = v.validate(obj)

      if res is not True:
            raise SchemaValidationException("Errors with schema ver {}: {}".format(ver, v.errors))

