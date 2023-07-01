from max30102 import MAX30102
import board
import busio

i2c = board.I2C()
#i2c = board.STEMMA_I2C

while not i2c.try_lock():
    pass



sensor = MAX30102(i2c=i2c)

sensor.setup_sensor()

while (True):
    # The check() method has to be continuously polled, to check if
    # there are new readings into the sensor's FIFO queue. When new
    # readings are available, this function will put them into the storage.
    sensor.check()

    # Check if the storage contains available samples
    if (sensor.available()):
        # Access the storage FIFO and gather the readings (integers)
        red_sample = sensor.pop_red_from_storage()
        ir_sample = sensor.pop_ir_from_storage()

        # Print the acquired data (can be plot with Arduino Serial Plotter)
        print(red_sample, ",", ir_sample)


'''
import time
from max30102 import MAX30102
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import board

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

i2c = board.I2C()
#i2c = board.STEMMA_I2C

while not i2c.try_lock():
    pass

counter= 0
try:
    while True:
        print(
            "I2C found:",
            [hex(device_address) for device_address in i2c.scan()],
        )
        time.sleep(2)

finally:
    i2c.unlock()




#    ble.start_advertising(advertisement)  # Advertise when not connected.
#    while not ble.connected:
#        counter += 1
#        print("Not connected: " +str(counter) + " sec")
#        sleep(1)
#        pass
#    print("Connected")
#    counter = 0
#    while ble.connected:  # Connected

#        while uart_server.in_waiting:  # Check BLE commands
#            packet = uart_server.read()

 #           #print(str(packet)[2:6])
 #           if str(packet)[2:6] == "data":

  #              try:
   #                 uart_server.write("Insert sensor data here\n")  # Transmit data
    #                uart_server.write("Insert sensor data here\n")  # Transmit data
     #           except OSError:
      #              pass

    sleep(.2)

'''




