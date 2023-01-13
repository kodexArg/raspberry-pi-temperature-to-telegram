import sys
import time
from loguru import logger
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
import dotenv
import numpy as np
from telegram_bot import main as tel_bot

from db import db_inserts

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
