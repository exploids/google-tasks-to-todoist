import pytest
from google_tasks_to_todoist.converter import map_google_tasks_to_todoist_tasks

@pytest.fixture
def sample_tasks():
    return [
        {
            "id": "task1",
            "title": "Top-level task",
            "status": "needsAction",
            "due": "2025-08-01T10:00:00Z",
            "notes": "A description for the top-level task.",
            "starred": True,
        },
        {"id": "task2", "title": "Subtask", "parent": "task1", "status": "needsAction", "starred": False},
        {"id": "task3", "title": "Completed task", "status": "completed", "starred": False},
        {"id": "task4", "title": "Another top-level task", "status": "needsAction", "starred": False},
    ]


def test_map_google_tasks_to_todoist_tasks_basic(sample_tasks):
    result = map_google_tasks_to_todoist_tasks(sample_tasks, 1, 4, False)
    assert len(result) == 3
    assert result[0]["CONTENT"] == "Top-level task"
    assert result[1]["CONTENT"] == "Subtask"
    assert result[2]["CONTENT"] == "Another top-level task"


def test_map_google_tasks_to_todoist_tasks_include_completed(sample_tasks):
    result = map_google_tasks_to_todoist_tasks(sample_tasks, 1, 4, True)
    assert len(result) == 4
    assert result[2]["CONTENT"] == "Completed task"


def test_subtask_indentation(sample_tasks):
    result = map_google_tasks_to_todoist_tasks(sample_tasks, 1, 4, False)
    assert result[0]["INDENT"] == 1
    assert result[1]["INDENT"] == 2


def test_priority_mapping(sample_tasks):
    result = map_google_tasks_to_todoist_tasks(sample_tasks, 1, 4, False)
    assert result[0]["PRIORITY"] == 1
    assert result[1]["PRIORITY"] == 4


def test_date_mapping(sample_tasks):
    result = map_google_tasks_to_todoist_tasks(sample_tasks, 1, 4, False)
    assert result[0]["DATE"] == "2025-08-01 10:00"
