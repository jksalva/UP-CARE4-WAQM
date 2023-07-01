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

pm = SPS30(I2C)
#mics = MICS4514(I2C)
ze = ZE25O3(I2C)
bme680 = Adafruit_BME680_I2C(I2C,debug = False)



###############################################################################################

#pm.start_measurement()
#pm.start_fan_cleaning()

###############################################################################################

#mics.wakeup_mode()
#mics.warm_up_time(3)               #if from power off
#mics.warm_up_time(0.05)             #if on for more than 3 mins

###############################################################################################

#ze.set_active_mode()


###############################################################################################



while True:

    if sensor_setup == False:          #setup of sensors
        Xiao_1.BTConnect(sensor_setup) #execute without returning any command
        pm.start_measurement()
        pm.start_fan_cleaning()
        #Xiao_1.sendMsg("SPS30 Sensor Fan Cleaning")
        print("SPS30 Sensor Fan Cleaning")

        #mics.wakeup_mode()
        #Xiao_1.sendMsg("Calibrating MICS Sensor")
        #mics.warm_up_time(3)


        ze.set_active_mode()


        sensor_setup = True
        print(sensor_setup)
        #Xiao_1.sendMsg("Device ready for measurement")
        print("Device ready for measurement")
    #command = Xiao_1.BTConnect(sensor_setup)    #sensor data measurement
    command = 'data'    #bypass manual button from app








#PM2.5 Sensor Reading
###############################################################################################
    #serial_num = pm.read_device_serial()
    #print(serial_num)
    #print(pm.read_data_ready_flag())
    #pm.reset()         #run command to reset module if it no work
    #pm.stop_measurement()


    pm.read_measured_values()
    #pm.print_values()

###############################################################################################


    #print()


#CO and NO2 Sensor Reading
###############################################################################################

    #mics.get_gas_ppm()
    #mics.read_measured_values()
    #print("Reading gas")


###############################################################################################


    #print()

#O3 Sensor Reading
###############################################################################################



    ze.get_ozone_data()
    #ze.read_measured_values()



###############################################################################################



    #print()

#Temp Humidity Sensor Reading
###############################################################################################


    #bme680.print_values()



###############################################################################################
    #print()
    #print()



    temp = int(float("%0.2f" % bme680.temperature)*100)  #Temp: deg C


    humidity = int(float("%0.1f" %  bme680.humidity)*100)  #Humidity: %

    VOC = float("%d" % bme680.gas)  #VOC: ohm


    PM25 = int(float("%0.2f" % pm.dict_values['pm2p5'])*100) #PM2.5: ug/m3

    #CO = float("%0.2f" % mics.CO_ppm)  #CO: ppm


    #NO2 = float("%0.2f" % (mics.NO2_ppb))  #NO2: ppb

    O3 = float("%0.2f" % ze.O3_ppb)        #O3: ppb

    #datastr = str(data)[1:-1]

    data = "w".join([str(temp),str(humidity),str(PM25)])
    #data = " ".join([str(float(temp/100)),str(float(humidity/100)),str(float(PM25/100)),str(O3)])
    #data = "w".join([str(int(temp*100)),str(int(humidity*100)),str(int(PM25*100)),str(int(CO*100))])           #use this for app config
    #data="1.00,2.00,3.00,4.00,5.00,6.00,7.00"
    #data = "bwcwdwewf"
    #data = str(int(temp*100))+str(int(humidity*100))+str(int(PM25*100))+str(int(CO*100))

    print(data)


    Xiao_1.sendData(command,data)





    #time.sleep(3)


    #print(data);






