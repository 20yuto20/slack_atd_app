from app.constants import CALLBACK_SCHEDULE_MODAL
from app.services import schedule
from datetime import datetime

def open_schedule_modal(client, trigger_id, user_id, workspace_id):
    view = {
        "type": "modal",
        "callback_id": CALLBACK_SCHEDULE_MODAL,
        "title": {"type": "plain_text", "text": "スケジュール登録"},
        "submit": {"type": "plain_text", "text": "登録"},
        "close": {"type": "plain_text", "text": "キャンセル"},
        "blocks": [
            {
                "type": "input",
                "block_id": "start_time",
                "label": {"type": "plain_text", "text": "開始時間"},
                "element": {
                    "type": "datetimepicker",
                    "action_id": "start_time_picker"
                }
            },
            {
                "type": "input",
                "block_id": "end_time",
                "label": {"type": "plain_text", "text": "終了時間"},
                "element": {
                    "type": "datetimepicker",
                    "action_id": "end_time_picker"
                }
            },
            {
                "type": "input",
                "block_id": "description",
                "label": {"type": "plain_text", "text": "説明"},
                "element": {
                    "type": "plain_text_input",
                    "action_id": "description_input"
                }
            }
        ]
    }
    
    client.views_open(trigger_id=trigger_id, view=view)

def handle_schedule_submission(ack, body, client):
    ack()
    user_id = body["user"]["id"]
    workspace_id = body["team"]["id"]
    
    start_time = datetime.fromtimestamp(int(body["view"]["state"]["values"]["start_time"]["start_time_picker"]["selected_date_time"]))
    end_time = datetime.fromtimestamp(int(body["view"]["state"]["values"]["end_time"]["end_time_picker"]["selected_date_time"]))
    description = body["view"]["state"]["values"]["description"]["description_input"]["value"]
    
    schedule.register_schedule(user_id, workspace_id, start_time, end_time, description)
    client.chat_postMessage(channel=user_id, text="スケジュールが登録されました。")