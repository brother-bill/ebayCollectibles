import pickle
from os.path import exists
import os
from collections import defaultdict
from pathlib import Path
from shutil import copy

# A with statement does not create a scope (like if, for, try/except and while do not create a scope either).

# Get real path to file and then append new directory name
new_items = os.path.dirname(os.path.realpath(__file__)) + "/" + "items"
new_logs = os.path.dirname(os.path.realpath(__file__)) + "/" + "logs"
# Make new directory
Path(new_items).mkdir(parents=True, exist_ok=True)
Path(new_logs).mkdir(parents=True, exist_ok=True)
# Directory of pickle file
dirof_item_results = new_items + "/" + "items.pkl"
dirof_history = new_logs + "/" + "history.txt"
dirof_id = new_logs + "/" + "item_id.txt"
dirof_log = new_logs + "/" + "log.txt"
# If file of items to read exists, then open it and set the list to equal what's inside the file, also make a backup
# Else create a new file and write a default dictionary of sets inside
item_results = defaultdict(set)
if exists(dirof_item_results):
    with open(dirof_item_results, "rb") as items_file:
        print("EXISTS")
        copy(dirof_item_results, new_items + "/" +"items_copy.pkl")
        items_results = pickle.load(items_file)
else:
    with open(dirof_item_results, "wb") as items_file:
        print("NOPE")
        pickle.dump(items_results, items_file, -1)

