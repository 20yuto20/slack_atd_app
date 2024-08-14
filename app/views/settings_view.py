from app.constants import CALLBACK_SETTINGS_MODAL
from app.services import settings

def open_settings_modal(client, trigger_id, user_id, workspace_id):
    user_settings = settings.get_user_settings(user_id, workspace_id)
    
    view = {
        "type": "modal",
        "callback_id": CALLBACK_SETTINGS_MODAL,
        "title": {"type": "plain_text", "text": "設定"},
        "submit": {"type": "plain_text", "text": "保存"},
        "close": {"type": "plain_text", "text": "キャンセル"},
        "blocks": [
            {
                "type": "input",
                "block_id": "report_channel",
                "label": {"type": "plain_text", "text": "報告用チャンネル"},
                "element": {
                    "type": "channels_select",
                    "placeholder": {"type": "plain_text", "text": "チャンネルを選択"},
                    "action_id": "report_channel_select",
                    "initial_channel": user_settings.get('report_channel_id', '')
                }
            },
            {
                "type": "input",
                "block_id": "supervisor",
                "label": {"type": "plain_text", "text": "上長（メンションする人）"},
                "element": {
                    "type": "users_select",
                    "placeholder": {"type": "plain_text", "text": "ユーザーを選択"},
                    "action_id": "supervisor_select",
                    "initial_user": user_settings.get('supervisor_user_id', '')
                }
            }
        ]
    }
    
    client.views_open(trigger_id=trigger_id, view=view)

def handle_settings_submission(ack, body, client):
    ack()
    user_id = body["user"]["id"]
    workspace_id = body["team"]["id"]
    
    new_settings = {
        "report_channel_id": body["view"]["state"]["values"]["report_channel"]["report_channel_select"]["selected_channel"],
        "supervisor_user_id": body["view"]["state"]["values"]["supervisor"]["supervisor_select"]["selected_user"]
    }
    
    settings.update_user_settings(user_id, workspace_id, new_settings)
    client.chat_postMessage(channel=user_id, text="設定が更新されました。")