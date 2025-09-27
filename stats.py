import json
import os
from ai import calculate_exp, generate_motivation

PROFILE_FILE = "profile.json"
STATS_FILE = "stats.json"

def load_profile():
    if not os.path.exists(PROFILE_FILE):
        return {
            "username": "Usta",
            "level": 1,
            "exp": 0,
            "completed_habits": 0,
            "streak": 0,
            "rank": "E-rank Hunter"
        }
    with open(PROFILE_FILE, "r") as f:
        return json.load(f)

def save_profile(profile):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f, indent=4)

def get_rank(level):
    if level < 20:
        return "E-rank Hunter"
    elif level < 40:
        return "D-rank Hunter"
    elif level < 50:
        return "C-rank Hunter"
    elif level < 60:
        return "B-rank Hunter"
    elif level < 70:
        return "A-rank Hunter"
    else:
        return "S-rank Hunter"

def add_exp(profile, points):
    profile["exp"] += points
    leveled_up = False

    while profile["exp"] >= profile["level"] * 100:
        profile["exp"] -= profile["level"] * 100
        profile["level"] += 1
        profile["rank"] = get_rank(profile["level"])
        leveled_up = True

    save_profile(profile)
    return leveled_up

def complete_habit_stat(habit_name, current_level, stats):
    # --- EXP from AI ---
    gained_exp = calculate_exp(habit_name, current_level)
    stats["exp"] += gained_exp

    # --- Level up check ---
    level_up = False
    motivation_msg = None
    if stats["exp"] >= stats["next_level_exp"]:
        stats["level"] += 1
        stats["exp"] -= stats["next_level_exp"]
        stats["next_level_exp"] = int(stats["next_level_exp"] * 1.5)

        # AI motivational message
        motivation_msg = generate_motivation(stats["level"], habit_name)
        level_up = True

    save_stats(stats)

    return {
        "gained_exp": gained_exp,
        "level_up": level_up,
        "motivation": motivation_msg
    }

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)

def show_profile():
    profile = load_profile()
    level_bar_length = 20
    progress = int((profile["exp"] / (profile["level"] * 100)) * level_bar_length)
    bar = "█" * progress + "-" * (level_bar_length - progress)
    return (
        f"👤 {profile['username']}\n"
        f"⭐ Level: {profile['level']} ({profile['rank']})\n"
        f"💠 EXP: [{bar}] {profile['exp']}/{profile['level']*100}\n"
        f"✅ Completed Habits: {profile['completed_habits']}\n"
        f"🔥 Streak: {profile['streak']} days"
    )
