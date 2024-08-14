from app.constants import *
from app.services import attendance, break_time, schedule, tasks

def update_home_tab(client, user_id, workspace_id):
    user_status = attendance.get_user_status(user_id, workspace_id)
    user_schedules = schedule.get_user_schedules(user_id, workspace_id)
    user_tasks = tasks.get_user_tasks(user_id, workspace_id)
    
    view = {
        "type": "home",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🕒 Kotonaru勤怠管理",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*現在の状態:* {user_status['status']}"
                }
            },
            {
                "type": "actions",
                "elements": get_action_buttons(user_status['status'])
            },
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📅 今日のスケジュール",
                    "emoji": True
                }
            }
        ] + get_schedule_blocks(user_schedules) + [
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📝 タスク",
                    "emoji": True
                }
            }
        ] + get_task_blocks(user_tasks) + [
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "スケジュール管理",
                            "emoji": True
                        },
                        "value": "manage_schedule",
                        "action_id": ACTION_OPEN_SCHEDULE
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "タスク管理",
                            "emoji": True
                        },
                        "value": "manage_tasks",
                        "action_id": ACTION_OPEN_TASKS
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "休暇申請",
                            "emoji": True
                        },
                        "value": "request_leave",
                        "action_id": ACTION_OPEN_LEAVE_REQUEST
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "レポート",
                            "emoji": True
                        },
                        "value": "view_report",
                        "action_id": ACTION_OPEN_REPORT
                    }
                ]
            }
        ]
    }
    
    client.views_publish(user_id=user_id, view=view)

def get_action_buttons(status):
    if status == STATUS_WORKING:
        return [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "業務終了", "emoji": True},
                "style": "danger",
                "value": "end_work",
                "action_id": ACTION_WORK_END
            },
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "休憩開始", "emoji": True},
                "style": "primary",
                "value": "start_break",
                "action_id": ACTION_BREAK_BEGIN
            }
        ]
    elif status == STATUS_BREAK:
        return [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "休憩終了", "emoji": True},
                "style": "danger",
                "value": "end_break",
                "action_id": ACTION_BREAK_END
            }
        ]
    else:
        return [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "業務開始", "emoji": True},
                "style": "primary",
                "value": "start_work",
                "action_id": ACTION_WORK_BEGIN
            }
        ]

def get_schedule_blocks(schedules):
    blocks = []
    for schedule in schedules:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{schedule['start_time']} - {schedule['end_time']}*\n{schedule['description']}"
            }
        })
    return blocks

def get_task_blocks(tasks):
    blocks = []
    for task in tasks:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{task['description']}*\n期限: {task['due_date']}"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "完了",
                    "emoji": True
                },
                "value": task['task_id'],
                "action_id": "complete_task"
            }
        })
    return blocks