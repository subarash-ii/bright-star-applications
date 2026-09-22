from datetime import datetime

def remove_at(text):
    if text.startswith("@"):
        return text.replace("@", "")

    return text


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False