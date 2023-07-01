from ZE25O3_i2c import ZE25O3
import time
import busio
import board

I2C = busio.I2C(board.SCL, board.SDA)


ze = ZE25O3(I2C)
print("Startup")
ze.set_active_mode()


while True:

    #print("ajfkla")
    print("O3 concentration: " + str(ze.get_ozone_data()) + " ppb")
    time.sleep(5)
