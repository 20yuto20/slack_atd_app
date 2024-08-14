from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from app.config import config
from app.constants import *
from app.services import attendance, break_time, schedule, report, leave, tasks, analysis
from app.views import home_view, settings_view, work_done_view, schedule_view, report_view, leave_view, tasks_view

app = App(
    token=config.BOT_TOKEN,
    signing_secret=config.APP_TOKEN,
    process_before_response=True
)

def ack_app_home_opened(ack):
    ack()

def update_home_tab(client, event, logger):
    try:
        user_id = event["user"]
        workspace_id = event["team"]
        home_view.update_home_tab(client, user_id, workspace_id)
    except Exception as e:
        logger.error(f"Error updating home view: {e}")

app.event("app_home_opened")(
    ack=ack_app_home_opened,
    lazy=[update_home_tab]
)

def ack_work_begin(ack):
    ack()

def process_work_begin(client, body):
    user_id = body["user"]["id"]
    workspace_id = body["team"]["id"]
    attendance.record_work_start(user_id, workspace_id, client)

app.action(ACTION_WORK_BEGIN)(
    ack=ack_work_begin,
    lazy=[process_work_begin]
)

def ack_work_end(ack):
    ack()

def process_work_end(client, body):
    user_id = body["user"]["id"]
    workspace_id = body["team"]["id"]
    p_key, work_hours, work_minutes = attendance.record_work_end(user_id, workspace_id, client)
    break_hours, break_minutes = break_time.get_total_break_duration(p_key)
    work_done_view.open_work_done_modal(client, body["trigger_id"], work_hours, work_minutes, break_hours, break_minutes)

app.action(ACTION_WORK_END)(
    ack=ack_work_end,
    lazy=[process_work_end]
)

def ack_break_begin(ack):
    ack()

def process_break_begin(client, body):
    user_id = body["user"]["id"]
    workspace_id = body["team"]["id"]
    break_time.start_break(user_id, workspace_id, client)

app.action(ACTION_BREAK_BEGIN)(
    ack=ack_break_begin,
    lazy=[process_break_begin]
)

def ack_break_end(ack):
    ack()

def process_break_end(client, body):
    user_id = body["user"]["id"]
    workspace_id = body["team"]["id"]
    break_time.end_break(user_id, workspace_id, client)

app.action(ACTION_BREAK_END)(
    ack=ack_break_end,
    lazy=[process_break_end]
)

def ack_open_settings(ack):
    ack()

def process_open_settings(client, body):
    user_id = body["user"]["id"]
    workspace_id = body["team"]["id"]
    settings_view.open_settings_modal(client, body["trigger_id"], user_id, workspace_id)

app.action(ACTION_OPEN_SETTINGS)(
    ack=ack_open_settings,
    lazy=[process_open_settings]
)

def ack_settings_submission(ack):
    ack()

def process_settings_submission(client, body):
    settings_view.handle_settings_submission(body, client)

app.view(CALLBACK_SETTINGS_MODAL)(
    ack=ack_settings_submission,
    lazy=[process_settings_submission]
)

def ack_work_done_submission(ack):
    ack()

def process_work_done_submission(client, body):
    user_id = body["user"]["id"]
    workspace_id = body["team"]["id"]
    work_done_view.handle_work_done_submission(body, client, user_id, workspace_id)

app.view(CALLBACK_WORK_DONE_MODAL)(
    ack=ack_work_done_submission,
    lazy=[process_work_done_submission]
)

def ack_open_schedule(ack):
    ack()

def process_open_schedule(client, body):
    user_id = body["user"]["id"]
    workspace_id = body["team"]["id"]
    schedule_view.open_schedule_modal(client, body["trigger_id"], user_id, workspace_id)

app.action(ACTION_OPEN_SCHEDULE)(
    ack=ack_open_schedule,
    lazy=[process_open_schedule]
)

def ack_schedule_submission(ack):
    ack()

def process_schedule_submission(client, body):
    schedule_view.handle_schedule_submission(body, client)

app.view(CALLBACK_SCHEDULE_MODAL)(
    ack=ack_schedule_submission,
    lazy=[process_schedule_submission]
)

def ack_open_report(ack):
    ack()

def process_open_report(client, body):
    user_id = body["user"]["id"]
    workspace_id = body["team"]["id"]
    report_view.open_report_modal(client, body["trigger_id"], user_id, workspace_id)

app.action(ACTION_OPEN_REPORT)(
    ack=ack_open_report,
    lazy=[process_open_report]
)

def ack_open_leave_request(ack):
    ack()

def process_open_leave_request(client, body):
    user_id = body["user"]["id"]
    workspace_id = body["team"]["id"]
    leave_view.open_leave_request_modal(client, body["trigger_id"], user_id, workspace_id)

app.action(ACTION_OPEN_LEAVE_REQUEST)(
    ack=ack_open_leave_request,
    lazy=[process_open_leave_request]
)

def ack_leave_request_submission(ack):
    ack()

def process_leave_request_submission(client, body):
    leave_view.handle_leave_request_submission(body, client)

app.view(CALLBACK_LEAVE_REQUEST_MODAL)(
    ack=ack_leave_request_submission,
    lazy=[process_leave_request_submission]
)

def ack_open_tasks(ack):
    ack()

def process_open_tasks(client, body):
    user_id = body["user"]["id"]
    workspace_id = body["team"]["id"]
    tasks_view.open_tasks_modal(client, body["trigger_id"], user_id, workspace_id)

app.action(ACTION_OPEN_TASKS)(
    ack=ack_open_tasks,
    lazy=[process_open_tasks]
)

def ack_tasks_submission(ack):
    ack()

def process_tasks_submission(client, body):
    tasks_view.handle_tasks_submission(body, client)

app.view(CALLBACK_TASKS_MODAL)(
    ack=ack_tasks_submission,
    lazy=[process_tasks_submission]
)

def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))