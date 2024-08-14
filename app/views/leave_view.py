from app.constants import CALLBACK_LEAVE_REQUEST_MODAL
from app.services import leave
from datetime import datetime

def open_leave_request_modal(client, trigger_id, user_id, workspace_id):
    view = {
        "type": "modal",
        "callback_id": CALLBACK_LEAVE_REQUEST_MODAL,
        "title": {"type": "plain_text", "text": "休暇申請"},
        "submit": {"type": "plain_text", "text": "申請"},
        "close": {"type": "plain_text", "text": "キャンセル"},
        "blocks": [
            {
                "type": "input",
                "block_id": "start_date",
                "label": {"type": "plain_text", "text": "開始日"},
                "element": {
                    "type": "datepicker",
                    "action_id": "start_date_picker"
                }
            },
            {
                "type": "input",
                "block_id": "end_date",
                "label": {"type": "plain_text", "text": "終了日"},
                "element": {
                    "type": "datepicker",
                    "action_id": "end_date_picker"
                }
            },
            {
                "type": "input",
                "block_id": "reason",
                "label": {"type": "plain_text", "text": "理由"},
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "reason_input"
                }
            }
        ]
    }
    
    client.views_open(trigger_id=trigger_id, view=view)

def handle_leave_request_submission(ack, body, client):
    ack()
    user_id = body["user"]["id"]
    workspace_id = body["team"]["id"]
    
    start_date = body["view"]["state"]["values"]["start_date"]["start_date_picker"]["selected_date"]
    end_date = body["view"]["state"]["values"]["end_date"]["end_date_picker"]["selected_date"]
    reason = body["view"]["state"]["values"]["reason"]["reason_input"]["value"]
    
    success = leave.request_leave(user_id, workspace_id, start_date, end_date, reason, client)
    
    if success:
        client.chat_postMessage(channel=user_id, text="休暇申請が送信されました。承認をお待ちください。")
    else:
        client.chat_postMessage(channel=user_id, text="休暇申請の送信に失敗しました。もう一度お試しください。")