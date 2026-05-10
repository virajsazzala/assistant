import json

MEMORY_FILE = "./memory/user_profile.json"

def load_user_profile():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)

    except Exception as e:
        print(f"Memory Error: {e}")
        return {}