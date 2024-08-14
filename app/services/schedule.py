from datetime import datetime
from app.db.dynamo_db import db
from app.constants import TABLE_SCHEDULES
from app.slack_utils import send_message

def register_schedule(user_id, workspace_id, start_time, end_time, description):
    item = {
        'user_id': user_id,
        'workspace_id': workspace_id,
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'description': description
    }
    return db.put_item(TABLE_SCHEDULES, item)

def get_user_schedules(user_id, workspace_id):
    return db.query(
        TABLE_SCHEDULES,
        'user_id = :uid AND workspace_id = :wid',
        {':uid': user_id, ':wid': workspace_id}
    )

def check_upcoming_schedules(client):
    now = datetime.now()
    upcoming = now.replace(minute=now.minute + 15).isoformat()
    schedules = db.scan(
        TABLE_SCHEDULES,
        'start_time BETWEEN :now AND :upcoming',
        {':now': now.isoformat(), ':upcoming': upcoming}
    )
    
    for schedule in schedules:
        send_message(
            client,
            schedule['user_id'],
            f"業務開始時間が近づいています: {schedule['description']}"
        )