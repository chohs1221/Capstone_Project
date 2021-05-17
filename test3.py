
import serial

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout = 1)
while True:
    print("insert op :", end=' ')
    op = input()
    op = int(op.split(""))
    op = bytearray(op)
    ser.write(op)
    print("write 성공")
    data = ser.readline()
    print("R: ", data.decode('utf-8'))
    
    if op is 'q':
        ser.close()