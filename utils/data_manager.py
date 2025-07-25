# utils/data_manager.py

import json
import os
from datetime import datetime

DATA_DIR = "data"

# --- CHORES DATABASE ---
# Added the new trash chore and a 'reasoning' key to the 9-year-old's tasks.
CHORES_DATA = [
    # Daily Chores
    {"id": "make_bed", "name": "Make Your Bed", "emoji": "🛏️", "stars": 2, "assigned_to": ["6yo", "9yo"],
     "frequency": "daily", "limit_per_day": 1, "instructions": "Pull your blanket all the way up to your pillows.",
     "reasoning": "Starting the day with a made bed makes your whole room feel cleaner and more organized."},
    {"id": "put_away_clothes", "name": "Clothes Off The Floor", "emoji": "👕", "stars": 2, "assigned_to": ["6yo", "9yo"],
     "frequency": "daily", "limit_per_day": 1,
     "instructions": "Put dirty clothes in the basket. Put clean clothes in your drawer.",
     "reasoning": "This keeps our clothes from getting wrinkled and makes the room easy to walk through without tripping."},
    {"id": "pick_up_toys", "name": "Toys Off The Floor", "emoji": "🧸", "stars": 2, "assigned_to": ["6yo", "9yo"],
     "frequency": "daily", "limit_per_day": 1,
     "instructions": "Put all your toys and books back where they belong so the floor is clean.",
     "reasoning": "This keeps your important things from getting stepped on and broken, and makes them easy to find later."},
    {"id": "clear_plate", "name": "Bring Plate to Kitchen", "emoji": "🍽️", "stars": 1, "assigned_to": ["6yo", "9yo"],
     "frequency": "daily", "limit_per_day": 3,
     "instructions": "After you eat, carry your plate, cup, and fork to the kitchen counter.",
     "reasoning": "Doing this right away helps keep the table clean for everyone and stops food from getting hard to clean up later."},
    {"id": "hang_towels", "name": "Hang Up Your Wet Towel", "emoji": "🛁", "stars": 1, "assigned_to": ["6yo", "9yo"],
     "frequency": "daily", "limit_per_day": 1,
     "instructions": "Make sure your big towel is hanging on the hook or bar so it can dry.",
     "reasoning": "Hanging your towel lets it dry properly so it doesn't get a yucky, musty smell."},
    {"id": "wipe_bathroom_sink", "name": "Wipe the Bathroom Sink", "emoji": "💧", "stars": 1, "assigned_to": ["9yo"],
     "frequency": "daily", "limit_per_day": 2,
     "instructions": "Use a cloth to wipe up all the toothpaste and water spots from the sink.",
     "reasoning": "This keeps the sink clean for the next person and prevents toothpaste from drying into hard-to-clean spots."},

    # Weekly Chores
    {"id": "bedroom_sweep", "name": "Sweep Your Bedroom Floor", "emoji": "🧹", "stars": 3, "assigned_to": ["9yo"],
     "frequency": "weekly",
     "instructions": "Sweep all the dust from the corners into a pile in the middle and use the dustpan.",
     "reasoning": "Sweeping gets rid of dust and dirt that can make us sneeze and helps keep our socks clean."},
    {"id": "bedroom_dust", "name": "Dust Your Dresser", "emoji": "✨", "stars": 2, "assigned_to": ["6yo"],
     "frequency": "weekly", "instructions": "Use the fluffy duster to wipe the top of your dresser and nightstand."},
    {"id": "common_tidy", "name": "Living Room Speed Clean", "emoji": "🛋️", "stars": 3, "assigned_to": ["6yo", "9yo"],
     "frequency": "weekly",
     "instructions": "Help for 10 minutes! Put blankets, pillows, and books back where they go in the living room.",
     "reasoning": "When we all help for a few minutes, it makes our shared family space nice and relaxing for everyone to enjoy."},
    {"id": "vacuum_rugs", "name": "Vacuum the Rugs", "emoji": "💨", "stars": 3, "assigned_to": ["9yo"],
     "frequency": "weekly", "instructions": "Use the vacuum to clean the rugs in your room and the living room.",
     "reasoning": "Vacuuming pulls deep-down dirt and dust out of the rugs, which keeps the air in our house cleaner to breathe."},
    {"id": "empty_trash", "name": "Empty Little Trash Cans", "emoji": "🗑️", "stars": 2, "assigned_to": ["6yo"],
     "frequency": "weekly",
     "instructions": "Take the trash bags from your room and the bathroom to the big kitchen trash can."},
    {"id": "kitchen_sweep_swiffer", "name": "Sweep & Mop the Kitchen", "emoji": "🧼", "stars": 4, "assigned_to": ["9yo"],
     "frequency": "weekly",
     "instructions": "First, sweep the whole kitchen floor. Then, use the Swiffer to mop it clean.",
     "reasoning": "This gets rid of crumbs and sticky spots on the floor, which keeps our kitchen clean and helps keep it bug-free."},
    {"id": "laundry_gather", "name": "Bring Laundry Downstairs", "emoji": "🧺", "stars": 2, "assigned_to": ["6yo"],
     "frequency": "weekly",
     "instructions": "Go to all the laundry baskets and bring the dirty clothes to the laundry room."},
    {"id": "dust_living_room", "name": "Dust the TV Stand", "emoji": "📺", "stars": 2, "assigned_to": ["6yo"],
     "frequency": "weekly", "instructions": "Use the fluffy duster to wipe the TV stand and the coffee table."},
    {"id": "wipe_dining_table", "name": "Wipe the Big Table", "emoji": "🧽", "stars": 1, "assigned_to": ["6yo"],
     "frequency": "weekly", "instructions": "Use a damp cloth to wipe all the crumbs off the big eating table."},

    # --- NEW CHORE ---
    {"id": "bedroom_trash_wipe", "name": "Empty Room Trash & Wipe", "emoji": "🐜", "stars": 2, "assigned_to": ["9yo"],
     "frequency": "weekly",
     "instructions": "Take the trash bag out of your can and wipe up any sticky spots on your desk or nightstand.",
     "reasoning": "This is important because leftover food wrappers and spills can attract ants and other bugs into your room."}
]

