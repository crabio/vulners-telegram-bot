from logger_helper import create_logger
from bot import Bot
from parser import Parser
import threading
import logging
import os


if __name__ == '__main__':
    SITE_URL = os.environ.get('SITE_URL')
    STORAGE_MAX_LEN = int(os.environ.get('STORAGE_MAX_LEN'))
    WAIT_TIME_SECONDS = int(os.environ.get('WAIT_TIME_SECONDS'))
    LOGGING_DEBUG = True if os.environ.get('LOGGING_DEBUG') else False
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

    # Parser object
    parser = Parser(SITE_URL, STORAGE_MAX_LEN, LOGGING_DEBUG)
    # Telegram Bot
    bot = Bot(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, LOGGING_DEBUG)

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


async def main(loop, logger):
    # Check environment variables
    # Debug logging level option
    if os.environ.get('LOGGING_LEVEL') == "DEBUG":
        logger = create_logger("main", logging.DEBUG)
    # NATS broker config
    nats_host = os.environ.get('NATS_HOST') if os.environ.get(
        'NATS_HOST') else "localhost"
    nats_port = os.environ.get('NATS_PORT') if os.environ.get(
        'NATS_PORT') else 4222
    # Forks searcher options
    profit_percentage_threshold = float(
        os.environ.get('PROFIT_PERCENTAGE_THRESHOLD')) if os.environ.get(
            'PROFIT_PERCENTAGE_THRESHOLD') else 0.05
    old_data_cleaning_threshold_s = int(
        os.environ.get('OLD_DATA_CLEANING_TTL_S')) if os.environ.get(
            'OLD_DATA_CLEANING_TTL_S') else 3600
    # Init Fork Searcher class
    fork_searcher = await ForkSearcher.create(
        loop,
        nats_host=nats_host,
        nats_port=nats_port,
        profit_percentage_threshold=profit_percentage_threshold,
        old_data_threshold_s=old_data_cleaning_threshold_s,
        logger=logger)
    # Run infinite loop
    await fork_searcher.run()
    # Close all connections
    await fork_searcher.close()
    logger.info("Closed")


if __name__ == '__main__':
    logger = create_logger("main", logging.INFO)
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT,
                            functools.partial(shutdown, loop, logger))
    loop.add_signal_handler(signal.SIGHUP,
                            functools.partial(shutdown, loop, logger))
    loop.add_signal_handler(signal.SIGTERM,
                            functools.partial(shutdown, loop, logger))
    supervisor(loop, logger)
