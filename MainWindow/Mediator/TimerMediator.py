from PyQt5.QtWidgets import QApplication, QWidget
import os
from PyQt5.QtWidgets import *
import serial
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QUrl, QObject, QTimer, QSettings
from MainWindow.AllCellTab.AllCell import ALLCellService
from MainWindow.SystemTab.System import SystemService

class TimerMediatorService(QWidget):
    
    def __init__(self, parent, systemServiceInstance, allCellServiceInstance):
        super().__init__(parent)
        self.systemServiceInstance = systemServiceInstance
        self.allCellServiceInstance = allCellServiceInstance # 

        self.portSettingServiceInstance = self.systemServiceInstance.getPortSettingServiceInstance() # 포트 세팅 서비스

        # 타이머 
        self.timer = None
        self.timer2 = None
        # 시그널 슬롯 설정
        self.parent().inputBtn.clicked.connect(self.check)
        self.parent().inputBtn_2.clicked.connect(self.check_2)
        self.parent().Btn_close.clicked.connect(self.closePort)

        

    def check(self):
        self.timer1 = self.systemServiceInstance.timer
        self.timer2 = self.allCellServiceInstance.timer2
        print("timerTest")
        if self.timer2.isActive():
            self.timer2.stop()
            print("실행중이던 Timer2를 중지시키고 Timer1을 실행")

        self.systemServiceInstance.setOnClickSystemBtn() # systemTab Start 버튼 클릭 이벤트
    
    def check_2(self):
        self.timer1 = self.systemServiceInstance.timer
        self.timer2 = self.allCellServiceInstance.timer2

        if self.timer1.isActive():
            self.timer1.stop()
            print("실행 중이던 Timer1을 중지시키고 Timer2를 실행")
        
        self.allCellServiceInstance.setOnClickAllCellBtn()

    def closePort(self):
        if self.timer1:
            if self.timer1.isActive():
                print("타이머 1 중지")
                self.timer1.stop()
        if self.timer2:
            if self.timer2.isActive():
                print("타이머 2 중지")    
                self.timer2.stop()
        
        self.portSettingServiceInstance.closePort()



    

        

