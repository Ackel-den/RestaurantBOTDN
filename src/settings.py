import os

from dotenv import load_dotenv


class Settings:
    load_dotenv()

    def __init__(self):
        self.bot_token = os.getenv("token")
        self.time_start = os.getenv("work_start")
        self.time_end = os.getenv("work_end")
