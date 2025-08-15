import os

from dotenv import load_dotenv


class Settings:
    load_dotenv()
    def __init__(self):
        self.bot_token = os.getenv('TOKEN')
