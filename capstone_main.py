import sys
import time
import threading

from opencv_header import *
import resource_rc

from collections import deque
import serial
import cv2
from playsound import playsound
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtGui import *


def audio():
    global status
    global switch
    while True:
        if status:
            switch = status.popleft()
            if switch == 1:
                print(1)
                #playsound("cartin.wav")
            elif switch == 2:
                print(2)
                # playsound("cartout.wav")
            elif switch == 3:
                print(3)
                # playsound("q.wav")
            elif switch == 4:
                print(4)
                # playsound("q.wav")
            elif switch == 5:
                print(5)
                # playsound("q.wav")

def angle2string(angle):
    if angle >= 0:
        return '++' + str("%05.2f" % (angle))
    elif angle < 0:
        return '--' + str("%05.2f" % (-angle))

def serial_run():
    global connection
    # read
    global status
    # write
    global angle
    global cart_size
    global mode
    global pump
    global stop_flag
    
    while True:
        if connection:
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
                status.append(int(data))

            except ValueError:
                print("valueError")
            except serial.SerialException:
                print("disconnect")
                connection=False
            except UnicodeDecodeError:
                print("UnicodeDecodeError")

            # write
            try:
                slope = angle2string(angle)
                # 7 + 1 + 1 + 1 + 1= 10
                data_w = slope + str(cart_size) + str(mode) + str(pump) + str(stop_flag)
                ser.write(('qq' + data_w + 'qq').encode('utf-8'))
                print(data_w)
            except:
                print("ser.write() error!!")
                continue
                
        else:
            while True:
                try:
                    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)

                except serial.SerialException:
                    continue
                else:
                    print("connect")
                    connection=True
                    break

def onChange(pos):
    pass

def opencv4():
    global angle, cart_size
    capture = cv2.VideoCapture(-1)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    cv2.namedWindow("img_contourBox")

    cv2.createTrackbar("h_min", "img_contourBox", 0, 179, onChange)
    cv2.createTrackbar("h_max", "img_contourBox", 0, 179, onChange)
    cv2.createTrackbar("s_min", "img_contourBox", 0, 255, onChange)
    cv2.createTrackbar("s_max", "img_contourBox", 0, 255, onChange)
    cv2.createTrackbar("v_min", "img_contourBox", 0, 255, onChange)
    cv2.createTrackbar("v_max", "img_contourBox", 0, 255, onChange)
    cv2.createTrackbar("blur", "img_contourBox", 5, 15, onChange)
    cv2.createTrackbar("g_scale", "img_contourBox", 0, 255, onChange)

    cv2.setTrackbarPos("h_min", "img_contourBox", 7)
    cv2.setTrackbarPos("h_max", "img_contourBox", 30)
    cv2.setTrackbarPos("s_min", "img_contourBox", 20)
    cv2.setTrackbarPos("s_max", "img_contourBox", 140)
    cv2.setTrackbarPos("v_min", "img_contourBox", 190)
    cv2.setTrackbarPos("v_max", "img_contourBox", 250)
    cv2.setTrackbarPos("blur", "img_contourBox", 9)
    cv2.setTrackbarPos("g_scale", "img_contourBox", 100)

    while cv2.waitKey(33) != ord('q'):
        ret, frame = capture.read()
        cv2.imshow("VideoFrame", frame)
        height, width, channel = frame.shape

        low = [7, 20, 190]
        high = [30, 140, 250]
        low[0] = cv2.getTrackbarPos("h_min", "img_contourBox")
        high[0] = cv2.getTrackbarPos("h_max", "img_contourBox")
        low[1] = cv2.getTrackbarPos("s_min", "img_contourBox")
        high[1] = cv2.getTrackbarPos("s_max", "img_contourBox")
        low[2] = cv2.getTrackbarPos("v_min", "img_contourBox")
        high[2] = cv2.getTrackbarPos("v_max", "img_contourBox")
        blur = cv2.getTrackbarPos("blur", "img_contourBox")
        g_scale = cv2.getTrackbarPos("g_scale", "img_contourBox")

        img_masked = mask(frame, low, high)
        cv2.imshow("img_masked", img_masked)

        img_blur = Blurring(img_masked, blur)
        cv2.imshow('img_blur', img_blur)

        img_binary = Grayscale(img_blur, g_scale)
        cv2.imshow('img_binary', img_binary)

        contours, img_contour = draw_Contours(img_binary, height, width, channel)
        cv2.imshow('contours', img_contour)

        img_contourBox, angle, cart_size = draw_ContourBox(contours, 300, 3, frame)
        cv2.imshow('img_contourBox', img_contourBox)

        if cv2.waitKey(33) == ord('r'):
            cv2.setTrackbarPos("h_min", "img_contourBox", 7)
            cv2.setTrackbarPos("h_max", "img_contourBox", 30)
            cv2.setTrackbarPos("s_min", "img_contourBox", 20)
            cv2.setTrackbarPos("s_max", "img_contourBox", 140)
            cv2.setTrackbarPos("v_min", "img_contourBox", 190)
            cv2.setTrackbarPos("v_max", "img_contourBox", 250)
            cv2.setTrackbarPos("blur", "img_contourBox", 9)
            cv2.setTrackbarPos("g_scale", "img_contourBox", 100)

    capture.release()
    cv2.destroyAllWindows()

