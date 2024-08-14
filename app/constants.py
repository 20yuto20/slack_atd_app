# Status constants
STATUS_WORKING = "業務中"
STATUS_BREAK = "休憩中"
STATUS_OFF_DUTY = "業務外"

# Table names
TABLE_USER_SETTINGS = "user_settings"
TABLE_PUNCH_TIME = "punch_time"
TABLE_BREAK_TIME = "break_time"
TABLE_SCHEDULES = "schedules"
TABLE_LEAVE_REQUESTS = "leave_requests"
TABLE_TASKS = "tasks"

# Action IDs
ACTION_WORK_BEGIN = "click_work_begin"
ACTION_WORK_END = "click_work_end"
ACTION_BREAK_BEGIN = "click_break_begin"
ACTION_BREAK_END = "click_break_end"
ACTION_OPEN_SETTINGS = "open_settings"
ACTION_OPEN_SCHEDULE = "open_schedule"
ACTION_OPEN_REPORT = "open_report"
ACTION_OPEN_LEAVE_REQUEST = "open_leave_request"
ACTION_OPEN_TASKS = "open_tasks"

# Callback IDs
CALLBACK_WORK_DONE_MODAL = "callback_id_work_done_modal"
CALLBACK_SETTINGS_MODAL = "callback_settings_modal"
CALLBACK_SCHEDULE_MODAL = "callback_schedule_modal"
CALLBACK_LEAVE_REQUEST_MODAL = "callback_leave_request_modal"
CALLBACK_TASKS_MODAL = "callback_tasks_modal"

# Message templates
MSG_WORK_START = "業務開始時刻：{time}"
MSG_WORK_END = "業務終了時刻：{time}"
MSG_WORK_DURATION = "稼働時間：{hours}時間{minutes}分\n休憩時間：{break_hours}時間{break_minutes}分"