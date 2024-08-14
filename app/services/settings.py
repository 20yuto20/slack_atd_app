from app.db.dynamo_db import db
from app.constants import TABLE_USER_SETTINGS

def get_user_settings(user_id, workspace_id):
    return db.get_item(TABLE_USER_SETTINGS, {'user_id': user_id, 'workspace_id': workspace_id})

def update_user_settings(user_id, workspace_id, settings):
    return db.update_item(
        TABLE_USER_SETTINGS,
        {'user_id': user_id, 'workspace_id': workspace_id},
        "SET " + ", ".join(f"{k} = :{k}" for k in settings.keys()),
        {f":{k}": v for k, v in settings.items()}
    )

def get_report_channel(user_id, workspace_id):
    settings = get_user_settings(user_id, workspace_id)
    return settings.get('report_channel_id') if settings else None

def get_supervisor(user_id, workspace_id):
    settings = get_user_settings(user_id, workspace_id)
    return settings.get('supervisor_user_id') if settings else None