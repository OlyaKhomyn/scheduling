sender_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["email", "password"]
}

recipients_schema = {
    "type": "object",
    "properties": {
        "emails": {"type": "array"}
    },
    "required": ["emails"]
}