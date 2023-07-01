#####################################


#SPS30 		= 0x69
#MiCS4514 	= 0x75
#ZE25O3 	= 0x73
from SPS30_i2c import SPS30
import time

pm = SPS30()

#pm.reset()

pm.start_measurement()
#pm.start_fan_cleaning()
#time.sleep(3)
while True:





#PM2.5 Sensor Reading
##########################################################
    #serial_num = pm.read_device_serial()
    #print(serial_num)
    #print(pm.read_data_ready_flag())
    #pm.start_measurement()
    pm.read_measured_values()
    #pm.print_values()
    #pm.reset()         #run command to reset module if it no work


    #pm.stop_measurement()
###########################################################

    #data = 'pm2p5: ' + str(pm.dict_values['pm2p5'])+ " ug/m3" + '\n'
    #print(data)
    #pm.print_values()


    print(pm.dict_values['pm2p5'])

    time.sleep(1)



