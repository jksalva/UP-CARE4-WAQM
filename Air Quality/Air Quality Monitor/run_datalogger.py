#####################################


#SPS30 		= 0x69
#MiCS4514 	= 0x75
#ZE25O3 	= 0x73




from ble_connect import XiaoBLE
from SPS30_i2c import SPS30
import time

Xiao_1 = XiaoBLE()
pm = SPS30()

pm.start_measurement()
#pm.start_fan_cleaning()
#time.sleep(10)

command = "data"
while True:
    #command = Xiao_1.BTConnect()
    Xiao_1.BTConnect()



#PM2.5 Sensor Reading
##########################################################
    #serial_num = pm.read_device_serial()
    #print(serial_num)
    #print(pm.read_data_ready_flag())
    #pm.start_measurement()
    pm.read_measured_values()
    #pm.print_values()
    #pm.reset()         #run command to reset module if it no work

    #print('pm2p5: ' + str(pm.dict_values['pm2p5'])+ " ug/m3")


    #pm.stop_measurement()
###########################################################

    #data = 'pm2p5: ' + str(pm.dict_values['pm2p5'])+ " ug/m3" + '\n'
    data = str(pm.dict_values['pm2p5'])

    print(data)

    Xiao_1.sendData(command,data)




    time.sleep(5)



