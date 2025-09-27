import json

HABIT_FILE = "habits.json"

def read_habit():
    try:
        with open(HABIT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"habit": [], "completed": []}

def save_habit(data):
    with open(HABIT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def add_habit(name):
    data = read_habit()
    data["habit"].append(name)
    save_habit(data)

def delete_habit(index):
    data = read_habit()
    if 0 < index <= len(data["habit"]):
        removed = data["habit"].pop(index-1)
        save_habit(data)
        return f"{removed} deleted!"
    return "Invalid index."


def save_habit(data):
    with open(HABIT_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_habit(habit_name):
    data = read_habit()
    data["habit"].append(habit_name)
    save_habit(data)

def list_habits():
    data = read_habit()
    if not data["habit"]:
        print("No habits found.")
    else:
        for i, habit in enumerate(data["habit"], start=1):
            print(f"{i}. {habit}")

def delete_habit(habit_number):
    data = read_habit()
    index = habit_number - 1
    if 0 <= index < len(data["habit"]):
        removed = data["habit"].pop(index)
        save_habit(data)
        return f"Habit '{removed}' deleted successfully."
    else:
        return "Habit not found."

def update_habit(habit_number, new_name):
    data = read_habit()
    index = habit_number - 1
    if 0 <= index < len(data["habit"]):
        old_name = data["habit"][index]
        data["habit"][index] = new_name
        save_habit(data)
        return f"Habit '{old_name}' updated to '{new_name}'."
    else:
        return "Habit not found."

def complete_habit(habit_number):
    data = read_habit()
    index = habit_number - 1
    if 0 <= index < len(data["habit"]):
        completed = data["habit"].pop(index)
        if "completed" not in data:
            data["completed"] = []
        data["completed"].append(completed)
        save_habit(data)
        return f"Habit '{completed}' marked as completed."
    else:
        return "Habit not found."

def list_completed_habits():
    data = read_habit()
    completed = data.get("completed", [])
    if not completed:
        print("No completed habits.")
    else:
        for i, habit in enumerate(completed, start=1):
            print(f"{i}. {habit}")
