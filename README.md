# raspberry-temp-humi
Raspberry Temperature Humidity

## Installation:

### Create environments
touch .env file in your project folder with these variables:
DBUSER=...
DBPASS=...
DBHOST=localhost
ISRPI=1 for Raspberry, 0 for developer computer. // Switching ISRPI to use getth_sim.py or getth.py. The last one will use adafruit_dht library, only available for Raspberry Pi (as long as I know...)

### Run it as a service in your Raspberry pi
You can use the sample file 'raspberry-temp-humi.service'. I'm soft-linking this file in /etc/systemd/system.

```
ln -s /home/$USER/app/raspberry-temp-humi/raspberry-temp-humi.service
```
