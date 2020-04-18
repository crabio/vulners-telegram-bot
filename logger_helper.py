import logging


def create_logger(name, level=logging.INFO):
    # Create  logging format
    format = logging.Formatter(
        '%(asctime)s - %(name)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    )
    # Get logger
    logger = logging.getLogger(name)
    # Set logger level
    logger.setLevel(level)
    # Create logger console stream handler
    c_handler = logging.StreamHandler()
    # Set console logger level
    c_handler.setLevel(level)
    # Set console logger format
    c_handler.setFormatter(format)
    # Add console logger into main logger
    logger.addHandler(c_handler)

    return logger
