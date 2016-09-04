
from cerberus import Validator

def validate(obj, schema):
  
      v = Validator(schema)
      res = v.validate(obj)

      if res is not True:
            raise Exception(str(v.errors))
  
