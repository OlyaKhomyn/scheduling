slack_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "bot_token": {"type": "string"},
        "user_token": {"type": "string"},
        "channel_id": {"type": "string"},
    },
    "required": ["name", "channel_id", "bot_token", "user_token"]
}
