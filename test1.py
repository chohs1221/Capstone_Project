import cv2
import time
import serial
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from multiprocessing import Process
import threading
from opencv_header import *
import resource_rc

def serial_():
    ser = serial.Serial('/dev/ttyACM0', 9600)
    while(1):
        code = 100
        if code=='q':
            break
        else:
            code = code.encode('utf-8')
            ser.write(code)

def onChange(pos):
    pass

def opencv4():
    capture = cv2.VideoCapture(1)
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

        img_contourBox = draw_ContourBox(contours, 300, 3, frame)
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

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
ui_home = uic.loadUiType("home.ui")[0]
ui_start = uic.loadUiType("start.ui")[0]
ui_master = uic.loadUiType("mastermode.ui")[0]
ui_status = uic.loadUiType("status.ui")[0]
ui_stop = uic.loadUiType("stop.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class Window_Home(QMainWindow, ui_home) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Home')

        # 창 위치
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        # 버튼 이벤트 설정
        self.q_btn_start.clicked.connect(self.f_btn_start)
        self.q_btn_mastermode.clicked.connect(self.f_btn_mastermode)
        self.q_btn_status.clicked.connect(self.f_btn_status)
        self.q_btn_stop.clicked.connect(self.f_btn_stop)
    
    
    def f_btn_start(self) :
        print("Start Mode ")
        self.close()
        win_start.show()

    def f_btn_mastermode(self) :
        print("Mater Mode ")
        self.close()
        win_master.show()

    def f_btn_status(self) :
        print("Status Mode ")
        self.close()
        win_status.show()
    
    def f_btn_stop(self) :
        print("Stop Mode ")
        self.close()
        win_stop.show()

class Window_Start(QMainWindow, ui_start) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Start')

        # 창 위치
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # 버튼 이벤트 설정
        self.q_btn_home.clicked.connect(self.f_btn_home)
        self.q_btn_stop.clicked.connect(self.f_btn_stop)
    
    def f_btn_home(self) :
        print("home")
        self.close()
        win_home.show()
    
    def f_btn_stop(self) :
        print("Stop Mode ")
        self.close()
        win_stop.show()

class Window_Master(QMainWindow, ui_master) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Master')

        # 창 위치
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # 버튼 이벤트 설정
        self.q_btn_home.clicked.connect(self.f_btn_home)
        self.q_btn_stop.clicked.connect(self.f_btn_stop)

        self.q_rad_large.clicked.connect(self.f_gBox_size)
        self.q_rad_midium.clicked.connect(self.f_gBox_size)
        self.q_rad_small.clicked.connect(self.f_gBox_size)

        self.q_chkb_washonly.stateChanged.connect(self.f_chkb_washonly)
        self.q_rad_Level1.clicked.connect(self.f_gBox_pressure)
        self.q_rad_Level2.clicked.connect(self.f_gBox_pressure)
        self.q_rad_Level3.clicked.connect(self.f_gBox_pressure)
    
    def f_btn_home(self) :
        print("home")
        self.close()
        win_home.show()

    def f_gBox_size(self) :
        if self.q_rad_large.isChecked() : print("Large Size")
        elif self.q_rad_midium.isChecked() : print("Midium Size")
        elif self.q_rad_small.isChecked() : print("Small Size")
    
    def f_chkb_washonly(self) :
        if self.q_chkb_washonly.isChecked() :
            print("Wash Only")
        else :
            print("Wash and Clean")
    
    def f_gBox_pressure(self) :
        if self.q_rad_Level1.isChecked() : print("level 1")
        elif self.q_rad_Level2.isChecked() : print("level 2")
        elif self.q_rad_Level3.isChecked() : print("level 3")
    
    def f_btn_stop(self) :
        print("Stop Mode ")
        self.close()
        win_stop.show()

class Window_Status(QMainWindow, ui_status) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Status')

        # 창 위치
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # 버튼 이벤트 설정
        self.q_btn_home.clicked.connect(self.f_btn_home)
        self.q_btn_stop.clicked.connect(self.f_btn_stop)
    
    def f_btn_home(self) :
        print("home")
        self.close()
        win_home.show()
    
    def f_btn_stop(self) :
        print("Stop Mode ")
        self.close()
        win_stop.show()

class Window_Stop(QMainWindow, ui_stop) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Stop')

        # 창 위치
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # 버튼 이벤트 설정
        self.q_btn_home.clicked.connect(self.f_btn_home)
    
    def f_btn_home(self) :
        print("home")
        self.close()
        win_home.show()
    
    def f_btn_stop(self) :
        print("Stop Mode ")
        self.close()
        win_stop.show()


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    cnt = 0
    win_home = Window_Home()
    win_start = Window_Start()
    win_master = Window_Master()
    win_status = Window_Status()
    win_stop = Window_Stop()
    win_home.show()
    p1 = Process(target=opencv4)
    p1.start()
    app.exec_()