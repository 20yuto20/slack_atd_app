from datetime import datetime
from app.db.dynamo_db import db
from app.constants import *
from app.slack_utils import update_home_view

def start_break(user_id, workspace_id, client):
    timestamp = datetime.now()
    break_start_time = timestamp.strftime('%H:%M')
    
    items = db.query(
        TABLE_PUNCH_TIME,
        'punch_user_id = :uid AND punch_workspace_id = :wid',
        {':uid': user_id, ':wid': workspace_id}
    )
    
    if not items:
        return False
    
    latest_punch = items[0]
    
    break_item = {
        'break_id': f"{latest_punch['p_key']}_{timestamp.strftime('%Y%m%d%H%M%S')}",
        'punch_id': latest_punch['p_key'],
        'break_begin_time': break_start_time
    }
    
    if db.put_item(TABLE_BREAK_TIME, break_item):
        update_home_view(client, user_id, {"status": STATUS_BREAK, "break_start_time": break_start_time})
        return True
    return False

def end_break(user_id, workspace_id, client):
    timestamp = datetime.now()
    break_end_time = timestamp.strftime('%H:%M')
    
    items = db.query(
        TABLE_BREAK_TIME,
        'break_id BEGINS_WITH :pid',
        {':pid': f"{user_id}_{workspace_id}_"}
    )
    
    if not items:
        return False
    
    latest_break = items[0]
    break_start_time = datetime.strptime(latest_break['break_begin_time'], '%H:%M')
    break_end_time_obj = datetime.strptime(break_end_time, '%H:%M')
    break_duration = break_end_time_obj - break_start_time
    
    db.update_item(
        TABLE_BREAK_TIME,
        {'break_id': latest_break['break_id']},
        "SET break_end_time = :bet, break_duration = :bd",
        {':bet': break_end_time, ':bd': break_duration.seconds // 60}
    )
    
    update_home_view(client, user_id, {"status": STATUS_WORKING})
    return True

def get_total_break_duration(punch_id):
    items = db.query(
        TABLE_BREAK_TIME,
        'punch_id = :pid',
        {':pid': punch_id}
    )
    
    total_duration = sum(item.get('break_duration', 0) for item in items)
    hours, minutes = divmod(total_duration, 60)
    return hours, minutes