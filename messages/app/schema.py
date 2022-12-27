email_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "title": {"type": "string"},
        "recipients": {"type": "array"},
        "body": {"type": "string"}
    },
    "required": ["username", "password", "title", "recipients", "body"]
}

telegram_text_schema = {
    "type": "object",
    "properties": {
        "token": {"type": "string"},
        "chat_id": {"type": "string"},
        "text": {"type": "string"}
    },
    "required": ["token", "chat_id", "text"]
}

slack_schema = {
    "type": "object",
    "properties": {
        "token": {"type": "string"},
        "channel": {"type": "string"},
        "text": {"type": "string"}
    },
    "required": ["token", "channel", "text"]
}

