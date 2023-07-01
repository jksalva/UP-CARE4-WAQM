import board
import busio
import binascii
import time

class ZE25O3:

    def __init__(self,wire):

        self.ZE_ADDR = 0x73

        self.MEASURE_MODE_AUTOMATIC     = 0x00
        self.AUTO_DATA_REG              = 0x09
        self.AUTO_READ_DATA             = 0x00
        self.MODE_REG                   = 0x03
        self.MODE_FLG                     = 0      #mode flag is 0 for automatic


        self.DATA_REG                   = 0x04

        self.COUNT                      = 0      #number of measurements made, max is 20 for moving average
        self.COLL_NUM                   = 20    #measurements buffer 100 items

        self.ozone_data                 =[0]*self.COLL_NUM
        self.i2c = wire

        self.O3_ppb                         = 0.0

    def set_active_mode(self):

        while not self.i2c.try_lock():          #lock connection
            pass

        buf = self.MEASURE_MODE_AUTOMATIC
        reg = []
        reg.append(self.MODE_REG)
        reg.append(buf)
        self.i2c.writeto(self.ZE_ADDR,bytes(reg))

        print("Active mode set")
        self.i2c.unlock()                         #unlock connection


    def get_ozone_data(self):

        while not self.i2c.try_lock():          #lock connection
            pass



        if self.COLL_NUM > 0:
            for num in range(self.COLL_NUM ,1 ,-1):
                self.ozone_data[num-1] = self.ozone_data[num-2]

        if self.MODE_FLG == 0:                    #automatic
            buf = self.AUTO_READ_DATA

            reg = []
            reg.append(self.DATA_REG)
            reg.append(buf)


            self.i2c.writeto(self.ZE_ADDR,bytes(reg))


            self.ozone_data[0] = self.get_ozone()
            #print(self.ozone_data)
        if self.COUNT < self.COLL_NUM:
            self.COUNT += 1

        #print(self.COUNT)

        self.i2c.unlock()                         #unlock connection

        val = self.get_average(self.ozone_data ,self.COUNT)
        #print(val)
        self.O3_ppb = val
        return self.O3_ppb

        #elif (collectnum > 100) or (collectnum <= 0):
            #return -1





    def get_ozone(self):

        #while not self.i2c.try_lock():          #lock connection
            #pass


        rslt = bytearray(2)
        self.i2c.writeto_then_readfrom(self.ZE_ADDR,bytes([self.AUTO_DATA_REG]),rslt)

        #print(rslt)
        #print((rslt[0] << 8) + rslt[1])

        #print(self.ozone_data)
        #self.i2c.unlock()                         #unlock connection

        return ((rslt[0] << 8) + rslt[1])           #instantaneous O3 reading

    def get_average(self ,barry ,len):
        sum = 0
        for i in range (0 ,len):
            sum += barry[i]
        return (sum / len)

    def read_measured_values(self):
        print("O3 : " + str(self.get_ozone_data()) + " ppb")
