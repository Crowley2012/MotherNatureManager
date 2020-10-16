from datetime import datetime
from influxdb import InfluxDBClient

import time
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

# Wait for the co2 sensor to be ready
while not CCS811_SENSOR.data_ready:
    pass

while True:
    try:
        humidity, tempC = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        tempF = (tempC * (9/5)) + 32
        co2 = CCS811_SENSOR.eco2
        tvoc = CCS811_SENSOR.tvoc

        #print("TEMP: {0:0.1f} F / {1:0.1f} C, HUMIDITY: {2:0.1f} %, CO2: {3} PPM, TVOC: {4} PPB".format(tempF, tempC, humidity, co2, tvoc))

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
                "tvoc": tvoc
            }
        }]

        client.write_points(json)

        time.sleep(1);

    except:
        print("Error")
        time.sleep(1);
