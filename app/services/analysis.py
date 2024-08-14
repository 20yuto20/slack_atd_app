from app.db.dynamo_db import db
from app.constants import TABLE_PUNCH_TIME
from datetime import datetime, timedelta
from collections import defaultdict

def analyze_work_pattern(user_id, workspace_id):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # 過去30日間のデータを分析
    
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
    
    pattern = defaultdict(list)
    for record in work_records:
        day = datetime.strptime(record['punch_date'], '%Y年%m月%d日').strftime('%A')
        if 'punch_out' in record and 'punch_in' in record:
            work_hours = (datetime.strptime(record['punch_out'], '%H:%M') - 
                          datetime.strptime(record['punch_in'], '%H:%M')).total_seconds() / 3600
            pattern[day].append(work_hours)
    
    analysis = "あなたの勤務パターン分析:\n"
    for day, hours in pattern.items():
        avg_hours = sum(hours) / len(hours)
        analysis += f"{day}: 平均 {avg_hours:.2f} 時間\n"
    
    if any(sum(hours) / len(hours) > 10 for hours in pattern.values()):
        analysis += "\n提案: 一部の曜日で長時間労働が見られます。業務の分散を検討してみてはいかがでしょうか？"
    
    return analysis

def get_productivity_stats(user_id, workspace_id):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # 過去30日間のデータを分析
    
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
    
    total_work_time = 0
    total_tasks_completed = 0
    
    for record in work_records:
        if 'punch_out' in record and 'punch_in' in record:
            work_hours = (datetime.strptime(record['punch_out'], '%H:%M') - 
                          datetime.strptime(record['punch_in'], '%H:%M')).total_seconds() / 3600
            total_work_time += work_hours
        
        if 'work_contents' in record:
            total_tasks_completed += len(record['work_contents'].split(','))
    
    productivity = total_tasks_completed / total_work_time if total_work_time > 0 else 0
    
    return {
        'total_work_time': total_work_time,
        'total_tasks_completed': total_tasks_completed,
        'productivity': productivity
    }