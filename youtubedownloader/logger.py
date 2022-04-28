import logging

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(levelname)s %(name)s: %(message)s")
)

def create_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
