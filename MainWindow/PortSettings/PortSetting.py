import serial
import time
import csv
from PyQt5.QtCore import Qt, QUrl, QObject, QTimer, QSettings
from PyQt5.QtGui import QColor, QFont
from MainWindow.SystemTab.System import SystemService
from MainWindow.AllCellTab.AllCell import ALLCellService
from MainWindow.Mediator.TimerMediator import TimerMediatorService
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import *

class PortSettingService(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.ser = None

        port_list = ['COM3','COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'COM10']
        baud_list = ['9600', '19200','115200']
        parent.portCBox.addItems(port_list)
        parent.BaudCBox.addItems(baud_list)

         # 포트를 여는 Open / Close 버튼을 눌렀을때 발생하는 이벤트 설정
        self.parent().Btn_close.setEnabled(False)     # 비활성화
        self.parent().Btn_open.setEnabled(True)       # 활성화

        self.parent().Btn_open.clicked.connect(self.openPort)
        
        #Interval Enter 1 버튼에 기능을 연결 => System measurement
        
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
                self.parent().Btn_close.setStyleSheet("QPushButton { background-color : white }");
                self.parent().Btn_close.setEnabled(True)    #Close 버튼 활성화
                self.parent().Btn_open.setEnabled(False)    #open 버튼 비활성화
                self.parent().inputBtn.setEnabled(True)     #Enter 1 버튼 활성화
                self.parent().inputBtn_2.setEnabled(True)     #Enter 2 버튼 활성화
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
            # self.timer.stop()               # System measurement 중지
            # self.timer_2.stop()             # All cell measurement 중지
            self.ser.close()
            print(self.ser)
            self.ser = None
            self.parent().Port_msg.setText('Port Closed')
            self.parent().Btn_open.setStyleSheet("QPushButton { background-color : white }");#색상 변경
            self.parent().Btn_close.setStyleSheet("QPushButton { background-color : yellow }");#색상 변경
            self.parent().inputBtn.setStyleSheet("QPushButton { background-color :white }");#색상 변경
            self.parent().inputBtn_2.setStyleSheet("QPushButton { background-color : white }");#색상 변경
            self.parent().Btn_open.setEnabled(True)      #open 버튼 활성화
            self.parent().Btn_close.setEnabled(False)    #close 버튼 비활성화
            self.parent().inputBtn.setEnabled(False)     #Enter 1 버튼 비활성화
            self.parent().inputBtn_2.setEnabled(False)
        else:
            print("Serial port is not open.")
            self.parent().openBtn.setEnabled(True)
    
    def getSerial(self):
        return self.ser