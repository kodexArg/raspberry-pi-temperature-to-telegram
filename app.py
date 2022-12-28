import time
import logging
import sys
import os

import dotenv
import mariadb
import numpy as np

#Loading environment variables
dotenv.load_dotenv()

#Enable logging
logging.basicConfig(
        format"%(asctime)s - %(name)s - %(levelname)s - %(message)s"), level=logging.INFO
)
logger = logging.getLogger(__name__)

#Import adafruit_dht on Raspberry PI or a fake number generator
if os.getenv('ISRPI') == 'yes':
    print("using adafruit_dht... (ISRPI=yes)")
    import getth
else:
    print('using getth_sim to generate random numbers... (ISPRI<>yes)')
    import getth_sim as getth


def mariadb_cursor():
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
        print(f"Exit with error:\n{e}")
        sys.exit(1)

    return conn.cursor()


def if_nan_go_null(value):
    if np.isnan(value):
        return "NULL"
    else:
        return np.int32(value)


def mariadb_inserts():
    cur = mariadb_cursor()
    pause_seconds = 5
    while True:
        try:
            t = if_nan_go_null(getth.get_temp()) 
            h = if_nan_go_null(getth.get_humi())
            qry = f"INSERT INTO temphumi (temp, humi) VALUES ({t}, {h})"
            cur.execute(qry)
            if __name__ == "__main__":
                print(f"Timestamp: {time.strftime('%T')}\nTemperature: {t}C°  \nHumidity: {h} %")

        except ValueError as e:
            print(f"Fail: \n{e}")
        
        time.sleep(pause_seconds)


if __name__ == "__main__":
    print("Staring as __main__:")
    mariadb_inserts()
