import board
import busio

R_SERIAL_NUM = [0xD0, 0x33]


i2c = busio.I2C(board.SCL,board.SDA)

while not i2c.try_lock():
    pass


add_res = [hex(x) for x in i2c.scan()]
#print(add_res)


i2c.writeto(0x69, bytes(R_SERIAL_NUM))
result = bytearray(48)
i2c.readfrom_into(0x69, result)


res_new = result          #decimal form of ascii character
res_clean = []
for i in range(len(res_new)):

    if (i+1)%3 != 0:
        res_clean.append(int(res_new[i]))

res_str = ""
for i in res_clean:
    #print(chr(i))
    res_str += chr(i)

print(str(res_str))






