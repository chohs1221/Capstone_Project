import sys
import time
import threading

import cv2
from opencv_header import *

from collections import deque
import serial

from playsound import playsound

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtGui import *
import resource_rc


def audio(num):
    try:
        if num == 0:
            print(0)
            playsound("cartin.wav")
        elif num == 1:
            print(1)
            playsound("cartout.wav")
        elif num == 2:
            print(2)
            playsound("cartin.wav")
        elif num == 3:
            print(3)
            playsound("cartout.wav")
        # elif num == 4:
        #     print(4)
        #     playsound("cartout.wav")
        elif num == 5:
            print(5)
            playsound("cartin.wav")
        elif num == 6:
            print(6)
            playsound("cartout.wav")
        elif num == 7:
            print(7)
            playsound("cartin.wav")
        elif num == 8:
            print(8)
            playsound("cartin.wav")
        else:
            pass
    except:
        pass

def angle2string(angle):
    if angle >= 0:
        return '+' + str("%05.2f" % (angle))
    elif angle < 0:
        return '-' + str("%05.2f" % (-angle))

def serial_run():
    global connection
    global daily
    global accumulate
    # write
    global angle
    global cart_size
    global mode
    global pump
    global stop_flag
    #read
    global data
    global empty
    
    data_pre = 0
    while True:
        if connection:
            # read
            try:
                res = ser.readline()
                data = int.from_bytes(res, byteorder = 'little')
                if ((data % 10) != data_pre) and (0 <= (data % 10) <= 7):
                    data_pre = (data % 10)
                    print(data_pre)
                    if data_pre == 7:
                        accumulate += 1
                        daily += 1
                    audio(num = (data % 10))
                if (data // 10) == 0:
                    empty = 0
                elif (data // 10) == 1:
                    empty = 1

            except ValueError:
                print("valueError")
            except serial.SerialException:
                print("disconnect")
                connection=False
            except UnicodeDecodeError:
                print("UnicodeDecodeError")

            # write
            try:
                # slope = angle2string(angle)
                if angle >= 0:
                    sign = 0b00000000
                else:
                    sign = 0b10000000
                # 0xff, 0xff, 부호+각도, 01?, 01?, 012?, 01?, 01234 => 8byte
                checksum = cart_size + mode + pump + stop_flag
                ser.write([255, 255, (sign+abs(round(angle))), cart_size, mode, pump, stop_flag, checksum])
                # print(bytearray([255, 255, (sign+abs(round(angle))), cart_size, mode, pump, stop_flag, checksum]))
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
            stop_flag = 0
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
            # win_home.showFullScreen()

        def f_timeout(self):
            global data
            try:
                img = QPixmap("./images/img{}.png".format(data))
                img = img.scaled(1020,550)
                self.q_lb_img.setPixmap(QPixmap(img))
            except:
                pass


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
            # win_home.showFullScreen()
        
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
            # win_home.showFullScreen()
        
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
            global empty
            global accumulate
            global daily

            if empty == 0:
                img = QPixmap("./images/empty_green.png")
                img = img.scaled(330,200)
                self.q_lb_level.setPixmap(QPixmap(img))
            elif empty == 1:
                img = QPixmap("./images/empty_red.png")
                img = img.scaled(330,200)
                self.q_lb_level.setPixmap(QPixmap(img))

            self.q_lb_daily.setText("{}".format(daily))
            self.q_lb_accumulate.setText("{}".format(accumulate))

    class Window_Stop(QMainWindow, ui_stop) :
        def __init__(self) :
            super().__init__()
            self.setupUi(self)
            img = QPixmap("./images/imgstop.png")
            img = img.scaled(1000, 460)
            self.q_lb_stop.setPixmap(QPixmap(img))
            # self.setWindowTitle('Stop')
            
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
            # win_home.showFullScreen()

    app = QApplication(sys.argv)
    win_home = Window_Home()
    win_start = Window_Start()
    win_manager = Window_Manager()
    win_status = Window_Status()
    win_stop = Window_Stop()
    win_home.show()
    # win_home.showFullScreen()
    app.exec_()

if __name__ == "__main__" :
    # write
    angle = 127.0
    cart_size = 0
    mode = 0
    pump = 0
    stop_flag = 0

    # read
    data = 0
    empty = 0

    daily = 0    
    accumulate = 0

    connection = False
    # app = QApplication(sys.argv)
    # win_home = Window_Home()
    # win_start = Window_Start()
    # win_master = Window_Master()
    # win_status = Window_Status()
    # win_stop = Window_Stop()
    # win_home.show()
    p1 = threading.Thread(target=opencv4)
    p1.start()
    p2 = threading.Thread(target=pyqt5)
    p2.start()
    p3 = threading.Thread(target=serial_run)
    p3.start()