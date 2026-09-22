import os
import json

from config import APPLICATIONS_PATH


def load_applications() -> dict[int, dict[int, int]]:
    if not os.path.exists(APPLICATIONS_PATH):
        return {}

    try:
        with open(APPLICATIONS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

            return {int(user_id): {int(admin_id): msg_id for admin_id, msg_id in admins.items()}
                    for user_id, admins in data.items()}
    except Exception as e:
        print(f"Failed to load applications: {e}")


def save_applications():
    try:
        with open(APPLICATIONS_PATH, "w", encoding="utf-8") as f:
            json.dump(APPLICATIONS_MESSAGES, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to save applications: {e}")


APPLICATIONS_MESSAGES: dict[int, dict[int, int]] = load_applications()