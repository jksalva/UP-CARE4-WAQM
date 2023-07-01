#####################################


#SPS30 		= 0x69
#MiCS4514 	= 0x75
#ZE25O3 	= 0x73




from ble_connect import XiaoBLE

from SPS30_i2c import SPS30
from MICS4514_i2c import MICS4514
from ZE25O3_i2c import ZE25O3
from BME680_i2c import Adafruit_BME680_I2C

from I2C import I2C
import board
import busio
import time




sensor_setup = False



I2C = busio.I2C(board.SCL, board.SDA)
Xiao_1 = XiaoBLE()

while not I2C.try_lock():
    pass

I2C.scan()

I2C.unlock()

#Xiao_1.BTConnect()
#time.sleep(5)

mics = MICS4514(I2C)
pm = SPS30(I2C)
ze = ZE25O3(I2C)
bme680 = Adafruit_BME680_I2C(I2C,debug = False)



###############################################################################################

#pm.start_measurement()
#pm.start_fan_cleaning()

###############################################################################################

mics.wakeup_mode()
#mics.warm_up_time(3)               #if from power off
mics.warm_up_time(0.05)             #if on for more than 3 mins

###############################################################################################

#ze.set_active_mode()


###############################################################################################



while True:

    if sensor_setup == False:          #setup of sensors
        Xiao_1.BTConnect(sensor_setup) #execute without returning any command
        pm.start_measurement()
        pm.start_fan_cleaning()
        Xiao_1.sendMsg("SPS30 Sensor Fan Cleaning")


        #mics.wakeup_mode()
        #Xiao_1.sendMsg("Calibrating MICS Sensor")
        #mics.warm_up_time(3)


        ze.set_active_mode()


        sensor_setup = True
        print(sensor_setup)
        Xiao_1.sendMsg("Device ready for measurement")

    command = Xiao_1.BTConnect(sensor_setup)    #sensor data measurement









#PM2.5 Sensor Reading
###############################################################################################
    #serial_num = pm.read_device_serial()
    #print(serial_num)
    #print(pm.read_data_ready_flag())
    #pm.reset()         #run command to reset module if it no work
    #pm.stop_measurement()


    pm.read_measured_values()
    pm.print_values()

###############################################################################################


    print()


#CO and NO2 Sensor Reading
###############################################################################################

    mics.get_gas_ppm()
    mics.read_measured_values()
    print("Reading gas")


###############################################################################################


    print()

#O3 Sensor Reading
###############################################################################################



    ze.get_ozone_data()
    ze.read_measured_values()



###############################################################################################



    print()

#Temp Humidity Sensor Reading
###############################################################################################


    bme680.print_values()



###############################################################################################
    print()
    print()

    data = "Temp: " + str(bme680.temperature) + "deg C"
    Xiao_1.sendData(command,data)

    data = "Humidity: " + str(bme680.humidity) + "%"
    Xiao_1.sendData(command,data)

    data = "VOC: " + str(bme680.gas) + "ohm"
    Xiao_1.sendData(command,data)

    data = "PM2.5: " + str(pm.dict_values['pm2p5']) + " ug/m3"
    #data = [1,2,3]
    #print(data)
    #data = bme680.temperature
    Xiao_1.sendData(command,data)

    data = "CO: " + str(mics.CO_ppm) + " ppm"
    Xiao_1.sendData(command,data)


    data = "NO2: " + str(mics.NO2_ppb) + " ppb"
    Xiao_1.sendData(command,data)

    data = "O3: " + str(ze.O3_ppb) + " ppb"
    Xiao_1.sendData(command,data)





    time.sleep(60)







