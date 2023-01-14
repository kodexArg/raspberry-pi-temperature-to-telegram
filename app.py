"""App.py

The app runs a mariadb insert loops (background_write_to_database function) and initiate telegram
bot (tel_bot function) that listen commands.

The loop injecting SQL to mariadb database with temperature and humidity values from adafruit_dht.

Telegram bot (from telegram_bot.py) has two main functions: take a picture using the first default
device (usually a raspberry pi camera) and read mariadb in order to create a chart from its data,
prepare it and send as a image file to telegram.

"""

import time
from loguru import logger
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
import dotenv

from kweed_utils.telegram_bot import main as tel_bot
from kweed_utils.db import db_inserts

# Loading environment and global variables
dotenv.load_dotenv()
start_time = time.time()


def background_write_to_database():
    scheduler = BackgroundScheduler(timezone=utc)
    scheduler.add_job(db_inserts, "interval", seconds=5)
    scheduler.start()


if __name__ == "__main__":
    logger.info("Staring...")
    background_write_to_database()
    tel_bot()
