from app.constants import CALLBACK_WORK_DONE_MODAL
from app.services import attendance

def open_work_done_modal(client, trigger_id, work_hours, work_minutes, break_hours, break_minutes):
    view = {
        "type": "modal",
        "callback_id": CALLBACK_WORK_DONE_MODAL,
        "title": {"type": "plain_text", "text": "業務サマリー・業務内容記入"},
        "submit": {"type": "plain_text", "text": "送信"},
        "close": {"type": "plain_text", "text": "キャンセル"},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*今回の業務時間*: {work_hours}時間{work_minutes}分"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*休憩時間*: {break_hours}時間{break_minutes}分"
                }
            },
            {
                "type": "input",
                "block_id": "work_summary",
                "label": {"type": "plain_text", "text": "業務内容サマリー"},
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "work_summary_input"
                }
            }
        ]
    }
    
    client.views_open(trigger_id=trigger_id, view=view)

def handle_work_done_submission(ack, body, client, user_id, workspace_id):
    ack()
    
    work_summary = body["view"]["state"]["values"]["work_summary"]["work_summary_input"]["value"]
    
    attendance.update_work_contents(user_id, workspace_id, body["view"]["private_metadata"], work_summary, client)