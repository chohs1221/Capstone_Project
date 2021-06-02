import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtGui import *

#UI파일 연결
ui_home = uic.loadUiType("./ui_workspace/home.ui")[0]
ui_start = uic.loadUiType("./ui_workspace/start.ui")[0]
ui_manager = uic.loadUiType("./ui_workspace/manager.ui")[0]
ui_status = uic.loadUiType("./ui_workspace/status.ui")[0]
ui_stop = uic.loadUiType("./ui_workspace/stop.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
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


if __name__ == "__main__" :
    data = 0
    mode = 0
    pump = 0
    stop_flag = 0

    empty = 0
    daily = 0    
    accumulate = 0

    app = QApplication(sys.argv)
    win_home = Window_Home()
    win_start = Window_Start()
    win_manager = Window_Manager()
    win_status = Window_Status()
    win_stop = Window_Stop()
    win_home.show()
    app.exec_()