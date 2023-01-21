from time import sleep
import board
import adafruit_dht
import numpy as np
import dotenv
import os

ATTEMPT = 5
TIME_RETRY = 1

if os.getenv("DHT") == 11:
    dht = adafruit_dht.DHT11(board.D4, use_pulseio=False)
else:
    dht = adafruit_dht.DHT22(board.D4, use_pulseio=False)


def dht_reading(ask_for):
    for attempt in range(ATTEMPT):
        try:
            if ask_for == "temperature":
                val = np.int32(dht.temperature)
            elif ask_for == "humidity":
                val = np.int32(dht.humidity)
            else:
                raise Exception('Valid choices are "temperature" or "humidity"')
        except:
            val = np.nan
            print(f"fail reading in attempt {attempt+1}")
            sleep(TIME_RETRY)

        if not np.isnan(val):
            break

    return val


def get_temp():
    return dht_reading("temperature")   


def get_humi():
    return dht_reading("humidity")  


def getth():
    t, h = get_temp(), get_humi()
    return t, h


if __name__ == "__main__":
    print(f"temperature:{get_temp()}")
    print(f"humidity:{get_humi()}")

