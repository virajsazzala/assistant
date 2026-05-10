from datetime import datetime

from integrations.notion import NotionAgenda

agenda = NotionAgenda()

def get_today_todos():
    current_day = datetime.now().strftime("%A")
    todos = agenda.get_day_todos(current_day)

    return {
        "day": current_day,
        "todos": todos
    }

def get_week_todos():
    return agenda.get_week_todos()