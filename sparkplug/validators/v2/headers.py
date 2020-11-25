
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
        "schema": messageReplySchema
        },
    "message_version": {
        "type": "string",
        "required": False}}