from app.db.dynamo_db import db
from app.constants import *
from app.slack_utils import send_message, update_home_view, post_to_channel
from app.services.settings import get_report_channel, get_supervisor
from datetime import datetime

def get_user_status(user_id, workspace_id):
    # ユーザーの最新の打刻記録を取得
    items = db.query(
        TABLE_PUNCH_TIME,
        'punch_user_id = :uid AND punch_workspace_id = :wid',
        {':uid': user_id, ':wid': workspace_id}
    )
    
    if not items:
        return {
            'status': STATUS_OFF_DUTY,
            'workspace_id': workspace_id
        }
    
    # 最新の記録を取得（日付でソート）
    latest_punch = max(items, key=lambda x: x['punch_date'])
    
    if 'punch_out' in latest_punch:
        return {
            'status': STATUS_OFF_DUTY,
            'workspace_id': workspace_id
        }
    else:
        return {
            'status': STATUS_WORKING,
            'workspace_id': workspace_id
        }

def record_work_start(user_id, workspace_id, client):
    timestamp = datetime.now()
    date = timestamp.strftime('%Y年%m月%d日')
    time = timestamp.strftime('%H:%M')
    
    item = {
        'punch_user_id': user_id,
        'punch_workspace_id': workspace_id,
        'punch_date': date,
        'punch_in': time,
        'p_key': f"{user_id}_{workspace_id}_{timestamp.strftime('%Y%m%d%H%M%S')}"
    }
    
    if db.put_item(TABLE_PUNCH_TIME, item):
        send_message(client, user_id, MSG_WORK_START.format(time=time))
        update_home_view(client, user_id, {"status": STATUS_WORKING, "start_time": time})
        
        # 管理者に通知
        report_channel = get_report_channel(user_id, workspace_id)
        supervisor = get_supervisor(user_id, workspace_id)
        user_info = client.users_info(user=user_id)
        username = user_info["user"]["real_name"]
        
        if report_channel and supervisor:
            post_to_channel(client, report_channel, f"<@{supervisor}> {username}さんが業務を開始しました。\n業務開始時刻：{time}")
        
        return True
    return False

def record_work_end(user_id, workspace_id, client):
    timestamp = datetime.now()
    end_time = timestamp.strftime('%H:%M')
    
    items = db.query(
        TABLE_PUNCH_TIME,
        'punch_user_id = :uid AND punch_workspace_id = :wid',
        {':uid': user_id, ':wid': workspace_id}
    )
    
    if not items:
        return False
    
    latest_punch = max(items, key=lambda x: x['punch_date'])
    start_time = datetime.strptime(latest_punch['punch_in'], '%H:%M')
    end_time_obj = datetime.strptime(end_time, '%H:%M')
    work_duration = end_time_obj - start_time
    
    hours, remainder = divmod(work_duration.seconds, 3600)
    minutes = remainder // 60
    
    db.update_item(
        TABLE_PUNCH_TIME,
        {'p_key': latest_punch['p_key']},
        "SET punch_out = :po, work_time = :wt",
        {':po': end_time, ':wt': f"{hours}時間{minutes}分"}
    )
    
    send_message(client, user_id, MSG_WORK_END.format(time=end_time))
    update_home_view(client, user_id, {"status": STATUS_OFF_DUTY})
    
    return latest_punch['p_key'], hours, minutes

def update_work_contents(user_id, workspace_id, p_key, work_contents, client):
    db.update_item(
        TABLE_PUNCH_TIME,
        {'p_key': p_key},
        "SET work_contents = :wc",
        {':wc': work_contents}
    )
    
    # 管理者に報告
    report_channel = get_report_channel(user_id, workspace_id)
    supervisor = get_supervisor(user_id, workspace_id)
    user_info = client.users_info(user=user_id)
    username = user_info["user"]["real_name"]
    
    if report_channel and supervisor:
        item = db.get_item(TABLE_PUNCH_TIME, {'p_key': p_key})
        if item:
            start_time = item['punch_in']
            end_time = item['punch_out']
            work_time = item['work_time']
            
            message = (
                f"<@{supervisor}> {username}さんが業務を終了しました。\n"
                f"{username}さんの業務開始時刻：{start_time}\n"
                f"{username}さんの業務終了時刻：{end_time}\n"
                f"{username}さんの業務時間：{work_time}\n"
                f"業務内容：{work_contents}"
            )
            post_to_channel(client, report_channel, message)

    return True