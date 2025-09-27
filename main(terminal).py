from habits import add_habit, read_habit, delete_habit, save_habit
from stats import complete_habit_stat, show_profile, load_profile, save_profile
from ai import calculate_exp, generate_motivation
import os
import json

PROFILE_FILE = "profile.json"

def show_habits():
    data = read_habit()
    print("\nYour Habits:")
    for i, habit in enumerate(data["habit"], start=1):
        print(f"{i}. {habit}")
    print()

def show_completed():
    data = read_habit()
    completed = data.get("completed", [])
    print("\nCompleted Habits:")
    if not completed:
        print("No completed habits.")
    else:
        for i, h in enumerate(completed, start=1):
            print(f"{i}. {h}")
    print()

def add_habit_terminal():
    habit_name = input("Enter habit name: ")
    if habit_name:
        add_habit(habit_name)
        print(f"Habit '{habit_name}' added.")

def delete_habit_terminal():
    show_habits()
    index = input("Enter the number of the habit to delete: ")
    if index.isdigit():
        result = delete_habit(int(index))
        print(result)
    else:
        print("Invalid input.")

def complete_habit_terminal():
    show_habits()
    index = input("Enter the number of the habit to complete: ")
    data = read_habit()
    if index.isdigit():
        idx = int(index)
        if 1 <= idx <= len(data["habit"]):
            habit_name = data["habit"][idx - 1]
            data.setdefault("completed", []).append(habit_name)
            del data["habit"][idx - 1]
            save_habit(data)

            profile = load_profile()
            current_level = profile.get("level", 1)
            result = complete_habit_stat(habit_name, current_level, profile)

            if result["level_up"]:
                print(f"\nLEVEL UP! You reached Level {profile.get('level', 1)}!")
                print(f"Motivation: {result['motivation']}\n")
            else:
                print(f"\n{habit_name} completed! +{result['gained_exp']} EXP\n")
        else:
            print("Invalid habit number.")
    else:
        print("Invalid input.")

def show_profile_terminal():
    print("\nProfile:")
    print(show_profile())
    print()

def store_terminal():
    items = {"Potion": 50, "Sword": 100, "Shield": 80}
    profile = load_profile()
    print("\nStore:")
    for i, (item, cost) in enumerate(items.items(), start=1):
        print(f"{i}. {item} ({cost} EXP)")
    choice = input("Enter the number of the item to buy (or press Enter to cancel): ")
    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(items):
            item = list(items.keys())[idx - 1]
            cost = items[item]
            if profile.get("exp", 0) >= cost:
                profile["exp"] -= cost
                profile.setdefault("inventory", []).append(item)
                save_profile(profile)
                print(f"You bought a {item}!")
            else:
                print("Not enough EXP!")
        else:
            print("Invalid item number.")
    else:
        print("Cancelled.")

def load_profile():
    if not os.path.exists(PROFILE_FILE):
        return {
            "username": "Usta",
            "level": 1,
            "exp": 0,
            "completed_habits": 0,
            "streak": 0,
            "rank": "E-rank Hunter",
            "next_level_exp": 100,  # <-- Add this line
            "inventory": []
        }
    with open(PROFILE_FILE, "r") as f:
        profile = json.load(f)
        if "next_level_exp" not in profile:
            profile["next_level_exp"] = profile.get("level", 1) * 100
        if "inventory" not in profile:
            profile["inventory"] = []
        return profile

def main():
    while True:
        print("\n--- Solo Leveling Habit Tracker (Terminal) ---")
        print("1. Show Habits")
        print("2. Add Habit")
        print("3. Delete Habit")
        print("4. Complete Habit")
        print("5. Show Completed Habits")
        print("6. Show Profile")
        print("7. Store")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            show_habits()
        elif choice == "2":
            add_habit_terminal()
        elif choice == "3":
            delete_habit_terminal()
        elif choice == "4":
            complete_habit_terminal()
        elif choice == "5":
            show_completed()
        elif choice == "6":
            show_profile_terminal()
        elif choice == "7":
            store_terminal()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()