from src.application.infrastructure.web.schema.json.user import user

put_user = {
    "type": "object",
    "properties": {
        "updated_user": user,
        "update_by_selector": {
            "type": "string"
        },
        "update_by_data": {
            "type": "string"
        }
    },
    "required": ["updated_user", "update_by_selector", "update_by_data"]
}
