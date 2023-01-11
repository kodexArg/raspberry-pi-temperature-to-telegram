import time
import sys
import os

from loguru import logger
import dotenv
import mariadb
import numpy as np

#Loading environment variables
dotenv.load_dotenv()


#Import adafruit_dht on Raspberry PI or a fake number generator
if os.getenv('ISRPI') == 'yes':
    logger.info("using adafruit_dht... (ISRPI=yes)")
    import getth
else:
    logger.info('using getth_sim to generate random numbers... (ISPRI<>yes)')
    import getth_sim as getth


def mariadb_cursor() -> mariadb.Cursor:
    try:
        conn = mariadb.connect(
            user = os.getenv('DBUSER','root'),
            password = os.getenv('DBPASS','root'),
            host = os.getenv('DBHOST','localhost'),
            port = 3306,
            database = "rpi",
            autocommit = True,
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
    while True:
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
        

def insert_loop(pause_seconds: float = 15) -> None:
    while True:
        mariadb_inserts()
        time.sleep(pause_seconds)


if __name__ == "__main__":
    logger.debug("Staring as __main__:")
    insert_loop(pause_seconds=15)
