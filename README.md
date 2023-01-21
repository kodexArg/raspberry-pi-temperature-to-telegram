### What do you need

**Raspberry PI 3+** with **any SO** will work as long as you can install python 3.9 on it. No GUI, please, it’s a Raspberry PI, you need all the available resources to get the job done.

The following guide assumes you already ran `sudo raspi-config` to setup your connection (wifi or ethernet), that hostname and localisation has been set and any configuration you thought were relevant for your device.

Check your internet and set up ssh with a custom key (this is not required but adviced).

You can follow any tutorial from the Web to reach to this point.

To sense **temperature** and **humidity** -and I bet you wish to- you’ll need a DHT11 or DHT22 sensor installed in your GPIO card. Again, follow any tutorial for this.

Same with the camera, you can use any device as long as it is supported by picamera module (and I bet it is indeed supported).

Once you get it done and connected via ssh you can continue with this guide.

### Initial setup

Update your OS from raspi-config or running something like:

`sudo apt update && sudo apt upgrade -y`

We gonna need the following packages:

`sudo apt install pyton3-pip git libgpiod2 libmariadb-dev mariadb-client mariadb-server` 

Create the /App folder with running privileges:

 `sudo mkdir /App && sudo chmod o=rwx /App`.

Get the app from github:

`git clone https://github.com/kodexArg/raspberry-temp-humi.git /App` 

Finally install the python required packages: 

`cd /App && pip install -r requirements.txt && pip install adafruit-circuitpython-dht`

***Ipython*** is not strictly necessary but usefull for debugin: like testing DHT sensor, database connection, etcetera. Install it now with `pip install ipython` or use the default ************python************ binary.

We got what we need. Let’s do some testing before configuring the application.

### Checkpoint: test DHT11/22 module

run **************ipython************** or python:

```python
In [1]: import adafruit_dht

In [2]: import board

In [3]: dht = adafruit_dht.DHT22(board.D4) #or adafruit_dht.DHT11(...)

In [4]: dht.temperature
Out[4]: 25.1
```

### Setup mariadb

You’re about to create the following structure:

```bash
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

So in order to get this done run `sudo mysql_secure_installation` and follow the assistant. Then run these commands using your username and passward (user kodex pass kodex for this example):

```bash
sudo mariadb -e "GRANT ALL PRIVILEGES ON *.* TO 'kodex'@'localhost' IDENTIFIED BY 'kodex'"

sudo mariadb -e "CREATE DATABASE rpi"

mariadb -u kodex -pkodex rpi < /App/installation/rpi.sql
```
