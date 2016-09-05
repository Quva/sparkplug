
from .schemas_v1 import SchemasV1
        
class SchemasV2(SchemasV1):

    messageReplySchema = {
        "reply_to_topic": {
            "type": "string",
            "required": True
        }
    }

    
    messageHeaderSchema = {
        "message_type": {
            "type": "string",
            "required": True
        },
        "message_id": {
            "type": "string",
            "required": True
        },
        "message_sender_id": {
            "type": "string",
            "required": True
        },
        "message_recipient_id": {
            "type": "string",
            "required": True
        },
        "message_reply": {
            "type": "dict",
            "required": False,
            "schema": messageReplySchema},
        "message_version": {
            "type": "string",
            "required": False}}

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


    measurementDataSchema = {
        "measurement_time": {
            "type": "string",
            "required": True
        },
        "measurement_num_value": {
            "type": "float",
            "required": False
        },
        "variable_name": {
            "type": "string",
            "required": True
        },
        "variable_source_id": {
            "type": "string",
            "required": True
        },
    }


    measurementsMessageBodySchema = {
        "product_id": {
            "type": "string",
            "required": True
        },
        "product_produced_time": {
            "type": "string",
            "required": True
        },
        "product_produced_id": {
            "type": "string",
            "required": True
        },
        "data": {
            "type": "list",
            "required": True,
            "schema": measurementDataSchema
        }
    }

    
    
    
    variableSchema = {
        "variable_name": {
            "type": "string",
            "required": True
        },
        "variable_name_alias": {
            "type": "string",
            "required": False
        },
        "variable_source_id": {
            "type": "string",
            "required": True
        },
        "variable_is_txt": {
            "type": "string",
            "required": False
        },
        "variable_unit": {
            "type": "string",
            "required": False
        },
        "variable_description": {
            "type": "string",
            "required": False
        },
        "variable_description_alias": {
            "type": "string",
            "required": False
        },
        "variable_properties": {
            "type": "dict",
            "required": False
        }
    }
    
    
    messageBodySchema = {
        "measurements": {
            "type": "dict",
            "required": False,
            "schema": measurementsBodySchema
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
        }
    }
    
    eventMessageBodySchema = {
        "event": {
            "type": "dict",
            "required": True,
            "schema": eventSchema
        },
        "measurements": {
            "type": "list",
            "required": True,
            "schema": measurementSchema
        },
        "request_analysis": {
            "type": "boolean",
            "required": False
        }
    }

        
    eventMessageSchema = {
        "message_header": {
            "type": "dict",
            "required": True,
            "schema": messageHeaderSchema},
        "message_body": {
            "type": "dict",
            "required": True,
            "schema": eventMessageBodySchema}}

    
    variablesMessageBodySchema = {
        "variables": {
            "type": "list",
            "required": True,
            "schema": variableSchema
        }
    }
    
    
    variablesMessageSchema = {
        "message_header": {
            "type": "dict",
            "required": True,
            "schema": messageHeaderSchema},
        "message_body": {
            "type": "dict",
            "required": True,
            "schema": variablesMessageBodySchema}}
    
    
    #messageBodySchema = 
    
    #variablesMessageBodySchema = {}

    @classmethod
    def getSchemaForMessageType(schemas, messageType):
        if messageType == "measurements":
            return schemas.measurementsMessageSchema
        if messageType == "variables":
            return schemas.variablesMessageSchema
        if messageType == "product":
            return schemas.productMessageSchema
    

class Schemas(object):

    v1 = SchemasV1
    v2 = SchemasV2
    latest = SchemasV1
    
