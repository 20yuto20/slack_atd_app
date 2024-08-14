from datetime import datetime, timedelta
from app.db.dynamo_db import db
from app.constants import TABLE_PUNCH_TIME
from app.slack_utils import send_message

def generate_weekly_report(user_id, workspace_id, client):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    work_records = db.query(
        TABLE_PUNCH_TIME,
        'punch_user_id = :uid AND punch_workspace_id = :wid AND punch_date BETWEEN :start AND :end',
        {
            ':uid': user_id,
            ':wid': workspace_id,
            ':start': start_date.strftime('%Y年%m月%d日'),
            ':end': end_date.strftime('%Y年%m月%d日')
        }
    )
    
    total_work_time = sum(
        (datetime.strptime(record['punch_out'], '%H:%M') - 
         datetime.strptime(record['punch_in'], '%H:%M')).total_seconds() / 3600 
        for record in work_records if 'punch_out' in record and 'punch_in' in record
    )
    
    report = f"週間レポート ({start_date.date()} - {end_date.date()}):\n"
    report += f"合計勤務時間: {total_work_time:.2f} 時間\n"
    report += "業務内容サマリー:\n"
    for record in work_records:
        if 'work_contents' in record:
            report += f"- {record['work_contents']}\n"
    
    send_message(client, user_id, report)