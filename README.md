# Smart Study Planner (CLI)

A Python command-line tool that helps students prioritise academic tasks based on deadlines,
estimated effort, and importance.

Instead of acting as a simple to-do list, the planner provides daily study recommendations.

---

## Features
- Add, list, and complete study tasks
- Persistent storage using JSON
- Deadline-aware prioritisation algorithm
- Daily study recommendations (minutes per day)
- Clean, modular CLI design

---

## How to Run

```bash
python -m planner.cli

```md
## Commands

Once the application is running, the following commands are available:

- `help`  
  Show all available commands.

- `add`  
  Add a new task (you will be prompted for title, module, deadline, hours, and importance).

- `list`  
  View all saved tasks along with their status.

- `done <id>`  
  Mark a task as completed using its ID (example: `done 2`).

- `today`  
  Show today’s recommended study focus based on deadlines, effort, and importance.  
  Outputs suggested study time in minutes per day.

- `quit` (or `q` / `exit`)  
  Save tasks to `tasks.json` and exit the application.