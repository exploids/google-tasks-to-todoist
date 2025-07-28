# google_tasks_to_todoist

A command-line utility to convert your Google Tasks JSON exports into a CSV format compatible with Todoist, making it easier to migrate your tasks.

If you're switching from Google Tasks to Todoist, you've likely discovered that there's no direct way to import your tasks. This tool bridges that gap by converting your Google Tasks data into a structured CSV file that Todoist can import, preserving your task lists, titles, and due dates.

## Installation

This project uses `uv` for project and dependency management.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/exploids/google-tasks-to-todoist.git
    cd google-tasks-to-todoist
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

## How to Get Your Google Tasks Data

You can export your Google Tasks data as a JSON file from [Google Takeout](https://takeout.google.com/). Select only "Tasks" to get a `Tasks.json` file.

## Usage

Run the converter from your terminal using `uv run`.

```bash
uv run google-tasks-to-todoist [INPUT_FILE] [OPTIONS]
```

-   `[INPUT_FILE]`: The path to your `Tasks.json` file from Google Takeout.

The script will generate a separate CSV file for each of your task lists. These files will be saved in the same directory as your input file, ready for import into Todoist.

### Options

-   `--starred-priority PRIORITY`: Set the priority for starred tasks. The default is `2`. (1: highest priority, 4: lowest priority)
-   `--non-starred-priority PRIORITY`: Set the priority for non-starred tasks. The default is `4`. (1: highest priority, 4: lowest priority)
-   `--include-completed`: Include completed tasks in the export. By default, they are not included.

## Example

Let's say you have a `Tasks.json` file and you want to assign the highest priority to your starred tasks and a medium priority to others.

```bash
uv run google-tasks-to-todoist Tasks.json --starred-priority 1 --non-starred-priority 3
```

This command will:

-   **Read tasks from `Tasks.json`**.
-   **Assign priority 1 (p1)** to all starred tasks.
-   **Assign priority 3 (p3)** to all non-starred tasks.
-   **Exclude completed tasks** (since `--include-completed` is not present).
-   **Generate CSV files** for each task list, which you can then import into Todoist.

## Testing

To run the test suite, use the following command:

```bash
uv run pytest
```

## Limitations on Recurring Tasks

Please note that Google's Takeout export for Tasks does not include information about recurring tasks. As a result, all tasks converted by this utility will be non-recurring.

## Disclaimer

This tool is an independent project and is not affiliated with, endorsed by, or in any way officially connected with Google or Doist.
