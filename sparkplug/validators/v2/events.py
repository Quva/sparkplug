from .measurements import measurementDataSchema
from .headers import messageHeaderSchema
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