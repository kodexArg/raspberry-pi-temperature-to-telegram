# raspberry-temp-humi
Raspberry Temperature Humidity


.env:
  DBUSER=...
  DBPASS=...
  DBHOST=localhost
  ISRPI=1 for Raspberry, 0 for developer computer.
    # Switching ISRPI to use getth_sim.py or getth.py. The last one will use adafruit_dht library, only available for Raspberry Pi (as long as I know...)
