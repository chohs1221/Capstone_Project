import serial
while True:
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)

    except serial.SerialException:
        continue
    print("connect")
    connection=True
    break