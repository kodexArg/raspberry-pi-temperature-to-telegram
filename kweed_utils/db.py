import os
import sys
import time
import dotenv
import mariadb
import numpy as np
from loguru import logger
from sqlalchemy import create_engine


# Import adafruit_dht on Raspberry PI or a fake number generator
if os.getenv("ISRPI") == "yes":
    logger.info("using adafruit_dht... (ISRPI=yes)")
    import kweed_utils.getth as getth
else:
    logger.info("DEMO MODE withotu adafruit_dht. It will generate random numbers (ISPRI<>yes)")
    import kweed_utils.getth_sim as getth


# def get_mariadb_data():
#     conn_local = f"mariadb+mariadbconnector://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}/rpi"
#     conn_remote = f"mariadb+mariadbconnector://{os.getenv('REMOTEDBUSER')}:{os.getenv('REMOTEDBPASS')}@{os.getenv('REMOTEDBHOST')}/rpi"
#     engine = create_engine(conn_str)


def db_cursor() -> mariadb.connection.cursor:
    try:
        dotenv.load_dotenv()
        conn_local = mariadb.connect(
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

    # try:
    #     conn_remote = mariadb.connect(
    #         user=os.getenv("REMOTEDBUSER", "root"),
    #         password=os.getenv("REMOTEDBPASS", "root"),
    #         host=os.getenv("REMOTEDBHOST", "localhost"),
    #         port=3306,
    #         database="rpi",
    #         autocommit=True,
    #     )
    
    # except mariadb.Error as e:
    #     logger.error(f"Connection fail to remote database...")
        
        


def if_nan_go_null(value):
    if np.isnan(value):
        return "NULL"
    else:
        return np.int32(value)


def db_inserts() -> None:
    cur = db_cursor()
    try:
        t = if_nan_go_null(getth.get_temp())
        h = if_nan_go_null(getth.get_humi())
        qry = f"INSERT INTO temphumi (temp, humi) VALUES ({t}, {h})"
        cur.execute(qry)
        if __name__ == "__main__":
            logger.info(f"\nTimestamp: {time.strftime('%T')}\nTemperature: {t}C°  \nHumidity: {h} %")

    except ValueError as e:
        logger.error(f"Fail: \n{e}")
        # todo: sending error to telegram?
        sys.exit()


if __name__ == "__main__":
    db_inserts()
