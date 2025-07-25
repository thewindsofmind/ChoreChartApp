# views/chart_view.py

import tkinter as tk
from tkinter import messagebox
from utils import data_manager
import pyttsx3


# --- A simple Tooltip class for hover-over text ---
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"), wraplength=250)
        label.pack(ipadx=1)

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None


def speak_text(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"An error occurred with the TTS engine: {e}")
        messagebox.showerror("TTS Error", "Could not initialize the text-to-speech engine.")


def show_chart(child_info, root):
    """Displays the chore chart with tooltips for reasoning."""
    progress_data = data_manager.load_progress(child_info['id'])
    chart_window = tk.Toplevel(root)
    chart_window.title(f"{child_info['name']} Chore Chart")
    chart_window.geometry("600x700")

    def on_closing():
        root.destroy()

    chart_window.protocol("WM_DELETE_WINDOW", on_closing)

    def save_and_update_display():
        data_manager.save_progress(child_info['id'], progress_data)
        weekly_goal = data_manager.WEEKLY_STAR_GOALS.get(child_info['id'], 0)
        stars_var.set(f"Stars Earned This Week: {progress_data.get('weekly_stars', 0)}")
        goal_var.set(f"Weekly Goal: {progress_data.get('weekly_stars', 0)} / {weekly_goal} stars")
        current_reward_text = "Keep going! No rewards reached yet."
        child_reward_tiers = data_manager.REWARD_TIERS.get(child_info['id'], [])

        # --- THIS IS THE FIX ---
        # The variable typo 'child_reward_' has been corrected to 'child_reward_tiers'.
        for tier in reversed(child_reward_tiers):
            if progress_data.get('weekly_stars', 0) >= tier['stars']:
                current_reward_text = f"✅ Current Reward: {tier['reward']}"
                break
        reward_var.set(current_reward_text)

    def complete_chore(chore):
        progress_data["weekly_stars"] += chore['stars']
        if chore['frequency'] == 'daily':
            progress_data['completed_daily_tasks'].append(chore['id'])
        else:
            progress_data['completed_weekly_tasks'].append(chore['id'])
        save_and_update_display()
        messagebox.showinfo("Chore Complete!", f"You earned {chore['stars']} stars for '{chore['name']}'!")
        display_chores(scrollable_frame)

    def manual_reset_week():
        if messagebox.askyesno("Confirm Reset",
                               "Are you sure you want to reset the entire week? This will set stars and all tasks to zero."):
            progress_data["weekly_stars"] = 0
            progress_data["completed_weekly_tasks"] = []
            progress_data["completed_daily_tasks"] = []
            save_and_update_display()
            display_chores(scrollable_frame)
            messagebox.showinfo("Reset Complete", "The week has been reset!")

    header_frame = tk.Frame(chart_window)
    header_frame.pack(pady=10, fill="x")
    container = tk.Frame(chart_window)
    container.pack(fill="both", expand=True)
    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(header_frame, text=f"{child_info['name']}'s Chore Chart", font=("Helvetica", 18, "bold")).pack()
    stars_var = tk.StringVar()
    tk.Label(header_frame, textvariable=stars_var, font=("Helvetica", 16)).pack()
    goal_var = tk.StringVar()
    tk.Label(header_frame, textvariable=goal_var, font=("Helvetica", 12)).pack()
    reward_var = tk.StringVar()
    tk.Label(header_frame, textvariable=reward_var, font=("Helvetica", 12, "italic"), fg="purple").pack(pady=5)

    def display_chores(parent_frame):
        for widget in parent_frame.winfo_children():
            widget.destroy()
        child_chores = sorted(data_manager.get_chores_for_child(child_info['chore_key']), key=lambda x: x['name'])

        for frequency in ["daily", "weekly"]:
            tk.Label(parent_frame, text=f"{frequency.title()} Chores", font=("Helvetica", 14, "bold")).pack(anchor="w",
                                                                                                            pady=(10,
                                                                                                                  5),
                                                                                                            padx=5)

            for chore in [c for c in child_chores if c['frequency'] == frequency]:
                chore_display_frame = tk.Frame(parent_frame, bd=1, relief="solid", padx=5, pady=5)
                chore_display_frame.pack(fill="x", pady=2, padx=5)
                left_frame = tk.Frame(chore_display_frame)
                left_frame.pack(side=tk.LEFT, fill="x", expand=True)

                text_to_speak = f"{chore['name']}. {chore.get('reasoning', '')}"

                speaker_button = tk.Button(left_frame, text="🔊", font=("Helvetica", 12),
                                           command=lambda text=text_to_speak: speak_text(text), relief="flat")
                speaker_button.pack(side=tk.LEFT, padx=(0, 5))

                name_label = tk.Label(left_frame,
                                      text=f"{chore.get('emoji', '')} {chore['name']} ({'⭐' * chore['stars']})",
                                      anchor="w", font=("Helvetica", 11))
                name_label.pack(side=tk.LEFT)

                reasoning_text = chore.get("reasoning", "")
                if reasoning_text:
                    ToolTip(name_label, text=f"Why it's important: {reasoning_text}")

                right_frame = tk.Frame(chore_display_frame)
                right_frame.pack(side=tk.RIGHT)
                is_maxed_out, status_text = False, ""
                if frequency == 'daily':
                    completions = progress_data['completed_daily_tasks'].count(chore['id'])
                    limit = chore.get('limit_per_day', 1)
                    if completions >= limit:
                        is_maxed_out = True
                    status_text = f"({completions}/{limit})"
                elif frequency == 'weekly':
                    if chore['id'] in progress_data['completed_weekly_tasks']:
                        is_maxed_out = True
                if is_maxed_out:
                    tk.Label(right_frame, text="MAX DONE!", fg="green", font=("Helvetica", 10, "bold")).pack()
                else:
                    tk.Button(right_frame, text="Mark Complete", command=lambda c=chore: complete_chore(c)).pack(
                        side=tk.RIGHT)
                    if status_text:
                        tk.Label(right_frame, text=status_text, font=("Helvetica", 10)).pack(side=tk.RIGHT, padx=5)

    display_chores(scrollable_frame)
    save_and_update_display()

    tk.Button(chart_window, text="Reset Week (Parents Only)", command=manual_reset_week, bg="#ffdddd").pack(pady=10,
                                                                                                            side=tk.BOTTOM)