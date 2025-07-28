import logging
import os

def setup_logger():
    logger = logging.getLogger("BinanceBot")
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(log_level)

    if not logger.handlers:
        fh = logging.FileHandler("bot.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger