import os
import sys
import time
import dotenv
import mariadb
import numpy as np
from loguru import logger


# Import adafruit_dht on Raspberry PI or a fake number generator
dotenv.load_dotenv()
if os.getenv("ISRPI") == "yes":
    logger.info("using adafruit_dht... (ISRPI=yes)")
    import kweed_utils.getth as getth
else:
    logger.info("DEMO MODE withotu adafruit_dht. It will generate random numbers (ISPRI<>yes)")
    import kweed_utils.getth_sim as getth


def db_cursor(islocal:bool = True) -> mariadb.connection.cursor:
    if islocal:
        user_ = os.getenv("DBUSER", "root")
        pass_ = os.getenv("DBPASS", "root")
        port_ = os.getenv("DBPORT", 3306)
        host_ = os.getenv("DBHOST", "localhost")
    else:
        #error prone, use for debug and testings only
        user_ = os.getenv("REMOTEDBUSER")
        pass_ = os.getenv("REMOTEDBPASS")
        port_ = os.getenv("REMOTEDBPORT")
        host_ = os.getenv("REMOTEDBHOST")

    try:
        connection = mariadb.connect(
            user=user_,
            password=pass_,
            host=host_,
            port=3306,
            database="rpi",
            autocommit=True,
        )
    except mariadb.Error as e:
        if islocal:
            logger.error(f"DATABASE ERROR:\n{e}")
        else:
            logger.debug(f"Remote database failure\n{e}")
        return False
    return connection.cursor()


def if_nan_go_null(value):
    if np.isnan(value):
        return "NULL"
    else:
        return np.float32(value)


def db_inserts(islocal:bool=True) -> None:
    cursor = db_cursor()
    if cursor:
        try:
            t = if_nan_go_null(getth.get_temp())
            h = if_nan_go_null(getth.get_humi())
            qry = f"INSERT INTO temphumi (temp, humi) VALUES ({t}, {h})"
            cursor.execute(qry)
            if __name__ == "__main__":
                logger.info(f"\nTimestamp: {time.strftime('%T')}\nTemperature: {t}C°  \nHumidity: {h} %")

        except ValueError as e:
            logger.error(f"Fail: \n{e}")
            sys.exit()


if __name__ == "__main__":
    db_inserts()