# --- REWARD AND GOAL CONFIGURATION ---
WEEKLY_STAR_GOALS = {"dino": 25, "space": 50}
REWARD_TIERS = {
    "dino": [
        {"stars": 4, "reward": "30 minutes extra screen time 📱"},
        {"stars": 7, "reward": "3 cookies or similar treat 🍪"},
        {"stars": 15, "reward": "Pick the movie for family movie night 🎬"},
        {"stars": 25, "reward": "Choose a special outing or $10 toy 🎁"}
    ], "space": [
        {"stars": 7, "reward": "Playground visit or a favorite treat 🍦"},
        {"stars": 15, "reward": "Choose dessert for one night 🍨"},
        {"stars": 25, "reward": "Get 30 minutes of extra screen time 📱"},
        {"stars": 40, "reward": "Pick the movie for family movie night 🎬"},
        {"stars": 50, "reward": "Trip to the movies or the mall! 🍿🛍️"}
    ]
}


# --- DATA MANAGEMENT FUNCTIONS ---
def load_progress(child_id):
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{child_id}_progress.json")
    if not os.path.exists(filepath): return {"weekly_stars": 0, "last_saved_date": "1970-01-01",
                                             "completed_daily_tasks": [], "completed_weekly_tasks": []}
    with open(filepath, "r") as f:
        data = json.load(f)
    today = datetime.now();
    last_saved_date = datetime.strptime(data.get("last_saved_date", "1970-01-01"), "%Y-%m-%d")
    if today.date() > last_saved_date.date(): data["completed_daily_tasks"] = []
    if today.weekday() == 0 and last_saved_date.isocalendar() != today.isocalendar():
        data["weekly_stars"] = 0;
        data["completed_weekly_tasks"] = []
    data["last_saved_date"] = today.strftime("%Y-%m-%d")
    return data


def save_progress(child_id, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{child_id}_progress.json")
    with open(filepath, "w") as f: json.dump(data, f, indent=4)


def get_chores_for_child(child_chore_key):
    return [chore for chore in CHORES_DATA if child_chore_key in chore.get("assigned_to", [])]