from PyQt5.QtWidgets import QApplication, QWidget
import os
from PyQt5.QtWidgets import *
import serial
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class SystemService(QWidget):
    timerSignal = pyqtSignal(bool)
    def __init__(self, parent):
        super().__init__(parent)
        
        

       
        port_list = ['COM3','COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10']
        baud_list = ['9600', '19200','115200']
        parent.portCBox.addItems(port_list)
        parent.BaudCBox.addItems(baud_list)

         # 포트를 여는 Open / Close 버튼을 눌렀을때 발생하는 이벤트 설정
        parent.Btn_close.setEnabled(False)     # 비활성화
        parent.Btn_open.setEnabled(True)       # 활성화
        parent.Btn_open.clicked.connect(self.openPort)
        parent.Btn_close.clicked.connect(self.closePort)
        
        #Interval Enter 1 버튼에 기능을 연결 => System measurement
        parent.inputBtn.clicked.connect(self.inputBtn_Push)

        # 타이머 시그널 연결
        

    def openPort(self):  
        selected_Port = self.parent().portCBox.currentText()
        selected_BaudRate = self.parent().BaudCBox.currentText()
        print(selected_BaudRate)
        
        # self.save_comm_settings()
        try:
            self.ser = serial.Serial(
                port=selected_Port,\
                baudrate=int(selected_BaudRate),\
                parity=serial.PARITY_NONE,\
                stopbits=serial.STOPBITS_ONE,\
                bytesize=serial.EIGHTBITS,\
                timeout=0)
            if self.ser.is_open:
                self.parent().Port_msg.setText("%s is Open %d bps" % (selected_Port, int(selected_BaudRate)))
                self.parent().Btn_open.setEnabled(False)    #open 버튼 비활성화
                self.parent().Btn_open.setStyleSheet("QPushButton { background-color : yellow }");#색상 변경
                self.parent().Btn_close.setEnabled(True)    #Close 버튼 활성화
                self.parent().Btn_open.setEnabled(False)    #open 버튼 비활성화
                self.parent().inputBtn.setEnabled(True)     #Enter 1 버튼 활성화
            else:
               self.parent().Port_msg.setText('Port Open failed')     


        except Exception as e:
            print(f"Unexpected error: {e}")
            notification = QMessageBox(self)
            notification.setWindowTitle("알림 메세지")
            notification.setText("지정된 포트를 찾을 수 없습니다.")
            notification.setIcon(QMessageBox.Information)
            notification.exec_()
            return
    
    def closePort(self):
        #print(self.ser)
        #print(hasattr(self, 'ser'))
        #print(self.ser.is_open)
        if hasattr(self, 'ser') and self.ser and self.ser.is_open:
            self.timer.stop()               # System measurement 중지
            self.timer_2.stop()             # All cell measurement 중지
            self.ser.close()
            self.Port_msg.setText('Port Closed')
            self.Btn_open.setStyleSheet("QPushButton { background-color : white }");#색상 변경
            self.inputBtn.setStyleSheet("QPushButton { background-color :white }");#색상 변경
            self.inputBtn_2.setStyleSheet("QPushButton { background-color : white }");#색상 변경
            self.Btn_open.setEnabled(True)      #open 버튼 활성화
            self.Btn_close.setEnabled(False)    #close 버튼 비활성화
            self.inputBtn.setEnabled(False)     #Enter 1 버튼 비활성화
        else:
            print("Serial port is not open.")
            self.openBtn.setEnabled(True)

    def inputBtn_Push(self):
        self.disp_cnt_1=0               # Enter 1 버튼이 눌리면 display count_1 = 0 부터 시작
        self.parent().inputBtn.setStyleSheet(  "QPushButton { background-color :yellow }");#색상 변경
        self.parent().inputBtn_2.setStyleSheet("QPushButton { background-color : lightgray }");#색상 변경
        if self.timer_2.isActive():
            self.timer_2.stop()

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
        self.Timer_Task()               # System measurement 함수 시작
    
