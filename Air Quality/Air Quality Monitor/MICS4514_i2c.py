import board
import busio
import binascii
import time


class MICS4514:
    def __init__(self,wire):

        self.MICS_ADDR = 0x75
        self.OX_REG_HIGH = 0x04
        self.RED_REG_HIGH = 0x06
        self.POWER_REG_HIGH = 0x08

        self.CO = 0x01
        self.NO2 = 0x0A

        self.POWER_REGISTER_MODE = 0x0A
        self.SLEEP_MODE = 0x00
        self.WAKEUP_MODE = 0x01

        self.r0_ox = 1.0
        self.r0_red = 1.0

        self.rs_r0_red_data = 0.0
        self.rs_r0_ox_data  = 0.0

        self.CO_ppm = 0.0
        self.NO2_ppb = 0.0

        self.i2c = wire

    def get_power_mode(self):

        while not self.i2c.try_lock():
            pass
        result = bytearray(1)
        self.i2c.writeto_then_readfrom(
            self.MICS_ADDR, bytes([self.POWER_REGISTER_MODE]), result
        )
        # reg = []
        # reg.append(self.MICS_ADDR)
        # reg.append(self.POWER_REGISTER_MODE)
        # print(type(self.MICS_ADDR))

        #print("Power mode: " + str(result)[-3:-2])
        self.i2c.unlock()

    def wakeup_mode(self):

        while not self.i2c.try_lock():
            pass


        rslt = []
        rslt.append(self.POWER_REGISTER_MODE)
        rslt.append(self.WAKEUP_MODE)
        self.i2c.writeto(self.MICS_ADDR, bytes(rslt))

        self.i2c.unlock()

    def sleep_mode(self):

        while not self.i2c.try_lock():
            pass
        rslt = []
        rslt.append(self.POWER_REGISTER_MODE)
        rslt.append(self.SLEEP_MODE)
        self.i2c.writeto(self.MICS_ADDR, bytes(rslt))

        self.i2c.unlock()

    def warm_up_time(self, minute):

        second = minute * 60
        print("Start calibration Sensor!")
        while second >= 0:


            print("Please wait calibration! Time left: " + str(second) + " seconds")
            second = second - 1
            time.sleep(1)
        for i in range(10):
            res = self.get_mics_data()
            self.r0_ox = self.r0_ox + res[0]
            self.r0_red = self.r0_red + res[1]
            time.sleep(1)
            print("Please wait calibration!")
        self.r0_ox = (int)(self.r0_ox / 10)  # average over 10 seconds
        self.r0_red = (int)(self.r0_red / 10)  # average over 10 seconds
        print("calibration success!")

        print(self.r0_ox)
        print(self.r0_red)

    def get_mics_data(self):

        bytesdata = []
        while not self.i2c.try_lock():
            pass
        read = bytearray(6)  # 6 bytes, 16 bit values paired by 2 bytes in data
        self.i2c.writeto_then_readfrom(self.MICS_ADDR, bytes([self.OX_REG_HIGH]), read)
        #print(read)
        # print(list(read))

        #for i in range(len(read)):
        #    bytesdata.append(hex(read[i])[2:])

        #print(bytesdata)

        oxdata = read[0] * 256 + read[1]  # pair 2 bytes 16 bit, oxdata
        reddata = read[2] * 256 + read[3]  # pair 2 bytes 16 bit, reddata
        powerdata = read[4] * 256 + read[5]  # pair 2 bytes 16 bit, powerdata

        #print("Ox: " + str(oxdata) + " Red: " + str(reddata) + " Power: " + str(powerdata))
        # print(powerdata)

        res = [0] * 3
        if (powerdata - oxdata) <= 0:
            res[0] = 0
        else:
            res[0] = powerdata - oxdata


        if (powerdata - reddata) < 0:
            res[1] = 0
        else:
            res[1] = powerdata - reddata


        res[2] = powerdata

        #print(res)
        self.i2c.unlock()
        #print(res)
        return res

    def get_gas_ppm(self):

        result = self.get_mics_data()

        self.rs_r0_red_data = result[1]
        self.rs_r0_red_data = float(self.rs_r0_red_data) / float(self.r0_red)


        #print("rsr0red: " + str(self.rs_r0_red_data))
        self.rs_r0_ox_data = result[0]
        self.rs_r0_ox_data = float(self.rs_r0_ox_data) / float(self.r0_ox)

        #print("rsr0: " +  str(self.rs_r0_red_data) + "  " + str(self.rs_r0_ox_data))


        #print(self.rs_r0_ox_data)
        #print(self.rs_r0_red_data)

        self.get_C0(self.rs_r0_red_data)
        self.get_NO2(self.rs_r0_ox_data)

    def get_C0(self,data):
        if data > 0.425:
            return 0.0

        co = (0.425 - data) / 0.000405
        #print("co: " + str(co))
        if co > 1000.0:
            return 1000.0
        if co < 1.0:
            return 0.0

        self.C0_ppm = co
        return co

    def get_NO2(self,data):

        if data < 1.1:
            return 0.0
        no2 = (data - 0.045) / 6.13
        if no2 > 10.0:
            return 10.0
        if no2 < 0.05:
            return 0.0
        self.NO2_ppb = no2
        return no2

    def read_measured_values(self):

        print("C0: " + str(self.CO_ppm) + " ppm")
        print("NO2: " + str(self.NO2_ppb) + " ppb")
