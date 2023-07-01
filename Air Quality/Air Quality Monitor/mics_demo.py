# Write your code here :-)
from MICS4514_i2c import MICS4514
import time
import board
import busio

I2C = busio.I2C(board.SCL, board.SDA)

mics = MICS4514(I2C)
mics.wakeup_mode()
mics.wakeup_mode()
mics.get_power_mode()
#mics.warm_up_time(3)
mics.wakeup_mode()
mics.warm_up_time(0.05)
#mics.warm_up_time(3)

#print(mics.r0_ox)
#print(mics.r0_red)

while True:


    mics.get_gas_ppm()
    print("C0: " + str(mics.CO_ppm) + " ppm")
    print("NO2: " + str(mics.NO2_ppb) + " ppb")

    #mics.get_power_mode()
    #time.sleep(2)
    #mics.sleep_mode()
    #mics.get_power_mode()

    #mics.get_mics_data()



    time.sleep(2)

