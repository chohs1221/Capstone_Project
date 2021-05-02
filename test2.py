import serial

def serial_run():
    global connection
    #ser = serial.Serial('/dev/ttyACM0', 9600)
    while True:
        if connection:
            try:
                res=ser.readline()
                data=res.decode('utf-8')

                if data=='\r' or data=='\n':
                    continue
                else:
                    datalist=data.split('\t')
                    for val in datalist:
                        print(float(val))

            except ValueError:
                print("valueError")
            except serial.SerialException:
                print("disconnect")
                ser.close()
                connection=False
            except UnicodeDecodeError:
                print("UnicodeDecodeError")
            
            try:
                code = str(int(angle))
                code = code.encode('utf-8')
                ser.write(code)
            except:
                print("ser.write() error!!")
                continue
                
        else:
            while True:
                try:
                    ser = serial.Serial('/dev/ttyACM0', 9600)

                except serial.SerialException:
                    print("---")
                    continue
                else:
                    print("connect",self.ser)
                    self.connection=True
                    break

connection = False
serial_run()