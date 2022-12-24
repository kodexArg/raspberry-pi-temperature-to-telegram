# raspberry-temp-humi
Raspberry Temperature Humidity

## Installation:
### Create Mariadb database
Install mariadb in your raspberry pi with the folowing structure:
database name: rpi
table name: temphumi

```
+-------+---------------------+------+-----+---------------------+----------------+
| Field | Type                | Null | Key | Default             | Extra          |
+-------+---------------------+------+-----+---------------------+----------------+
| id    | bigint(20) unsigned | NO   | PRI | NULL                | auto_increment |
| temp  | float               | YES  |     | NULL                |                |
| humi  | float               | YES  |     | NULL                |                |
| time  | timestamp           | NO   |     | current_timestamp() |                |
+-------+---------------------+------+-----+---------------------+----------------+

```
Create a custom user and grant privileges on rpi.*.


### Create environments
Touch .env to create a file in your project folder and with these variables:
DBUSER=...
DBPASS=...
DBHOST=localhost
ISRPI=1 for Raspberry, 0 for developer computer. // Switching ISRPI to use getth_sim.py or getth.py. The last one will use adafruit_dht library, only available for Raspberry Pi (as long as I know...)

### Run it as a service
Set this script to autostart with your raspberry pi. Eighter load it using crontab or create a service for better control as I did. For this, you can use the sample file 'raspberry-temp-humi.service' included in this app. I'm soft-linking this file in /etc/systemd/system.

```
ln -s /home/$USER/app/raspberry-temp-humi/raspberry-temp-humi.service
```
