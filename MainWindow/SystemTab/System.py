from PyQt5.QtWidgets import QApplication, QWidget
import os
from PyQt5.QtWidgets import *
import serial
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QUrl, QObject, QTimer, QSettings

class SystemService(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
       
        self.mediatorInstance = None
        self.ser = None
        self.parent().inputBtn.clicked.connect(self.inputBtn_Push)
        
        self.timer = QTimer(self)   # Interval 1 timer - System Measurment
        self.timer.timeout.connect(self.timer_Task)

    def setMediatorInstance(self, mediatorInstance):
        self.mediatorInstance = mediatorInstance

    def setSerial(self, PortSerial):
        self.ser = PortSerial

    def timer_Task(self): 
        self.disp_cnt_1 += 1
        self.mediatorInstance.notify(self, "A")
        
    def inputBtn_Push(self):
        self.disp_cnt_1=0               # Enter 1 버튼이 눌리면 display count_1 = 0 부터 시작
        self.parent().inputBtn.setStyleSheet(  "QPushButton { background-color :yellow }");#색상 변경
        self.parent().inputBtn_2.setStyleSheet("QPushButton { background-color : lightgray }");#색상 변경
        
        # allCell 객체의 timer에게 중지 신호 보내기
        self.mediatorInstance.notify(self, "A")


        # All cell measurement 중지
        interval = self.parent().input_Interval.text().strip()

        if not self.ser:
            QMessageBox.warning(self.parent(), "Invalid Input", "포트를 연결하지 않았습니다.")
            return 

        if not interval or not interval.replace('.', '', 1).isdigit():
            QMessageBox.warning(self.parent(), "Invalid Input", "올바르지 못한 입력 값 입니다.")
            return
       
        self.period = int(interval) * 1000   # ms 단위 이므로 1000울 곱합니다.
        
        if self.period < 1:
            QMessageBox.warning(self.parent(), "Invalid Input", "1초 이상의 Interval을 입력해주세요")
            return

        self.timer.start(self.period)   # 10000 period
        self.timer_Task()               # System measurement 함수 시작
    
