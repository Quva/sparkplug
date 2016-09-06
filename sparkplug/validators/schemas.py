
from .schemas_v1 import SchemasV1
from .schemas_v2 import SchemasV2

class Schemas(object):
    
    v1 = SchemasV1
    v2 = SchemasV2
    latest = SchemasV1
    
