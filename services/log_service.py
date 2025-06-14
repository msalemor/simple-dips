import logging


def get_logger(name: str) -> logging.Logger:
    """Create and configure a logger with a console handler.
    Args:
        name (str): The name of the logger.
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    return logger
