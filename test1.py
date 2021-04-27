import serial

ser = serial.Serial('/dev/ttyACM0', 9600)


def ser_read():
    if ser.readable():
        line = ser.readline()
        code = str(line.decode())
        print(code)
        return code[0]

while(1):
    code = ser_read()
    if code=='q':
        break
    else:
        code = code.encode('utf-8')
        ser.write(code)