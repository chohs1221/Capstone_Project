# import serial 
# import time

# arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)


# while True:
#     try:
#         print(1)
#         data = arduino.readline()
#         print(2)
#         if data:
#             print(data)
#             print('Hi Arduino')
#     except:
#         arduino.close()

import serial

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout = 1)
while True:
    print("insert op :", end=' ')
    op = input()
    ser.write(op.encode('utf-8'))
    print("write 성공")
    data = ser.readline()
    print("R: ", data.decode('utf-8'))
    
    if op is 'q':
        ser.close()