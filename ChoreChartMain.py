# ChoreChartMain.py

import tkinter as tk
from views.chart_view import show_chart

CHILD_PROFILES = {
    "dino": {"id": "dino", "name": "6-Year-Old", "chore_key": "6yo"},
    "space": {"id": "space", "name": "9-Year-Old", "chore_key": "9yo"}
}

def launch_chart(selected_child_id):
    """Finds the child's profile, hides the launcher, and shows their chart."""
    root.withdraw()
    child_info = CHILD_PROFILES.get(selected_child_id)
    if child_info:
        # --- THIS IS THE FIX ---
        # The 'root' window is now correctly passed as the second argument.
        show_chart(child_info, root)
    else:
        print(f"Error: No profile found for ID {selected_child_id}")
        root.destroy()

root = tk.Tk()
root.title("Chore Chart Launcher")
root.geometry("400x300")

child_choice = tk.StringVar(value="dino")
tk.Label(root, text="Choose Your Chore Explorer", font=("Helvetica", 16)).pack(pady=20)
tk.Radiobutton(root, text="🦕 6-Year-Old (Dino Explorer)", variable=child_choice, value="dino", font=("Helvetica", 12)).pack(anchor="w", padx=60, pady=5)
tk.Radiobutton(root, text="🚀 9-Year-Old (Astro Commander)", variable=child_choice, value="space", font=("Helvetica", 12)).pack(anchor="w", padx=60, pady=5)
tk.Button(
    root,
    text="Begin Chores!",
    font=("Helvetica", 14, "bold"),
    command=lambda: launch_chart(child_choice.get())
).pack(pady=40)

root.mainloop()