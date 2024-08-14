from app.config import config
from slack_sdk.web.async_client import AsyncWebClient

def get_slack_client():
    return AsyncWebClient(token=config.BOT_TOKEN)

def send_message(client, channel, text):
    try:
        client.chat_postMessage(channel=channel, text=text)
    except Exception as e:
        print(f"Error sending message: {e}")

def update_home_view(client, user_id, view_content):
    try:
        client.views_publish(user_id=user_id, view=view_content)
    except Exception as e:
        print(f"Error updating home view: {e}")

def open_modal(client, trigger_id, view_content):
    try:
        client.views_open(trigger_id=trigger_id, view=view_content)
    except Exception as e:
        print(f"Error opening modal: {e}")

def post_to_channel(client, channel, message):
    try:
        client.chat_postMessage(channel=channel, text=message)
    except Exception as e:
        print(f"Error posting to channel: {e}")

def get_user_info(client, user_id):
    try:
        user_info = client.users_info(user=user_id)
        return user_info["user"]
    except Exception as e:
        print(f"Error getting user info: {e}")
        return None

def update_message(client, channel, ts, text):
    try:
        client.chat_update(channel=channel, ts=ts, text=text)
    except Exception as e:
        print(f"Error updating message: {e}")

def add_reaction(client, channel, timestamp, reaction):
    try:
        client.reactions_add(channel=channel, timestamp=timestamp, name=reaction)
    except Exception as e:
        print(f"Error adding reaction: {e}")

def remove_reaction(client, channel, timestamp, reaction):
    try:
        client.reactions_remove(channel=channel, timestamp=timestamp, name=reaction)
    except Exception as e:
        print(f"Error removing reaction: {e}")

def get_channel_info(client, channel_id):
    try:
        channel_info = client.conversations_info(channel=channel_id)
        return channel_info["channel"]
    except Exception as e:
        print(f"Error getting channel info: {e}")
        return None

def invite_user_to_channel(client, channel_id, user_id):
    try:
        client.conversations_invite(channel=channel_id, users=[user_id])
    except Exception as e:
        print(f"Error inviting user to channel: {e}")

def create_channel(client, channel_name, is_private=False):
    try:
        response = client.conversations_create(name=channel_name, is_private=is_private)
        return response["channel"]["id"]
    except Exception as e:
        print(f"Error creating channel: {e}")
        return None