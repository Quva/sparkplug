from .events import eventBodySchema
from .variables import variablesBodySchema
from .products import productBodySchema
from .jobs import jobBodySchema
from .headers import messageHeaderSchema

messageBodySchema = {
    "event": {
        "type": "dict",
        "required": False,
        "schema": eventBodySchema
    },
    "events": {
        "type": "list",
        "required": False
        #"schema": eventBodySchema
    },

    "variables": {
        "type": "dict",
        "required": False,
        "schema": variablesBodySchema
    },
    "product": {
        "type": "dict",
        "required": False,
        "schema": productBodySchema
    },
    "job_header": {
        "type": "dict",
        "required": False,
        "schema": jobBodySchema
    }
}

messageSchema = {
    "message_header": {
        "type": "dict",
        "required": True,
        "schema": messageHeaderSchema
    },
    "message_body": {
        "type": "dict",
        "required": True
    }
}
