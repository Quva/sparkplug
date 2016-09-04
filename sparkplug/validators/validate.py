
from cerberus import Validator

def validate(obj, schema):
  
      v = Validator(schema)
      res = v.validate(obj)
      return res, v.errors()
  
