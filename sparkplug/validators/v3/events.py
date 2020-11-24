from ..v2.messages import messageHeaderSchema

eventMeasurement = {
    "measurement_numeric_value": {
        "type": "float",
        "required": True
    },
    "measurement_time": {
        "type": "string",
        "required": False
    }
}
eventVariableMeasurements = {
    "variable_id": {
        "type": "string",
        "required": True
    },
    "measurements": {
        "type": "list",
        "required": True,
        "schema": eventMeasurement
    }
}
eventMeasurements = {
    "event_id": {
        "type": "string",
        "required": True
    },
    "variables": {
        "type": "list",
        "required": True,
        "schema": eventVariableMeasurements
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
            "process_measurements": {
                "type": "dict",
                "required": True,
                "schema": eventMeasurements
            }
        }
    }
}

eventMetaData = {
    "key": {
        "type": "string",
        "required": True
    },
    "value": {
        "type": "string",
        "required": True
    }
}

eventMetaDatas = {
    "event_id": {
        "type": "string",
        "required": True
    },
    "meta_data": {
        "type": "list",
        "required": True,
        "schema": eventMetaData
    }
}

eventMetaDataMessageSchema = {
    "message_header": {
        "type": "dict",
        "required": True,
        "schema": messageHeaderSchema
    },
    "message_body": {
        "type": "dict",
        "required": True,
        "schema": {
            "event_meta_data": {
                "type": "dict",
                "required": True,
                "schema": eventMetaDatas
            }
        }
    }
}
