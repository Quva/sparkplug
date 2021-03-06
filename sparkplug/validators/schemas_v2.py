
from .schemas_v1 import SchemasV1

import copy

class SchemasV2(SchemasV1):

    version = "v2"

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
            "required": False
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

    variableTranslationSchema = {
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
            "schema": variableTranslationSchema
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
        "process_id": {
            "type": "string",
            "required": False,
            "nullable": True
        },
        "job_id": {
            "type": "string",
            "required": True
        },
        "run_id": {
            "type": "string",
            "required": True,
            "nullable": True
        },
        "product_id": {
            "type": "string",
            "required": True,
            "nullable": True
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
                    "required": False,
                    "schema": eventBodySchema
                },
               "events": {
                    "type": "list",
                    "required": False
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


    @classmethod
    def lift(cls, msg, logger=None):

        msgVersion = msg["message_header"].get("message_version", "v1")

        if msgVersion == "v2":
            if logger:
                logger.info("No need to lift, message is already v2")
            return msg

        if msgVersion == "v1":
            return SchemasV2.__liftFromV1(msg, logger=logger)
        else:
            if logger:
                logger.info("No rule to lift {} -> v2".format(msgVersion))
            return msg

    @classmethod
    def __liftFromV1(cls, msg, logger=None):

        msgType = msg["message_header"]["message_type"]

        if msgType == "event":
            if logger:
                logger.info("Lifting message={} v1 -> v2".format(msgType))
            return SchemasV2.__liftEventFromV1(msg)
        else:
            if logger:
                logger.info("No rule to lift message={} v1 -> v2".format(msgType))



    @classmethod
    def __liftEventFromV1(cls, msg_c):

        msg = copy.deepcopy(msg_c)

        msg["message_header"]["message_version"] = "v2"

        msg["message_body"]["event"]["measurement_data"] = msg["message_body"].get("measurements", [])
        if msg["message_body"].get("measurements"):
            del msg["message_body"]["measurements"]

        return msg

