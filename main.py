from src import cynthiabot
import logging

logger = logging.getLogger("cynthiabot")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s:%(levelname)s:%(name)s:%(filename)s:%(lineno)s %(message)s"
    )
)
logger.addHandler(handler)

cynthiabot.start()
