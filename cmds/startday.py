from ops.greeting import get_greeting
from ops.datetime_info import get_datetime_info
from ops.todos import get_today_todos
from ops.about_user import get_about_user

from utils.prompt_builder import build_startday_prompt
from utils.llm import ask_llm
from utils.speak import speak


def start_day():

    context = {
        "greeting": get_greeting(),
        "datetime": get_datetime_info(),
        "todos": get_today_todos(),
        "user": get_about_user()
    }

    prompt = build_startday_prompt(context)

    response = ask_llm(prompt)

    speak(response)