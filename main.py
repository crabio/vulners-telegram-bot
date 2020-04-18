from logger_helper import create_logger
from bot import Bot
from parser import Parser
import threading
import logging
import json
import os


if __name__ == '__main__':
    SITE_URL = os.environ.get('SITE_URL')
    STORAGE_MAX_LEN = int(os.environ.get('STORAGE_MAX_LEN'))
    WAIT_TIME_SECONDS = int(os.environ.get('WAIT_TIME_SECONDS'))
    LOGGING_DEBUG = True if os.environ.get('LOGGING_DEBUG') else False

    # Read config data
    config_json = {}
    with open("config.json") as json_file:
        config_json = json.load(json_file)
        # Check required fields
        if "TELEGRAM_TOKEN" not in config_json or\
            "TELEGRAM_CHAT_ID" not in config_json or\
                "SEARCH_QUERIES" not in config_json:
            raise RuntimeError("Not enough fields in config.json.")

    # Parser object
    parser = Parser(SITE_URL,
                    STORAGE_MAX_LEN,
                    LOGGING_DEBUG,
                    config_json["SEARCH_QUERIES"])
    # Telegram Bot
    bot = Bot(config_json["TELEGRAM_TOKEN"],
              config_json["TELEGRAM_CHAT_ID"],
              LOGGING_DEBUG)

    def process():
        # First data parsing
        new_messages = parser.request_data()
        # Send messages to Telegram
        for message in new_messages:
            bot.send(message)

    process()

    # Periodic data parsing
    ticker = threading.Event()
    while not ticker.wait(WAIT_TIME_SECONDS):
        process()
