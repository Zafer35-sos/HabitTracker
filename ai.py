# ai.py (simple English version)
import ollama

MODEL_NAME = "gemma3"  # change if you prefer another model


def calculate_exp(habit_name: str, current_level: int) -> int:
    """
    Ask the AI to give EXP for a habit.
    The model must return ONLY a number.
    """
    resp = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an EXP calculator. Return only a number."},
            {"role": "user", "content": f"Habit: {habit_name}, Level: {current_level}\nReturn only EXP as a number."}
        ]
    )
    try:
        return int(resp["message"]["content"].strip())
    except:
        # fallback if AI fails
        return 10


def generate_motivation(level: int, habit_name: str) -> str:
    """
    Ask the AI for a short Solo Leveling–style motivation.
    """
    resp = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are the System from Solo Leveling. Speak epic and motivational in max 2 sentences."},
            {"role": "user", "content": f"The hunter reached Level {level} after completing '{habit_name}'. Write a motivational line."}
        ]
    )
    return resp["message"]["content"].strip()
