import logging
import requests
import xml.etree.ElementTree as ET

from collections import deque
from message import Message
from logger_helper import create_logger


class Parser:
    def __init__(self, siteUrl, storageMaxLen=100, debug=False):
        self._messagesStorage = deque(maxlen=storageMaxLen)
        self._siteUrl = siteUrl

        self._logger = create_logger("parser")
        if debug:
            self._logger = create_logger("parser", logging.DEBUG)

    def request_data(self):
        response = requests.get(self._siteUrl,
                                params={
                                    'query': '((type:mscve AND cvss.score:[8 TO 10]) OR (type:cve AND description:Microsoft AND cvss.score:[8 TO 10])) order:published'
                                })

        if response.status_code == 200:
            return self.parse_data(response.content)
        else:
            self._logger.error(
                'Failed getting responce from: %s' % self._siteUrl)

    def parse_data(self, dataText):
        self._logger.info("Parse data")
        root = ET.fromstring(dataText)

        # List of new messages
        new_messages = []

        for item in root[0].findall('item'):

            message = Message(item)

            if message.title not in self._messagesStorage:
                self._logger.debug("Add new message: %s" % message.title)
                self._messagesStorage.append(message.title)
                new_messages.append(message.to_message())
            else:
                self._logger.debug("Message exists: %s" % message.title)

        return new_messages
