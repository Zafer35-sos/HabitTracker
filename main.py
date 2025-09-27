import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
from habits import add_habit, read_habit, delete_habit, save_habit
from stats import complete_habit_stat, show_profile, load_profile,save_profile
from ai import calculate_exp, generate_motivation


class HabitTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Solo Leveling System")
        self.root.geometry("800x600")
        self.root.configure(bg="black")

        # --- Wallpaper ---
        try:
            bg_img = Image.open("wallpaper.png")
            bg_img = bg_img.resize((800, 600), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        except:
            self.bg_label = tk.Label(self.root, bg="black")
            self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # --- Custom Title Bar ---
        self.root.overrideredirect(True)

        title_bar = tk.Frame(self.root, bg="black")
        title_bar.pack(fill="x")

        tk.Label(
            title_bar, text="⚔️ Solo Leveling System ⚔️",
            fg="#00ffff", bg="black", font=("Courier", 14, "bold")
        ).pack(side="left", padx=10)

        btn_style = dict(bg="black", fg="#00ffff", bd=0, font=("Courier", 12, "bold"), width=3)

        min_btn = tk.Button(title_bar, text="—", **btn_style, command=self.minimize_window)
        min_btn.pack(side="right")

        max_btn = tk.Button(title_bar, text="⬜", **btn_style, command=self.toggle_fullscreen)
        max_btn.pack(side="right")

        close_btn = tk.Button(title_bar, text="X",
                              bg="black", fg="#ff3333", bd=0,
                              font=("Courier", 12, "bold"), width=3,
                              command=self.root.destroy)
        close_btn.pack(side="right")

        # --- Dragging window ---
        def start_move(e): self.x, self.y = e.x, e.y
        def do_move(e): self.root.geometry(f"+{e.x_root - self.x}+{e.y_root - self.y}")
        title_bar.bind("<Button-1>", start_move)
        title_bar.bind("<B1-Motion>", do_move)

        # --- Profile area ---
        self.profile_label = tk.Label(self.root, text="", justify="left",
                                      font=("Courier", 12), bg="#000000", fg="#ffffff")
        self.profile_label.pack(pady=10)

        # XP Bar (tek bar kalıyor)
        self.exp_var = tk.DoubleVar()
        self.exp_bar = ttk.Progressbar(self.root, orient="horizontal",
                                       length=300, mode="determinate",
                                       variable=self.exp_var, maximum=100)
        self.exp_bar.pack(pady=5)

        # --- Main Buttons ---
        btn_frame = tk.Frame(self.root, bg="#000000")
        btn_frame.pack(pady=20)

        self.make_button(btn_frame, "📜 Habits", self.open_habit_page, 0)
        self.make_button(btn_frame, "✅ Completed", self.open_completed_page, 1)
        self.make_button(btn_frame, "👤 Profile", self.open_profile_page, 2)
        self.make_button(btn_frame, "🏪 Store", self.open_store_page, 3)

        self.refresh_profile()

    def make_button(self, parent, text, command, col):
        btn = tk.Button(
            parent, text=text, command=command,
            bg="#000000", fg="#00ffff", width=15, bd=0,
            font=("Courier", 11, "bold"), activebackground="#111111", activeforeground="#00ffff"
        )
        btn.grid(row=0, column=col, padx=10, pady=5)
        return btn

    def refresh_profile(self):
        # ASCII EXP bar kaldırıldı
        profile = load_profile()
        display_text = (
            f"👤 {profile.get('name', 'Hunter')}\n"
            f"⭐ Level: {profile.get('level', 1)} ({profile.get('title', '')})\n"
            f"✅ Completed Habits: {profile.get('completed_habits', 0)}\n"
            f"🔄 Streak: {profile.get('streak', 0)} days"
        )
        self.profile_label.config(text=display_text)

        exp = profile.get("exp", 0)
        exp_to_next = profile.get("exp_to_next", 100)
        self.exp_var.set((exp / exp_to_next) * 100)

    def toggle_fullscreen(self):
        if not hasattr(self, "_is_fullscreen"):
            self._is_fullscreen = False
            self._prev_geometry = self.root.geometry()

        if self._is_fullscreen:
            self.root.geometry(self._prev_geometry)
        else:
            w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self._prev_geometry = self.root.geometry()
            self.root.geometry(f"{w}x{h}+0+0")

        self._is_fullscreen = not self._is_fullscreen

    def minimize_window(self):
        self.root.overrideredirect(False)
        self.root.iconify()
        self.root.after(10, lambda: self.root.overrideredirect(True))

    def open_habit_page(self):
        win = tk.Toplevel(self.root)
        win.title("Habits")
        win.geometry("500x400")
        win.configure(bg="black")

        habit_listbox = tk.Listbox(win, width=50, bg="#1e1e2f", fg="white", font=("Arial", 11))
        habit_listbox.pack(pady=10)

        data = read_habit()
        for i, habit in enumerate(data["habit"], start=1):
            habit_listbox.insert(tk.END, f"{i}. {habit}")

        tk.Button(win, text="Add Habit", command=lambda: self.add_habit_gui(habit_listbox),
                  bg="#ffaa00", fg="black").pack(pady=5)
        tk.Button(win, text="Delete Habit", command=lambda: self.delete_habit_gui(habit_listbox),
                  bg="#ff4444", fg="white").pack(pady=5)
        tk.Button(win, text="Complete Habit", command=lambda: self.complete_habit_gui(habit_listbox),
                  bg="#44ff44", fg="black").pack(pady=5)

    def open_completed_page(self):
        win = tk.Toplevel(self.root)
        win.title("Completed Habits")
        win.geometry("400x300")
        win.configure(bg="black")

        data = read_habit()
        completed = data.get("completed", [])
        if not completed:
            msg = "No completed habits."
        else:
            msg = "\n".join(f"{i+1}. {h}" for i, h in enumerate(completed))

        tk.Label(win, text=msg, bg="black", fg="white", font=("Courier", 11)).pack(pady=20)

    def add_habit_gui(self, listbox):
        habit_name = simpledialog.askstring("Add Habit", "Enter habit name:")
        if habit_name:
            add_habit(habit_name)
            self.refresh_profile()
            self.update_listbox(listbox)

    def delete_habit_gui(self, listbox):
        selection = listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a habit to delete")
            return
        index = selection[0] + 1
        result = delete_habit(index)
        messagebox.showinfo("Delete", result)
        self.update_listbox(listbox)
        self.refresh_profile()

    def complete_habit_gui(self, listbox):
        selection = listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Please select a habit to complete")
            return

        index = selection[0] + 1
        data = read_habit()
        if index <= len(data["habit"]):
            habit_name = data["habit"][index - 1]
            data.setdefault("completed", []).append(habit_name)
            del data["habit"][index - 1]
            save_habit(data)

            profile = load_profile()
            current_level = profile.get("level", 1)

            # Get EXP and motivation from AI
            result = complete_habit_stat(habit_name, current_level, profile)

            self.update_listbox(listbox)
            self.refresh_profile()

            if result["level_up"]:
                self.show_level_up(profile.get("level", 1), habit_name)
                messagebox.showinfo("LEVEL UP ⚔️",
                    f"You reached Level {profile.get('level', 1)}!\n\nMotivation:\n{result['motivation']}")
            else:
                messagebox.showinfo("Completed", f"{habit_name} completed! +{result['gained_exp']} EXP")

    def open_profile_page(self):
        win = tk.Toplevel(self.root)
        win.title("Profile")
        win.geometry("400x350")
        win.configure(bg="black")

        profile = load_profile()
        tk.Label(win, text=f"Username: {profile.get('username', 'Hunter')}", fg="#00ffff", bg="black", font=("Courier", 13)).pack(pady=10)
        tk.Label(win, text=f"Level: {profile.get('level', 1)} ({profile.get('rank', '')})", fg="gold", bg="black", font=("Courier", 12)).pack(pady=5)
        tk.Label(win, text=f"EXP: {profile.get('exp', 0)}", fg="white", bg="black", font=("Courier", 11)).pack(pady=5)
        tk.Label(win, text=f"Inventory: {', '.join(profile.get('inventory', []))}", fg="#ffaa00", bg="black", font=("Courier", 11)).pack(pady=10)

    def show_level_up(self, new_level, habit_name=""):
        profile = load_profile()
        title = profile.get("title", "Hunter")

        motivation = generate_motivation(new_level, habit_name)

        win = tk.Toplevel(self.root)
        win.title("Level Up!")
        win.geometry("450x250")
        win.configure(bg="black")

        tk.Label(win, text=f"⚔️ Level {new_level} ⚔️",
                 fg="#00ffff", bg="black",
                 font=("Courier", 16, "bold")).pack(pady=10)

        tk.Label(win, text=f"Ünvanın: {title}",
                 fg="gold", bg="black",
                 font=("Courier", 13)).pack(pady=5)

        tk.Label(win, text=f"『 {motivation} 』",
                 fg="white", bg="black",
                 font=("Courier", 11), wraplength=400, justify="center").pack(pady=15)

    def open_store_page(self):
        win = tk.Toplevel(self.root)
        win.title("Store")
        win.geometry("400x300")
        win.configure(bg="black")

        items = {"Potion": 50, "Sword": 100, "Shield": 80}
        profile = load_profile()

        def buy_item(item, cost):
            if profile.get("exp", 0) >= cost:
                profile["exp"] -= cost
                profile.setdefault("inventory", []).append(item)
                save_profile(profile)
                messagebox.showinfo("Store", f"You bought a {item}!")
                win.destroy()
            else:
                messagebox.showinfo("Store", "Not enough EXP!")

        for idx, (item, cost) in enumerate(items.items()):
            tk.Button(win, text=f"Buy {item} ({cost} EXP)", command=lambda i=item, c=cost: buy_item(i, c),
                      bg="#ffaa00", fg="black", font=("Courier", 11)).pack(pady=10)

    def update_listbox(self, listbox):
        if not listbox.winfo_exists():
            return
        listbox.delete(0, tk.END)
        data = read_habit()
        for i, habit in enumerate(data["habit"], start=1):
            listbox.insert(tk.END, f"{i}. {habit}")


if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTrackerGUI(root)
    root.geometry("800x600")
    root.mainloop()
