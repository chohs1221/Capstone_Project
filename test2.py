import serial
from collections import deque

def serial_run():
    global angle
    global status
    global connection
    #ser = serial.Serial('/dev/ttyACM0', 9600)
    while True:
        if connection:
            print(1)
            # read
            try:
                res=ser.readline()
                data=res.decode('utf-8')
                print(data)

                # if data=='\r' or data=='\n':
                #     continue
                # else:
                #     datalist=data.split('\t')
                #     for val in datalist:
                #         print(float(val))
                #status.append(data)

            except ValueError:
                print("valueError")
            except serial.SerialException:
                print("disconnect")
                ser.close()
                connection=False
            except UnicodeDecodeError:
                print("UnicodeDecodeError")
                
            # write
            try:
                code = str(int(angle))
                code = code.encode('utf-8')
                ser.write(code)
                print("전송완료")
            except:
                print("ser.write() error!!")
                continue
                
        else:
            while True:
                try:
                    ser = serial.Serial('/dev/ttyUSB0', 9600)

                except serial.SerialException:
                    
                    continue
                else:
                    print("connect")
                    connection=True
                    break

angle = 100
connection = False
serial_run()