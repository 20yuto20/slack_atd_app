from app.constants import CALLBACK_TASKS_MODAL
from app.services import tasks
from datetime import datetime

def open_tasks_modal(client, trigger_id, user_id, workspace_id):
    user_tasks = tasks.get_user_tasks(user_id, workspace_id)
    
    view = {
        "type": "modal",
        "callback_id": CALLBACK_TASKS_MODAL,
        "title": {"type": "plain_text", "text": "タスク管理"},
        "submit": {"type": "plain_text", "text": "新規タスク追加"},
        "close": {"type": "plain_text", "text": "閉じる"},
        "blocks": [
            {
                "type": "input",
                "block_id": "new_task",
                "label": {"type": "plain_text", "text": "新規タスク"},
                "element": {
                    "type": "plain_text_input",
                    "action_id": "task_input"
                }
            },
            {
                "type": "input",
                "block_id": "due_date",
                "label": {"type": "plain_text", "text": "期限"},
                "element": {
                    "type": "datepicker",
                    "action_id": "due_date_picker"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "現在のタスク",
                    "emoji": True
                }
            }
        ] + [get_task_block(task) for task in user_tasks]
    }
    
    client.views_open(trigger_id=trigger_id, view=view)

def get_task_block(task):
    return {
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
    }

def handle_tasks_submission(ack, body, client):
    ack()
    user_id = body["user"]["id"]
    workspace_id = body["team"]["id"]
    
    new_task = body["view"]["state"]["values"]["new_task"]["task_input"]["value"]
    due_date = body["view"]["state"]["values"]["due_date"]["due_date_picker"]["selected_date"]
    
    success = tasks.add_task(user_id, workspace_id, new_task, due_date)
    
    if success:
        client.chat_postMessage(channel=user_id, text=f"新しいタスク「{new_task}」が追加されました。期限: {due_date}")
    else:
        client.chat_postMessage(channel=user_id, text="タスクの追加に失敗しました。もう一度お試しください。")

def handle_complete_task(ack, body, client):
    ack()
    task_id = body["actions"][0]["value"]
    
    success = tasks.complete_task(task_id)
    
    if success:
        client.chat_postMessage(channel=body["user"]["id"], text="タスクが完了としてマークされました。")
    else:
        client.chat_postMessage(channel=body["user"]["id"], text="タスクの完了処理に失敗しました。もう一度お試しください。")