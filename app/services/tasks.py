from app.db.dynamo_db import db
from app.constants import TABLE_TASKS
import uuid

def add_task(user_id, workspace_id, description, due_date):
    task_id = str(uuid.uuid4())
    item = {
        'user_id': user_id,
        'workspace_id': workspace_id,
        'task_id': task_id,
        'description': description,
        'due_date': due_date,
        'status': 'pending'
    }
    return db.put_item(TABLE_TASKS, item)

def complete_task(task_id):
    return db.update_item(
        TABLE_TASKS, 
        {'task_id': task_id}, 
        "SET #status = :s",
        {':s': 'completed'},
        {'#status': 'status'}
    )

def get_user_tasks(user_id, workspace_id):
    return db.query(
        TABLE_TASKS,
        'user_id = :uid AND workspace_id = :wid',
        {':uid': user_id, ':wid': workspace_id}
    )

def update_task(task_id, description=None, due_date=None, status=None):
    update_expression = []
    expression_attribute_values = {}
    
    if description:
        update_expression.append("description = :d")
        expression_attribute_values[':d'] = description
    if due_date:
        update_expression.append("due_date = :dd")
        expression_attribute_values[':dd'] = due_date
    if status:
        update_expression.append("#status = :s")
        expression_attribute_values[':s'] = status
    
    if update_expression:
        return db.update_item(
            TABLE_TASKS,
            {'task_id': task_id},
            "SET " + ", ".join(update_expression),
            expression_attribute_values,
            {'#status': 'status'} if status else None
        )
    return False

def delete_task(task_id):
    return db.delete_item(TABLE_TASKS, {'task_id': task_id})