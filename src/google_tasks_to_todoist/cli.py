import argparse
from .converter import convert_google_tasks_to_todoist

def main():
    parser = argparse.ArgumentParser(description="Convert Google Tasks JSON to Todoist CSV.")
    parser.add_argument("input_file", help="Path to the Google Tasks JSON file.")
    parser.add_argument("--starred-priority", type=int, default=2, help="Priority for starred tasks (1-4).")
    parser.add_argument("--non-starred-priority", type=int, default=4, help="Priority for non-starred tasks (1-4).")
    parser.add_argument("--include-completed", action="store_true", help="Include completed tasks in the export.")
    
    args = parser.parse_args()
    
    convert_google_tasks_to_todoist(args.input_file, args.starred_priority, args.non_starred_priority, args.include_completed)

if __name__ == "__main__":
    main()
