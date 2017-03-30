
class SchemasV1(object):

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


    eventSchema = {
        "product_id": {
            "type": "string",
            "required": False
        },
        "event_id": {
            "type": "string",
            "required": True
        },
        "event_type": {
            "type": "string",
            "required": True
        },
        "event_start_time": {
            "type": "string",
            "required": False
        },
        "event_stop_time": {
            "type": "string",
            "required": False
        },
        "event_properties": {
            "type": "dict",
            "required": False
        }
    }


    measurementSchema = {
        "measurement_time": {
            "type": "string",
            "required": True
        },
        "measurement_num_value": {
            "type": "float",
            "required": False
        },
        "measurement_txt_value": {
            "type": "string",
            "required": False
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
        "event": {
            "type": "dict",
            "required": False,
            "schema": eventSchema
        },
        "measurements": {
            "type": "dict",
            "required": False,
            "schema": measurementSchema
        },
        "variables": {
            "type": "dict",
            "required": False,
            "schema": variableSchema
        },
        "request_analysis": {
            "type": "boolean",
            "required": False
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
            "required": False,
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

    @classmethod
    def getSchemaForMessageType(schemas, messageType):
        if messageType in ["event", "event-update"]:
            return schemas.eventMessageSchema
        elif messageType == "variables":
            return schemas.variablesMessageSchema
        elif messageType == "message":
            return schemas.messageSchema
        else:
            raise Exception("Unknown message type '{}' for schemas '{}'".format(messageType, schemas))
