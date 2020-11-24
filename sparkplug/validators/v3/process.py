from ..v2.messages import messageHeaderSchema

processMeasurement = {
    "measurement_numeric_value": {
        "type": "float",
        "required": True
    },
    "measurement_time": {
        "type": "string",
        "required": True
    }
}

processVariableMeasurements = {
    "variable_id": {
        "type": "string",
        "required": True
    },
    "measurements": {
        "type": "list",
        "required": True,
        "schema": processMeasurement
    }
}

processMeasurements = {
    "process_id": {
        "type": "string",
        "required": True
    },
    "variables": {
        "type": "list",
        "required": True,
        "schema": processVariableMeasurements
    }
}

processMeasurementMessageSchema = {
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
                "schema": processMeasurements
            }
        }
    }
}

processMetaData = {
    "time": {
        "type": "string",
        "required": True,
    },
    "key": {
        "type": "string",
        "required": True
    },
    "value": {
        "type": "string",
        "required": True
    }
}

processMetaDatas = {
    "process_id": {
        "type": "string",
        "required": True
    },
    "meta_data": {
        "type": "list",
        "required": True,
        "schema": processMetaData
    }

}
processMetaDataMessageSchema = {
    "message_header": {
        "type": "dict",
        "required": True,
        "schema": messageHeaderSchema
    },
    "message_body": {
        "type": "dict",
        "required": True,
        "schema": {
            "process_meta_data": {
                "type": "dict",
                "required": True,
                "schema": processMetaDatas
            }
        }
    }
}
