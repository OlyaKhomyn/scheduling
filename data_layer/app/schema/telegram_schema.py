token_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "token": {"type": "string"},
    },
    "required": ["token", "name"]
}

group_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "group_id": {"type": "string"}
    },
    "required": ["group_id"]
}
