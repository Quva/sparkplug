from ..v2.messages import messageHeaderSchema

eventMetadataMessageSchema = {
    "message_header": {
        "type": "dict",
        "required": True,
        "schema": messageHeaderSchema
    },
    "message_body": {
        "type": "dict",
        "required": True,
        "schema": {
            "event_id": {
                "type": "string",
                "required": True
            },
            "metadata": {
                "type": "list",
                "required": True,
                "schema": {
                    "key": {
                        "type": "string",
                        "required": True
                    },
                    "value": {
                        "type": "string",
                        "required": True
                    },
                    "time": {
                        "type": "datetime",
                        "required": False
                    }
                }
            }
        }
    }
}

eventMeasurementMessageSchema = {
    "message_header": {
        "type": "dict",
        "required": True,
        "schema": messageHeaderSchema
    },
    "message_body": {
        "type": "dict",
        "required": True,
        "schema": {
            "event_id": {
                "type": "string",
                "required": True
            },
            "variable_ids": {
                "type": "list",
                "required": True,
                "schema": {
                    "variable_id": {
                        "type": "string",
                        "required": True
                    },
                    "measurements": {
                        "type": "list",
                        "required": True,
                        "schema": {
                            "value": {
                                "type": "float",
                                "required": True
                            },
                            "time": {
                                "type": "datetime",
                                "required": False
                            }
                        }
                    }
                }
            }
        }
    }
}
