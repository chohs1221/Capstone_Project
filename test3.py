import serial 
import time

arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)


while True:
    try:
        print(1)
        data = arduino.readline()
        print(2)
        if data:
            print(data)
            print('Hi Arduino')
    except:
        arduino.close() 