import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def add_record(record):
    history = load_history()
    # Add ID if not present (though we should generate it before calling this)
    history.insert(0, record) # Prepend to show newest first
    save_history(history)

def delete_records(ids):
    history = load_history()
    # Filter out records with IDs in the deletion list
    new_history = [r for r in history if r.get("id") not in ids]
    save_history(new_history)
    return len(history) - len(new_history)

def get_all_records():
    return load_history()

def get_records_by_ids(ids):
    history = load_history()
    return [r for r in history if r.get("id") in ids]
