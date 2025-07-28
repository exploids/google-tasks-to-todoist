# google-tasks-to-todoist

A command-line utility to convert your Google Tasks JSON exports into a CSV format compatible with Todoist, making it easier to migrate your tasks.

If you're switching from Google Tasks to Todoist, you've likely discovered that there's no direct way to import your tasks. This tool bridges that gap by converting your Google Tasks data into a structured CSV file that Todoist can import, preserving your task lists, titles, and due dates.

## Usage

The general usage is as follows:

1. Export your Google Tasks data as a JSON file from [Google Takeout](https://takeout.google.com/).
2. Convert the JSON file to Todoist-compatible CSV using **google-tasks-to-todoist**.
3. Import the generated CSV files into Todoist.

This project uses `uv` for project and dependency management. If you don't have `uv` installed, you can find installation instructions [here](https://docs.astral.sh/uv/getting-started/installation/).
Once you have `uv` installed, you can run the converter from your terminal using `uvx`:

```bash
uvx google-tasks-to-todoist [INPUT_FILE] [OPTIONS]
```

The script will generate a separate CSV file for each of your task lists. These files will be saved in the same directory as your input file, ready for import into Todoist.

-   `[INPUT_FILE]`: The path to your `Tasks.json` file from Google Takeout.
-   `--starred-priority PRIORITY`: Set the priority for starred tasks. The default is `2`. (1: highest priority, 4: lowest priority)
-   `--non-starred-priority PRIORITY`: Set the priority for non-starred tasks. The default is `4`. (1: highest priority, 4: lowest priority)
-   `--include-completed`: Include completed tasks in the export. By default, they are not included.

## How to Get Your Google Tasks Data

You can export your Google Tasks data as a JSON file from [Google Takeout](https://takeout.google.com/). Select only "Tasks" to get a `Tasks.json` file.

## Example

Let's say you have a `Tasks.json` file, and you want to assign the medium priority to your starred tasks and a no priority to others.

```bash
uvx google-tasks-to-todoist Tasks.json
```

This command will:

-   **Read tasks from `Tasks.json`**.
-   **Assign medium priority (2)** to all starred tasks (the default).
-   **Assign no priority (4)** to all non-starred tasks (the default).
-   **Exclude completed tasks** (since `--include-completed` is not present).
-   **Generate CSV files** for each task list, which you can then import into Todoist.

## Limitations on Recurring Tasks

Please note that Google's Takeout export for Tasks does not include information about recurring tasks. As a result, all tasks converted by this utility will be non-recurring.

## Development

If you prefer to clone the repository and manage dependencies locally:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/exploids/google-tasks-to-todoist.git
    cd google-tasks-to-todoist
    ```

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

3.  **Run the converter:**
    ```bash
    uv run google-tasks-to-todoist [INPUT_FILE] [OPTIONS]
    ```

To run the test suite, use the following command:

```bash
uv run pytest
```

## Disclaimer

This tool is an independent project and is not affiliated with, endorsed by, or in any way officially connected with Google or Doist.
