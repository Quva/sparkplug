
from .v1.schemas import SchemasV1
from .v2.schemas import SchemasV2
from .v3.schemas import SchemasV3

class Schemas(object):
    
    v1 = SchemasV1
    v2 = SchemasV2
    v3 = SchemasV3
    default = SchemasV1
    latest = SchemasV3
