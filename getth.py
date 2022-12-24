import board
import adafruit_dht
import numpy as np

dht = adafruit_dht.DHT11(board.D4)

def get_temp():
    try:
        t = np.float64(dht.temperature)
    except:
        t = np.nan
    return t


def get_humi():
    try:
        h = np.float64(dht.humidity)
    except:
        h = np.nan
    return h


def getth():
    t, h = get_temp(), get_humi()
    return t, h


if __name__ == "__main__":
    print(f"temperature:{get_temp()}")
    print(f"humidity:{get_humi()}")

