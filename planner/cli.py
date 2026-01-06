from datetime import date, datetime
from planner.storage import load_tasks, save_tasks

def show_help():
    print("\nCommands:")
    print("  help  - show commands")
    print("  add   - add a task (next step)")
    print("  list  - list tasks (next step)")
    print("  today - show today's recommendations (later)")
    print("  quit  - save and exit")

def add_task(tasks):
    print("\nAdd a new task")

    title = input("Task title: ").strip()
    module = input("Module name: ").strip()
    deadline = input("Deadline (YYYY-MM-DD): ").strip()

    try:
        hours = float(input("Estimated hours needed: ").strip())
    except ValueError:
        print("Invalid number for hours.")
        return

    try:
        importance = int(input("Importance (1–5): ").strip())
        if importance < 1 or importance > 5:
            raise ValueError
    except ValueError:
        print("Importance must be between 1 and 5.")
        return

    task_id = max([t["id"] for t in tasks], default=0) + 1

    task = {
        "id": task_id,
        "title": title,
        "module": module,
        "deadline": deadline,
        "hours": hours,
        "importance": importance,
        "status": "todo"
    }

    tasks.append(task)
    print(f"Task added with ID {task_id}.")

def list_tasks(tasks):
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\nYour tasks:")
    for task in tasks:
        print(
            f"[{task['id']}] "
            f"{task['title']} | "
            f"{task['module']} | "
            f"Due: {task['deadline']} | "
            f"Hours: {task['hours']} | "
            f"Status: {task['status']}"
        )

def done_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            print(f"Task {task_id} marked as done.")
            return
    print(f"No task found with ID {task_id}.")
from datetime import datetime


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def priority_score(task, today):
    deadline = parse_date(task["deadline"])
    if deadline is None:
        days_left = 9999
    else:
        days_left = (deadline - today).days

    safe_days = max(days_left, 1)

    hours_left = float(task["hours"])
    importance = int(task["importance"])

    hours_per_day = hours_left / safe_days

    urgency = 10 / safe_days
    score = (importance * 2) + (hours_per_day * 3) + urgency

    return score, days_left, hours_per_day

def main():
    tasks = load_tasks()
    print("Smart Study Planner")
    print(f"Loaded {len(tasks)} task(s). Type 'help' to see commands.")

    while True:
        cmd = input("\n> ").strip().lower()

        if cmd in ("help", "h", "?"):
            show_help()

        elif cmd == "add":
            add_task(tasks)

        elif cmd == "list":
            list_tasks(tasks)

        elif cmd.startswith("done"):
            parts = cmd.split()
            if len(parts) != 2:
                print("Usage: done <task_id>")
            else:
                try:
                    task_id = int(parts[1])
                    done_task(tasks, task_id)
                except ValueError:
                    print("Task ID must be a number.")

        elif cmd == "today":
            today = date.today()
            todo = [t for t in tasks if t.get("status") != "done"]
            
            if not todo:
                print("\nNo active tasks. You're all caught up")
                continue
            ranked = []

            for t in todo:
                score, days_left, hpd = priority_score(t, today)
                ranked.append((score, days_left, hpd, t))

            ranked.sort(key=lambda x: x[0], reverse=True)

            print("\nToday's recommended focus:")

            for score, days_left, hpd, t in ranked[:3]:
                minutes_per_day = int(hpd * 60)

                print(
                    f"[{t['id']}] {t['title']} ({t['module']}) | "
                    f"Due in {days_left} day(s) | "
                    f"Suggested study: ~{minutes_per_day} min/day | "
                    f"Importance: {t['importance']}"
                )


        elif cmd in ("quit", "q", "exit"):
            save_tasks(tasks)
            print("Saved tasks. Bye!")
            break

        elif cmd == "":
            continue

        else:
            print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    main()