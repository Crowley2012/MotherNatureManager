from datetime import datetime, time
from influxdb import InfluxDBClient
from pyvesync import VeSync
from time import sleep

import board
import busio
import adafruit_ccs811
import Adafruit_DHT

# Sensor Setup
I2C = busio.I2C(board.SCL, board.SDA)
DHT_PIN = 4
DHT_SENSOR = Adafruit_DHT.DHT11
CCS811_SENSOR = adafruit_ccs811.CCS811(I2C)

# Database Setup
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('environments')

# Switch Setup
light = 0
fan = 0
humidifier = 0
manager = VeSync(, )
manager.login()
manager.update()

# Functions
def isTimeBetween(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:
        return check_time >= begin_time or check_time <= end_time

# Wait for the co2 sensor to be ready
while not CCS811_SENSOR.data_ready:
    pass

while True:
    try:
        humidity, tempC = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        tempF = (tempC * (9/5)) + 32
        co2 = CCS811_SENSOR.eco2
        tvoc = CCS811_SENSOR.tvoc

        #Manage switches
        #0 - Light | 1 - Fan | 2 - Humidifier

        #Light
        if isTimeBetween(time(16,00), time(4,00)):
                manager.outlets[0].turn_on()
                light = 1
        else:
                manager.outlets[0].turn_off()
                light = 0

        #Fan
        if humidity > 88 or tempF > 80:
                manager.outlets[1].turn_on()
                fan = 1
        else:
                manager.outlets[1].turn_off()
                fan = 0

        #Humidifier
        if humidity < 82:
                manager.outlets[2].turn_on()
                humidifier = 1
        else:
                manager.outlets[2].turn_off()
                humidifier = 0

        #Build database object
        json = [{
            "measurement": "environment",
            "tags": {
                "environment": "env1"
            },
            "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "fields": {
                "tempF": tempF,
                "tempC": tempC,
                "humidity": humidity,
                "co2": co2,
                "tvoc": tvoc,
                "light": light,
                "fan": fan,
                "humidifier": humidifier
            }
        }]

        #Write to database
        client.write_points(json)

        sleep(10);

    except:
        print("Error")
        manager.outlets[0].turn_off()
        manager.outlets[1].turn_off()
        manager.outlets[2].turn_off()

        time.sleep(1);
