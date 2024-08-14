from app.services import report, analysis

def open_report_modal(client, trigger_id, user_id, workspace_id):
    weekly_report = report.generate_weekly_report(user_id, workspace_id, client)
    work_pattern = analysis.analyze_work_pattern(user_id, workspace_id)
    productivity_stats = analysis.get_productivity_stats(user_id, workspace_id)
    
    view = {
        "type": "modal",
        "title": {"type": "plain_text", "text": "レポート"},
        "close": {"type": "plain_text", "text": "閉じる"},
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "週間レポート",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": weekly_report
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "勤務パターン分析",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": work_pattern
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "生産性統計",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"総労働時間: {productivity_stats['total_work_time']:.2f} 時間\n"
                            f"完了タスク数: {productivity_stats['total_tasks_completed']}\n"
                            f"生産性指標: {productivity_stats['productivity']:.2f} タスク/時間"
                }
            }
        ]
    }
    
    client.views_open(trigger_id=trigger_id, view=view)