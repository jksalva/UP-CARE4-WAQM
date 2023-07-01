import board
import busio
import binascii


def calculateCRC(input):
    crc = 0xFF
    for i in range (0, 2):
        crc = crc ^ input[i]
        for j in range(8, 0, -1):
            if crc & 0x80:
                crc = (crc << 1) ^ 0x31
            else:
                crc = crc << 1
    crc = crc & 0x0000FF
    return crc

def checkCRC(result):
    for i in range(2, len(result), 3):
        data = []
        data.append(result[i-2])
        data.append(result[i-1])

        crc = result[i]

        if crc == calculateCRC(data):
            crc_result = True
        else:
            crc_result = False
    return crc_result


def bin2dec(bindata):
    result = 0
    size = len(bindata)
    for i in range(size):

        exp = (size-1) - i
        result += int(bindata[i]) * (2 ** exp)

    return result

def bin2frac(bindata):
    result = 0
    size = len(bindata)
    for i in range(size):
        exp = -(i+1)
        result += int(bindata[i]) * (2 ** exp)

    return result

def IEEE754(data32):

    sign = int(data32[0])
    E = bin2dec(data32[1:9])
    frac = bin2frac(data32[9:32])

    e = E - 127

    result = ((-1) ** sign) * (1+frac) * (2 ** e)

    return result


def zeroPad(binary):
    remainder = 8-len(binary)
    result = ""
    pad = ""
    if remainder != 0:
        pad = '0'*remainder

    result = pad + binary
    #print(result)
    return result






class SPS30:

    def __init__(self,wire):



        self.SPS_ADDR = 0x69

        self.START_MEAS   = [0x00, 0x10]
        self.STOP_MEAS    = [0x01, 0x04]
        self.R_DATA_RDY   = [0x02, 0x02]
        self.R_VALUES     = [0x03, 0x00]
        self.RW_AUTO_CLN  = [0x80, 0x04]
        self.START_CLN    = [0x56, 0x07]
        self.R_ARTICLE_CD = [0xD0, 0x25]
        self.R_SERIAL_NUM = [0xD0, 0x33]
        self.START_CLN    = [0x56, 0x07]
        self.RESET        = [0xD3, 0x04]


        #self.i2c = busio.I2C(board.SCL,board.SDA)
        self.i2c = wire

        self.SERIAL_NUMBER_ERROR = -2

        self.dict_values = { "pm1p0"  : None,
                            "pm2p5"  : None,
                            "pm4p0"  : None,
                            "pm10p0" : None,
                            "nc0p5"  : None,
                            "nc1p0"  : None,
                            "nc2p5"  : None,
                            "nc4p0"  : None,
                            "nc10p0" : None,
                            "typical": None}


    def read_device_serial(self):

        while not self.i2c.try_lock():
            pass

        self.i2c.writeto(self.SPS_ADDR, bytes(self.R_SERIAL_NUM))
        result = bytearray(48)
        self.i2c.readfrom_into(self.SPS_ADDR, result)

        result_str = ""
        for i in range(len(result)):

            if (i+1)%3 != 0:
                result_str += chr(int(result[i]))


        self.i2c.unlock()

        return result_str


    def start_measurement(self):

        self.START_MEAS   = [0x00, 0x10]
        while not self.i2c.try_lock():
            pass


        self.START_MEAS.append(0x03)
        self.START_MEAS.append(0x00)

        crc = calculateCRC(self.START_MEAS[2:4])
        self.START_MEAS.append(crc)

        #print(self.START_MEAS)

        #add_res = [hex(x) for x in self.i2c.scan()]
        #print(add_res)
        self.i2c.writeto(self.SPS_ADDR,bytes(self.START_MEAS))
        #print("Start Measurement")

        self.i2c.unlock()

    def stop_measurement(self):

        while not self.i2c.try_lock():
            pass



        self.i2c.writeto(self.SPS_ADDR,bytes(self.STOP_MEAS))

        print("Measurement Stopped")
        self.i2c.unlock()

    def read_data_ready_flag(self):
        result = []
        while not self.i2c.try_lock():
            pass

        add_res = [hex(x) for x in self.i2c.scan()]
        #print(add_res)

        self.i2c.writeto(self.SPS_ADDR,bytes(self.R_DATA_RDY))

        read = bytearray(3)

        #print(read)
        #self.i2c.writeto_then_readfrom(self.SPS_ADDR,bytes(self.R_DATA_RDY),read)


        self.i2c.readfrom_into(self.SPS_ADDR, read)

        #print(read)

        if read[1] == 1:
            print("Sensor Ready to Read")

        self.i2c.unlock()
        return read[1]


    def read_measured_values(self):

        while not self.i2c.try_lock():
            pass

        #print("Reading Values")

        result = []
        bytesdata = []
        data32 = []

        add_res = [hex(x) for x in self.i2c.scan()]

        self.i2c.writeto(self.SPS_ADDR, bytes(self.R_VALUES))

        read = bytearray(60)
        self.i2c.readfrom_into(self.SPS_ADDR, read)

        #print()
        #print(read)
        #print()

        for i in range(len(read)):
            if (i+1)%3 != 0:            #remove checksum
                bytesdata.append(zeroPad(bin(read[i])[2:]))

        #print(bytesdata)

        #print()
        for i in range(0,len(bytesdata),4):

            data32.append(bytesdata[i]+bytesdata[i+1]+bytesdata[i+2]+bytesdata[i+3])
            #print(i)


        #print(data32)

        for i in range(len(data32)):
            result.append(IEEE754(data32[i]))

        #print()

        #print(result)

        index = 0

        #print()

        self.dict_values['pm1p0'] = result[0]
        self.dict_values['pm2p5'] = result[1]
        self.dict_values['pm4p0'] = result[2]
        self.dict_values['pm10p0'] = result[3]
        self.dict_values['nc0p5'] = result[4]
        self.dict_values['nc1p0'] = result[5]
        self.dict_values['nc2p5'] = result[6]
        self.dict_values['nc4p0'] = result[7]
        self.dict_values['nc10p0'] = result[8]
        self.dict_values['typical'] = result[9]





        self.i2c.unlock()

    def print_values(self):
        print('PM1.0: ' + str(self.dict_values['pm1p0']) + " ug/m3")
        print('PM2.5: ' + str(self.dict_values['pm2p5'])+ " ug/m3")
        print('PM4.0: ' + str(self.dict_values['pm4p0'])+ " ug/m3")
        print('PM10.0: ' + str(self.dict_values['pm10p0'])+ " ug/m3")
        print('NC0.5: ' + str(self.dict_values['nc0p5'])+ " #/cm3")
        print('NC1.0: ' + str(self.dict_values['nc1p0'])+ " #/cm3")
        print('NC2.5: ' + str(self.dict_values['nc2p5'])+ " #/cm3")
        print('NC4.0: ' + str(self.dict_values['nc4p0'])+ " #/cm3")
        print('NC10.0: ' + str(self.dict_values['nc10p0'])+ " #/cm3")
        print('Size: ' + str(self.dict_values['typical'])+ " um")



    def start_fan_cleaning(self):
        while self.i2c.try_lock():
            pass


        self.i2c.writeto(self.SPS_ADDR, bytes(self.START_CLN))

        print("Fan Cleaning")
        self.i2c.unlock()


    def reset(self):

        while self.i2c.try_lock():
            pass


        self.i2c.writeto(self.SPS_ADDR, bytes(self.RESET))

        print("Reseting Device")
        self.i2c.unlock()

