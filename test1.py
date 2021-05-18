a = bin(0b1100)
b = bytes([254])
sign = 128
angle = -11.2
cart_size = 101
mode = 112
pump = 122
stop_flag = 130
c = bytearray([255, 255, (sign+abs(round(angle))), cart_size, mode, pump, stop_flag, 254])
print(c)
print(bin(cart_size))