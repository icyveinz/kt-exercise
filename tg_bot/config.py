import os
from dotenv import load_dotenv

load_dotenv(".env")


class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TOKEN = os.getenv("TOKEN")

    @staticmethod
    def validate():
        if not Config.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN is not set in environment variables.")
        if not Config.TOKEN:
            raise ValueError("TOKEN is not set in environment variables.")


Config.validate()
