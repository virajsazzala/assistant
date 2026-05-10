from datetime import datetime

def get_datetime_info():

    now = datetime.now()

    return {
        "day": now.strftime("%A"),
        "date": now.strftime("%d %B %Y"),
        "time": now.strftime("%I:%M %p")
    }