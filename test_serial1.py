import serial

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout = 1)
while True:
    print("insert op :", end=' ')
    op = list(map(int, input().split()))
    ser.write(op)
    print("write 성공")
    data = ser.readline()
    print("R: ", int.from_bytes(data, byteorder = 'little'))
     
    if op is 'q':
        ser.close()