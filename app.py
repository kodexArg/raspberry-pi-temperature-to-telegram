import sys
import os
import time

from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger
import dotenv
import mariadb
import numpy as np

# Loading environment and global variables
dotenv.load_dotenv()
start_time = time.time()


# Import adafruit_dht on Raspberry PI or a fake number generator
if os.getenv("ISRPI") == "yes":
    logger.info("using adafruit_dht... (ISRPI=yes)")
    import getth
else:
    logger.info("DEMO MODE withotu adafruit_dht. It will generate random numbers (ISPRI<>yes)")
    import getth_sim as getth


def mariadb_cursor() -> mariadb.Cursor:
    try:
        conn = mariadb.connect(
            user=os.getenv("DBUSER", "root"),
            password=os.getenv("DBPASS", "root"),
            host=os.getenv("DBHOST", "localhost"),
            port=3306,
            database="rpi",
            autocommit=True,
        )

    except mariadb.Error as e:
        logger.error(f"Exit with error:\n{e}")
        sys.exit(1)

    return conn.cursor()


def if_nan_go_null(value):
    if np.isnan(value):
        return "NULL"
    else:
        return np.int32(value)


def mariadb_inserts() -> None:
    cur = mariadb_cursor()
    try:
        t = if_nan_go_null(getth.get_temp())
        h = if_nan_go_null(getth.get_humi())
        qry = f"INSERT INTO temphumi (temp, humi) VALUES ({t}, {h})"
        cur.execute(qry)
        if __name__ == "__main__":
            logger.debug(f"\nTimestamp: {time.strftime('%T')}\nTemperature: {t}C°  \nHumidity: {h} %")

    except ValueError as e:
        logger.error(f"Fail: \n{e}")
        # todo: sending error to telegram?
        sys.exit()


def background_write_to_database():
    scheduler = BackgroundScheduler(timezone=utc)
    scheduler.add_job(mariadb_inserts, "interval", seconds=5)
    scheduler.start()


if __name__ == "__main__":
    logger.info("Staring as __main__:")
    background_write_to_database()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            logger.warning("Exit with KeyboardInterrupt")
            sys.exit(-1)