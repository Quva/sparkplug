
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
        "variable_id": {
            "type": "string",
            "required": True
        },
        "measurement_threshold_min": {
            "type": "float",
            "required": False
        },
        "measurement_target": {
            "type": "float",
            "required": False
        },
        "measurement_threshold_max": {
            "type": "float",
            "required": False
        },
        "measurement_timeuuid": {
            "type": "string",
            "required": True
        }
    }

    
    variableDescriptionTranslationSchema = {
        "language": {"type": "string", "required": True},
        "translation": {"type": "string", "required": True}
    }
    
    
    variableDataSchema = {
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
        "variable_group": {
            "type": "string",
            "required": True
        },
        "variable_description": {
            "type": "string",
            "required": False
        },
        "variable_description_alias": {
            "type": "string",
            "required": False
        },
        "variable_translations": {
            "type": "list",
            "required": False,
            "schema": variableDescriptionTranslationSchema
        },
        "variable_properties": {
            "type": "dict",
            "required": False
        }
    }
    
    
    eventActionsSchema = {
        "preclean_variable_groups": {
            "anyof_type": ["string", "list"],
            "required": False
        },
        "request_analysis": {
            "type": "boolean",
            "required": False
        },
        "request_analysis_feedback": {
            "type": "boolean",
            "required": False
        }
    }
    
    eventBodySchema = {
        "event_id": {
            "type": "string",
            "required": True
        },
        "product_id": {
            "type": "string",
            "required": False
        },
        "event_produced_time": {
            "type": "string",
            "required": False
        },
        "event_type": {
            "type": "string",
            "required": False
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
        },
        "measurement_data": {
            "type": "list",
            "required": False,
            "schema": measurementDataSchema
        },
        "actions": {
            "type": "dict",
            "required": False,
            "schema": eventActionsSchema
        }
    }
    
    
    variablesBodySchema = {
        "variable_data": {
            "type": "list",
            "required": True,
            "schema": variableDataSchema
        }
    }
    
    
    productBodySchema = {
        "product_id": {
            "type": "string",
            "required": True
        },
        "product_type": {
            "type": "string",
            "required": True
        },
        "product_status": {
            "type": "string",
            "required": True
        },
        "product_description": {
            "type": "list",
            "required": True
        },
        "product_certificates": {
            "type": "list",
            "required": False
        },
        "product_specifications": {
            "type": "list",
            "required": False
        },
        "product_properties": {
            "type": "dict",
            "required": False
        },        
        "actions": {
            "type": "dict",
            "required": False
        }
    }

    
    jobBodySchema = {
        "job_source_id": {
            "type": "string",
            "required": True
        },
        "job_data": {
            "type": "list",
            "required": True
        }
    }
    

    messageBodySchema = {
        "event": {
            "type": "dict",
            "required": False,
            "schema": eventBodySchema
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
    
    
    eventMessageSchema = {
        "message_header": {
            "type": "dict",
            "required": True,
            "schema": messageHeaderSchema},
        "message_body": {
            "type": "dict",
            "required": True,
            "schema": {
                "event": {
                    "type": "dict",
                    "required": True,
                    "schema": eventBodySchema
                }
            }
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
            "schema": {
                "variables": {
                    "type": "dict",
                    "required": True,
                    "schema": variablesBodySchema
                }
            }
        }
    }

    
    productMessageSchema = {
        "message_header": {
            "type": "dict",
            "required": True,
            "schema": messageHeaderSchema},
        "message_body": {
            "type": "dict",
            "required": True,
            "schema": {
                "product_header": {
                    "type": "dict",
                    "required": True,
                    "schema": productBodySchema
                }
            }
        }
    }

    jobMessageSchema = {
        "message_header": {
            "type": "dict",
            "required": True,
            "schema": messageHeaderSchema},
        "message_body": {
            "type": "dict",
            "required": True,
            "schema": {
                "job_header": {
                    "type": "dict",
                    "required": True,
                    "schema": jobBodySchema
                }
            }
        }
    }
    
    
    @classmethod
    def getSchemaForMessageType(schemas, messageType):
        if messageType == "event":
            return schemas.eventMessageSchema
        elif messageType == "variables":
            return schemas.variablesMessageSchema
        elif messageType == "product":
            return schemas.productMessageSchema
        elif messageType == "job":
            return schemas.jobMessageSchema
        elif messageType == "message":
            return schemas.messageSchema
        else:
            raise Exception("Unknown message type '{}' for schemas '{}'".format(messageType, schemas))
        
