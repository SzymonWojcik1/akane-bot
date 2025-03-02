import json
import os

def load_config(filename='config.json'):
    try:
        with open(filename, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to parse {filename} as JSON.")
        return None

def load_data(filename):
    filepath = os.path.join("data", filename)

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            json.dump({}, f)
        return {}

    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_data(data, filename):
    filepath = os.path.join("data", filename)
    os.makedirs("data", exist_ok=True)

    with open(filepath, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def join_user(user, data, filename):
    if user not in data:
        data[user] = []
        save_data(data,filename)
        return True
    else:
        return False
