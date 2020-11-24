from .events import eventBodySchema
from .variables import variablesBodySchema
from .products import productBodySchema
from .jobs import jobBodySchema

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
