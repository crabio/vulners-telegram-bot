import logging
import requests
from logger_helper import create_logger


class Bot:
    def __init__(self, token, chatId, debug=False):
        self._token = token
        self._chatId = chatId

        self._logger = create_logger("bot")
        if debug:
            self._logger = create_logger("bot", logging.DEBUG)

    def send(self, message):
        # sending message to user
        url = 'https://api.telegram.org/bot%s/sendMessage' % self._token
        post_data = {"chat_id": self._chatId, "text": message}
        response = requests.post(url, data=post_data)

        if response.status_code != 200:
            self._logger.error(
                "Failed to send  data  to Telegram bot: %s" % message)
        else:
            self._logger.debug("Message sended to Telegram: %s" % message)
