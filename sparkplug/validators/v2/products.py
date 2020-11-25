from .headers import messageHeaderSchema

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