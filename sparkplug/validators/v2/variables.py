from .headers import messageHeaderSchema

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

variablesBodySchema = {
    "variable_data": {
        "type": "list",
        "required": True,
        "schema": variableDataSchema
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