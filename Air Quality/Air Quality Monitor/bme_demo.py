from BME680_i2c import Adafruit_BME680_I2C
import board
import busio
import time

i2c = busio.I2C(board.SCL,board.SDA)


bme680 = Adafruit_BME680_I2C(i2c,debug = False)




while True:
    bme680.print_values()

    time.sleep(1)