def pyqt5():
    ui_home = uic.loadUiType("./ui_workspace/home.ui")[0]
    ui_start = uic.loadUiType("./ui_workspace/start.ui")[0]
    ui_manager = uic.loadUiType("./ui_workspace/manager.ui")[0]
    ui_status = uic.loadUiType("./ui_workspace/status.ui")[0]
    ui_stop = uic.loadUiType("./ui_workspace/stop.ui")[0]

    global level
    global accumulate
    
    class Window_Home(QMainWindow, ui_home) :
        def __init__(self) :
            super().__init__()
            self.setupUi(self)
            self.setWindowTitle('Home')

            # 창 위치
            # qr = self.frameGeometry()
            # cp = QDesktopWidget().availableGeometry().center()
            # qr.moveCenter(cp)
            # self.move(qr.topLeft())
            self.showFullScreen()
            
            # 버튼 이벤트 설정
            self.q_btn_start.clicked.connect(self.f_btn_start)
            self.q_btn_manager.clicked.connect(self.f_btn_manager)
            self.q_btn_status.clicked.connect(self.f_btn_status)
            self.q_btn_stop.clicked.connect(self.f_btn_stop)
        
        
        def f_btn_start(self) :
            global stop_flag
            stop_flag = 1
            print("Start Mode ")
            self.close()
            win_start.show()
            win_start.showFullScreen()

        def f_btn_manager(self) :
            print("Manager Mode ")
            self.close()
            win_manager.show()
            win_manager.showFullScreen()

        def f_btn_status(self) :
            print("Status Mode ")
            self.close()
            win_status.show()
            win_status.showFullScreen()
        
        def f_btn_stop(self) :
            global stop_flag
            stop_flag = 1
            print("Stop Mode ")
            self.close()
            win_stop.show()
            win_stop.showFullScreen()

    class Window_Start(QMainWindow, ui_start) :
        def __init__(self) :
            super().__init__()
            self.setupUi(self)
            self.setWindowTitle('Start')

            # 창 위치
            # qr = self.frameGeometry()
            # cp = QDesktopWidget().availableGeometry().center()
            # qr.moveCenter(cp)
            # self.move(qr.topLeft())
            
            # 타이머
            self.timer = QTimer(self)
            self.timer.start(1000)
            self.timer.timeout.connect(self.f_timeout)

            # 버튼 이벤트 설정
            self.q_btn_home.clicked.connect(self.f_btn_home)
        
        def f_btn_home(self) :
            print("home")
            self.close()
            win_home.show()

        def f_timeout(self):
            global switch
            if switch == 1:
                img = QPixmap("1.jpg")
                img = img.scaled(1020,550)
                self.q_lb_img.setPixmap(QPixmap(img))
                switch += 1
            elif switch == 2:
                img = QPixmap("2.jpg")
                img = img.scaled(1020,550)
                self.q_lb_img.setPixmap(QPixmap(img))
                switch += 1
            elif switch == 3:
                img = QPixmap("3.jpg")
                img = img.scaled(1020,550)
                self.q_lb_img.setPixmap(QPixmap(img))
                switch += 1
            elif switch == 4:
                img = QPixmap("1.jpg")
                img = img.scaled(1020,550)
                self.q_lb_img.setPixmap(QPixmap(img))
                switch += 1
            elif switch == 5:
                img = QPixmap("2.jpg")
                img = img.scaled(1020,550)
                self.q_lb_img.setPixmap(QPixmap(img))
                switch -= 4


    class Window_Manager(QMainWindow, ui_manager) :
        def __init__(self) :
            super().__init__()
            self.setupUi(self)
            self.setWindowTitle('Manager')

            # 창 위치
            # qr = self.frameGeometry()
            # cp = QDesktopWidget().availableGeometry().center()
            # qr.moveCenter(cp)
            # self.move(qr.topLeft())
            #self.showFullScreen()

            # 버튼 이벤트 설정
            self.q_btn_home.clicked.connect(self.f_btn_home)
            self.q_btn_stop.clicked.connect(self.f_btn_stop)

            self.q_chkb_washonly.stateChanged.connect(self.f_chkb_washonly)
            self.q_rad_Level1.clicked.connect(self.f_gBox_pressure)
            self.q_rad_Level2.clicked.connect(self.f_gBox_pressure)
            self.q_rad_Level3.clicked.connect(self.f_gBox_pressure)
        
        def f_btn_home(self) :
            print("home")
            self.close()
            win_home.show()
            win_home.showFullScreen()
        
        def f_chkb_washonly(self) :
            global mode
            if self.q_chkb_washonly.isChecked() :
                mode = 1
                print("Wash Only")
            else :
                mode = 0
                print("Wash and Clean")
        
        def f_gBox_pressure(self) :
            global pump
            if self.q_rad_Level1.isChecked():
                pump = 0
                print("level 1")
            elif self.q_rad_Level2.isChecked():
                pump = 1
                print("level 2")
            elif self.q_rad_Level3.isChecked():
                pump = 2
                print("level 3")
        
        def f_btn_stop(self) :
            global stop_flag
            stop_flag = 1
            print("Stop Mode ")
            self.close()
            win_stop.show()
            win_stop.showFullScreen()

    class Window_Status(QMainWindow, ui_status) :
        def __init__(self) :
            super().__init__()
            self.setupUi(self)
            self.setWindowTitle('Status')

            # 창 위치
            # qr = self.frameGeometry()
            # cp = QDesktopWidget().availableGeometry().center()
            # qr.moveCenter(cp)
            # self.move(qr.topLeft())
            #self.showFullScreen()

            # 텍스트 출력
            self.q_lb_daily.setText("{}".format(daily))
            self.q_lb_accumulate.setText("{}".format(accumulate))

            # 버튼 이벤트 설정
            self.q_btn_home.clicked.connect(self.f_btn_home)
            self.q_btn_stop.clicked.connect(self.f_btn_stop)
            self.q_btn_resetD.clicked.connect(self.f_btn_resetD)
            self.q_btn_resetA.clicked.connect(self.f_btn_resetA)

            # 타이머
            self.timer = QTimer(self)
            self.timer.start(1000)
            self.timer.timeout.connect(self.f_timeout)
        
        def f_btn_home(self) :
            print("home")
            self.close()
            win_home.show()
        
        def f_btn_stop(self) :
            global stop_flag
            stop_flag = 1
            print("Stop Mode ")
            self.close()
            win_stop.show()
            win_stop.showFullScreen()
        
        def f_btn_resetD(self) :
            global daily
            daily = 0
            self.q_lb_daily.setText("{}".format(daily))
            
        def f_btn_resetA(self) :
            global accumulate
            accumulate = 0
            self.q_lb_accumulate.setText("{}".format(accumulate))

        def f_timeout(self):
            global level
            if level == 0:
                img = QPixmap("1111.png")
                img = img.scaled(330,200)
                self.q_lb_level.setPixmap(QPixmap(img))
                level += 1
            elif level == 1:
                img = QPixmap("2222.png")
                img = img.scaled(330,200)
                self.q_lb_level.setPixmap(QPixmap(img))
                level -= 1

    class Window_Stop(QMainWindow, ui_stop) :
        def __init__(self) :
            super().__init__()
            self.setupUi(self)
            self.setWindowTitle('Stop')

            # 창 위치
            # qr = self.frameGeometry()
            # cp = QDesktopWidget().availableGeometry().center()
            # qr.moveCenter(cp)
            # self.move(qr.topLeft())
            #self.showFullScreen()

            # 버튼 이벤트 설정
            self.q_btn_home.clicked.connect(self.f_btn_home)
        
        def f_btn_home(self) :
            print("home")
            self.close()
            win_home.show()
            win_home.showFullScreen()

    app = QApplication(sys.argv)
    win_home = Window_Home()
    win_start = Window_Start()
    win_manager = Window_Manager()
    win_status = Window_Status()
    win_stop = Window_Stop()
    win_home.show()
    app.exec_()

if __name__ == "__main__" :
    # write
    angle = 0.0
    cart_size = 0
    mode = 0
    pump = 0
    stop_flag = 1

    # read
    level = 0
    daily = 10
    switch = 1
    
    accumulate = 20
    status = deque()
    connection = False
    # app = QApplication(sys.argv)
    # win_home = Window_Home()
    # win_start = Window_Start()
    # win_master = Window_Master()
    # win_status = Window_Status()
    # win_stop = Window_Stop()
    # win_home.show()
    # p1 = threading.Thread(target=opencv4)
    # p1.start()
    # p1.join()
    p2 = threading.Thread(target=pyqt5)
    p2.start()
    # p2.join()
    p3 = threading.Thread(target=serial_run)
    p3.start()
    # p4 = threading.Thread(target=audio)
    # p4.start()
    # while True:
    #     print(angle, cart_size, mode, pump, stop_flag)