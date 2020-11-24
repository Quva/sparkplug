
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