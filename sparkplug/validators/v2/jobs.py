from .messages import messageHeaderSchema

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