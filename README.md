# raspberry-temp-humi
Raspberry Temperature and Humidity database

## Installation:
### Create Mariadb database
Install mariadb in your raspberry pi and create this structure:
```
database name: rpi
table name: temphumi
+-------+---------------------+------+-----+---------------------+----------------+
| Field | Type                | Null | Key | Default             | Extra          |
+-------+---------------------+------+-----+---------------------+----------------+
| id    | bigint(20) unsigned | NO   | PRI | NULL                | auto_increment |
| temp  | float               | YES  |     | NULL                |                |
| humi  | float               | YES  |     | NULL                |                |
| time  | timestamp           | NO   |     | current_timestamp() |                |
+-------+---------------------+------+-----+---------------------+----------------+
```
Create a custom user and grant privileges on 'rpi.*'.
To grant remote access to your database, you need to change your /etc/mysql/mariadb.conf from ```bind-address = 127.0.0.1``` to ```bind-address = 0.0.0.0```


### Create environments
```Touch .env``` to create a file in your project folder with the following variables:
```
DBUSER=...
DBPASS=...
DBHOST=localhost
ISRPI=1 for Raspberry, 0 for developer computer. // Switching ISRPI to use getth_sim.py or getth.py. The last one will use adafruit_dht library, only available for Raspberry Pi (as long as I know...)
```

### Run it as a service
Set this script to autostart with your raspberry pi. Either load it using crontab or create a service for better control as I did. For this, you can use the sample file 'raspberry-temp-humi.service' included in the folder app. I'm soft-linking this file in /etc/systemd/system and using it as is.
```
ln -s /home/$USER/app/raspberry-temp-humi/raspberry-temp-humi.service
```
