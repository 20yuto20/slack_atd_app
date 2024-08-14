from app.db.dynamo_db import db
from app.constants import TABLE_LEAVE_REQUESTS
from app.slack_utils import send_message
from app.services.settings import get_supervisor
import uuid

def request_leave(user_id, workspace_id, start_date, end_date, reason, client):
    request_id = str(uuid.uuid4())
    item = {
        'user_id': user_id,
        'workspace_id': workspace_id,
        'request_id': request_id,
        'start_date': start_date,
        'end_date': end_date,
        'reason': reason,
        'status': 'pending'
    }
    if db.put_item(TABLE_LEAVE_REQUESTS, item):
        supervisor = get_supervisor(user_id, workspace_id)
        if supervisor:
            send_message(client, supervisor, f"新しい休暇申請があります: {start_date} - {end_date}")
        return True
    return False

def approve_leave(request_id, approver_id, client):
    item = db.get_item(TABLE_LEAVE_REQUESTS, {'request_id': request_id})
    if item:
        db.update_item(
            TABLE_LEAVE_REQUESTS, 
            {'request_id': request_id},
            "SET #status = :s, approver = :a",
            {':s': 'approved', ':a': approver_id},
            {'#status': 'status'}
        )
        send_message(client, item['user_id'], f"休暇申請が承認されました: {item['start_date']} - {item['end_date']}")
        return True
    return False

def reject_leave(request_id, approver_id, reason, client):
    item = db.get_item(TABLE_LEAVE_REQUESTS, {'request_id': request_id})
    if item:
        db.update_item(
            TABLE_LEAVE_REQUESTS, 
            {'request_id': request_id},
            "SET #status = :s, approver = :a, reject_reason = :r",
            {':s': 'rejected', ':a': approver_id, ':r': reason},
            {'#status': 'status'}
        )
        send_message(client, item['user_id'], f"休暇申請が却下されました: {item['start_date']} - {item['end_date']}\n理由: {reason}")
        return True
    return False

def get_leave_requests(user_id, workspace_id):
    return db.query(
        TABLE_LEAVE_REQUESTS,
        'user_id = :uid AND workspace_id = :wid',
        {':uid': user_id, ':wid': workspace_id}
    )