import csv
import json
import os
from datetime import datetime

def map_google_tasks_to_todoist_tasks(tasks_data, starred_priority, non_starred_priority, include_completed):
    """
    Maps Google Tasks data to a list of Todoist task dictionaries.

    Args:
        tasks_data (list): A list of Google Tasks.
        starred_priority (int): Priority for starred tasks.
        non_starred_priority (int): Priority for non-starred tasks.
        include_completed (bool): Whether to include completed tasks.

    Returns:
        list: A list of dictionaries, where each dictionary represents a Todoist task.
    """
    tasks_to_export = []
    
    # Create a dictionary for quick parent lookup
    task_dict = {task['id']: task for task in tasks_data}
    
    # Add parent field to each task
    for task in tasks_data:
        if 'parent' not in task and task.get('id') in task_dict:
            for potential_parent in tasks_data:
                if 'items' in potential_parent and task['id'] in [t['id'] for t in potential_parent['items']]:
                    task['parent'] = potential_parent['id']
                    break
    
    # A dictionary to store the indent level of each task
    indent_levels = {}
    
    # First, identify top-level tasks and assign indent level 1
    for task in tasks_data:
        if 'parent' not in task:
            indent_levels[task['id']] = 1

    # Then, iteratively determine the indent level for subtasks
    def get_indent_level(task_id):
        if task_id in indent_levels:
            return indent_levels[task_id]
        
        task = task_dict.get(task_id)
        if not task or 'parent' not in task:
            # Should not happen if the logic is correct, but as a fallback
            return 1
        
        parent_indent = get_indent_level(task['parent'])
        indent_levels[task_id] = parent_indent + 1
        return indent_levels[task_id]

    for task in tasks_data:
        if not include_completed and task.get('status') == 'completed':
            continue

        content = task.get('title', '')
        description = task.get('notes', '')
        priority = starred_priority if task.get('starred') else non_starred_priority
        
        indent = get_indent_level(task['id'])

        due_date = ''
        if 'due' in task:
            try:
                due_datetime = datetime.fromisoformat(task['due'].replace('Z', '+00:00'))
                due_date = due_datetime.strftime('%Y-%m-%d %H:%M')
            except ValueError:
                pass # Ignore invalid date formats

        tasks_to_export.append({
            'TYPE': 'task',
            'CONTENT': content,
            'DESCRIPTION': description,
            'PRIORITY': priority,
            'INDENT': indent,
            'AUTHOR': '',
            'RESPONSIBLE': '',
            'DATE': due_date,
            'DATE_LANG': 'en',
            'TIMEZONE': '',
            'DURATION': '',
            'DURATION_UNIT': '',
            'DEADLINE': '',
            'DEADLINE_LANG': ''
        })
    return tasks_to_export

def convert_google_tasks_to_todoist(input_file, starred_priority, non_starred_priority, include_completed):
    """
    Converts a Google Tasks JSON export to Todoist CSV files.

    Args:
        input_file (str): Path to the Google Tasks JSON file.
        starred_priority (int): Priority for starred tasks.
        non_starred_priority (int): Priority for non-starred tasks.
        include_completed (bool): Whether to include completed tasks.
    """
    output_dir = os.path.dirname(input_file)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for task_list in data.get('items', []):
        list_title = task_list.get('title', 'Untitled')
        csv_filename = os.path.join(output_dir, f"{list_title}.csv")

        tasks = task_list.get('items', [])
        tasks_to_export = map_google_tasks_to_todoist_tasks(tasks, starred_priority, non_starred_priority, include_completed)

        if tasks_to_export:
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['TYPE', 'CONTENT', 'DESCRIPTION', 'PRIORITY', 'INDENT', 'AUTHOR', 'RESPONSIBLE', 'DATE', 'DATE_LANG', 'TIMEZONE', 'DURATION', 'DURATION_UNIT', 'DEADLINE', 'DEADLINE_LANG']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(tasks_to_export)
