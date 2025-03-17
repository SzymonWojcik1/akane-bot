import json
import os

def load_users(path, users_file):
    """
    Load users from json file or create an empty one if it does not exist
    :Args
      path : path to the file
      users_file : name of the file that it checks if it exists or needs to create
    :Retruns
      dict : Dict of users
    """
    file_and_path = os.path.join(path, users_file)

    if not os.path.exists(file_and_path):
        with open(file_and_path, "w") as f:
            json.dump({}, f)

    with open(file_and_path, "r") as f:
        return json.load(f)

def save_user(users, path, users_file):
    """
    Save user to the file
    :Args
      users : dict of users to save into the file
      path : path to the file
      users_file : name of the file that it checks if it exists or needs to create
    """
    file_and_path = os.path.join(path, users_file)

    with open(file_and_path, "w") as f:
        json.dump(users, f, indent=4)

def load_cards(cards_path):
    """
    Load the card set from a json file
    :Args
      cards_path : path to the cards json file
    :Returns
      dict : Cards data
    """
    if not os.path.exists(cards_path):
        raise FileNotFoundError(f"Card file '{cards_path}' not found!")
    with open(cards_path, "r") as f:
        return json.load(f)

def handle_user_json(user_id, path, users_file, cards_path):
    """
    Check if user exists, if not add them
    :Args
      user_id : user_id to add to the file or check if they exists
      path : path to the file
      users_file : name of the file that it checks if it exists or needs to create
    """
    users = load_users(path, users_file)

    if user_id not in users:
        cards = load_cards(cards_path)

        users[user_id] = {
            "packs_opened": 0,
            "base_set" : cards
            }
        save_user(users, path, users_file)
        return f"User {user_id} has been added!"
    return f"User {user_id} already exists"

def increment_packs_opened(user_id, path, users_file):
    """
    Increment by one the number of packs opened by a user

    :Args
      user_id : The user ID to update
      path : Path to the users file
      users_file : Name of the users file
    """
    users = load_users(path, users_file)

    if user_id in users:
        users[user_id]["packs_opened"] += 1 # Increment pack count
        save_user(users,path,users_file)