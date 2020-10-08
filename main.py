import time
import board
import busio
import adafruit_ccs811
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
i2c = busio.I2C(board.SCL, board.SDA)
ccs811 = adafruit_ccs811.CCS811(i2c)

# Wait for the co2 sensor to be ready
while not ccs811.data_ready:
    pass

while True:
    try:
        humidity, tempC = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        tempF = (tempC * (9/5)) + 32
        co2 = ccs811.eco2
        tvoc = ccs811.tvoc

        print("TEMP: {0:0.1f} F / {1:0.1f} C, HUMIDITY: {2:0.1f} %, CO2: {3} PPM, TVOC: {4} PPB".format(tempF, tempC, humidity, co2, tvoc))

        time.sleep(1);

    except:
        print("Error")
        time.sleep(1);