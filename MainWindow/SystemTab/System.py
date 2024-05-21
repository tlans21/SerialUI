from PyQt5.QtWidgets import QApplication, QWidget
import os
from PyQt5.QtWidgets import *
import serial
import time
import csv
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QUrl, QObject, QTimer, QSettings
from PyQt5.QtGui import QColor, QFont

class SystemService(QWidget):
    
    def __init__(self, parent, portSettingServiceInstance):
        super().__init__(parent)



        self.portSettingServiceInstance = portSettingServiceInstance
        self.ser = None
        
        self.timer = QTimer(self)   # Interval 1 timer - System Measurment
        self.timer.timeout.connect(self.startTimer)

        self.disp_cnt_1 = 0 # 실행 횟수 카운트
        # 
        self.Rly_state = "OFF"
        self.sent_ON_flag = "NO"
        self.sent_OFF_flag = "NO"
        # 시그널 슬롯 연결
        # Relay ON 버튼에 기능을 연결  => Btn_Rly_ON
        self.parent().Btn_Rly_ON.setEnabled(False)  # Relay ON 버튼 비활성화  
        self.parent().Btn_Rly_ON.clicked.connect(self.setOnClickRlyOnBtn)   # Relay ON
        # Relay OFF 버튼에 기능을 연결 => Btn_Rly_OFF
        self.parent().Btn_Rly_OFF.setEnabled(False)  # Relay OFF 버튼 비활성화  
        self.parent().Btn_Rly_OFF.clicked.connect(self.setOnClickRlyOffBtn)   # Relay OFF
        self.parent().csvBtn.clicked.connect(self.csvBtn_Push)
        # 기록 플래그 => True : 기록 시작, False : 기록 시작 X
        self.record_flag_1 = False

    def getPortSettingServiceInstance(self):
        return self.portSettingServiceInstance

    def setOnClickRlyOnBtn(self): 
        msg = QMessageBox()
        msg.setText("Are you sure [ON] ?")
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        retval = msg.exec_()

        if retval == QMessageBox.Yes :
            print('messagebox Yes : ', retval)

            if (self.Rly_state == "OFF"):
                self.Rly_state = "ON"
                self.sent_ON_flag = "NO"
                self.parent().Btn_Rly_ON.setStyleSheet("background-color: red;")
                self.parent().Btn_Rly_OFF.setStyleSheet("background-color: white;")           

            elif retval == QMessageBox.No :
                return
    def setOnClickRlyOffBtn(self):
        msg = QMessageBox()
        msg.setText("Are you sure [OFF] ?")
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        
        retval = msg.exec_()

        if retval == QMessageBox.Yes :
            print('messagebox Yes : ', retval)

            if (self.Rly_state == "ON"):
                self.Rly_state = "OFF"
                self.sent_OFF_flag = "NO"
                self.parent().Btn_Rly_OFF.setStyleSheet("background-color: red;")
                self.parent().Btn_Rly_ON.setStyleSheet("background-color: white;")
            
            elif retval == QMessageBox.No :
                return

    def checkBit(self, bit):
        item = QTableWidgetItem()

        font = QFont()
        if bit == 0:
            font.setPointSize(10)
            item.setFont(font)
            item.setText(" ◯")
            item.setForeground(QColor("black"))    
        else:
            font.setPointSize(8)
            item.setFont(font)
            item.setText(" 🔴")
            item.setForeground(QColor("red"))

        return item

    def startTimer(self): 
        # 포트 연결이 끊기거나 연결되어 있지 않을시 진행 안되도록 수정
        if self.ser == None:
            return
        self.parent().Btn_close.setEnabled(False)
        self.parent().Btn_close.setStyleSheet(  "QPushButton { background-color :gray}");
        self.disp_cnt_1 += 1   # Measurement 횟수 숫자 표시
        self.parent().label_cnt.setStyleSheet("color: blue")  # Set text color to blue
        self.parent().label_cnt.setText(str(self.disp_cnt_1))
        
        self.parent().Btn_Rly_ON.setEnabled(True)  # Relay ON 버튼 활성화  
        self.parent().Btn_Rly_OFF.setEnabled(True)  # Relay ON 버튼 활성화 

        if ((self.Rly_state == "ON") and (self.sent_ON_flag == "NO") == 1) :
            self.text = ['A', 'B', 'C', 'D', 'E', 'Z']     
            self.sent_ON_flag = "YES"
            print("RLY ON CMD SENT")
        
        elif ( ( (self.Rly_state == "OFF") and (self.sent_OFF_flag == "NO") )== 1 ):
            self.text = ['A', 'B', 'C', 'D', 'E', 'Y']
            self.sent_OFF_flag = "YES"
            print("RLY OFF CMD SENT")
        
        else:
            self.text = ['A', 'B', 'C', 'D', 'E']

        csv_data = []

        for step, data in enumerate(self.text):
            encode_data = data.encode()
            
            
            self.ser.write(encode_data) #Send A~E for request data
            time.sleep(0.1)  

            buffer = [0 for i in range(65)]
            cnt = 0

            if self.ser.readable():
                if (self.ser.in_waiting < 65):
                    
                    self.ser.reset_input_buffer()
                    
                elif (self.ser.in_waiting == 65):
                    
                    while True:
                        
                        Rx = ' '.join([format(byte, '02X') for byte in self.ser.read(1)])
                        
                        buffer[cnt] = Rx
                        cnt += 1
                        #  buffer의 index가 0 ~ 64 총 65개가 만들어짐.
                        if cnt == 65:
                            # 종료 신호가 0x03가 아니라면 cnt 초기화 후 다시 읽어들여야함.
                            if Rx != '03':
                                cnt = 0
                                self.ser.reset_input_buffer()
                                buffer = [0 for i in range(65)] # 버퍼 초기화
                            else:
                                break # 정상 동작이므로 while문 탈출

                    display_data = []  
                    # 입력 값이 'A', 'B', 'C', 'D' 일때 
                    if 0 <= step <= 3: 
                        
                        for i in range(0, 5):
                            Mod_n = int(buffer[(i*12)+3],16)

                            Vmodule_H = int(buffer[(i*12)+4],16)
                            Vmodule_L = int(buffer[(i*12)+5],16)
                            Vmodule = round(float(Vmodule_H *256 + Vmodule_L) * 0.1, 2)
                        
                            Vcmax_H = int(buffer[(i*12)+6],16)
                            Vcmax_L = int(buffer[(i*12)+7],16)
                            Vcmax   = round(float(Vcmax_H *256 + Vcmax_L) * 0.001, 3)
                            
                            Vcmin_H = int(buffer[(i*12)+8],16)
                            Vcmin_L = int(buffer[(i*12)+9],16)
                            Vcmin = round(float(Vcmin_H *256 + Vcmin_L) * 0.001, 3)
                            Vdiff = Vcmax - Vcmin
                            Vdiff = "{:.3f}".format(Vcmax-Vcmin)
                            Tmax =  int(buffer[(i*12)+10],16) -50
                            Tmin =  int(buffer[(i*12)+11],16) -50
                            Tdiff = Tmax - Tmin
                            
                            Bal_H = int(buffer[i*12 + 12], 16) 
                            Bal_M = int(buffer[i*12 + 13], 16)
                            Bal_L = int(buffer[i*12 + 14], 16) 
                            Balance = hex(Bal_H*(256 **2) + Bal_M*256 + Bal_L) 

                            display_data = (Vmodule, Vcmax, Vcmin, Vdiff, Tmax, Tmin, Tdiff, Balance)
                            csv1_data = (self.disp_cnt_1, Mod_n, Vmodule, Vcmax, Vcmin, Tmax, Tmin)
                            #print(csv_data)
                            
                            for col in range(0, len(display_data)):
                                cdata = QTableWidgetItem(str(display_data[col]))
                                cdata.setTextAlignment(0x0004 | 0x0080)  # Qt.AlignCenter
                                self.parent().tableWidget.setItem(step*5+i, col, cdata)

                            if (self.record_flag_1):
                                with open('AtoE.csv', 'a', newline='',  encoding='ANSI') as csv_file:
                                    f1a = csv.writer(csv_file)
                                    f1a.writerow(csv1_data)

                    # 입력 값이 'E' 일때
                    elif step == 4:
                        Vrack_H = int(buffer[3], 16)
                        Vrack_L = int(buffer[4], 16)
                        Vrack = Vrack_H *256 + Vrack_L
                        
                        Irack_H = int(buffer[5], 16)
                        Irack_L = int(buffer[6], 16)
                        Irack = ((Irack_H * 256 + Irack_L) * 0.1) - 500
                        
                        SOC_H = int(buffer[7], 16)
                        SOC_L = int(buffer[8], 16)
                        SOC = round((SOC_H * 256 + SOC_L) * 0.1, 1)

                        BMS_MODE = int(buffer[9], 16)
                        Mode = ""
                        if BMS_MODE == 2:
                            Mode = 'Fault '
                        elif BMS_MODE == 1:
                            Mode = 'Warning'
                        elif BMS_MODE == 0:
                            Mode = 'Normal'
                    
                        Relay = int(buffer[10], 16)
                        if Relay == 0:
                            Relay_Status = 'OFF'
                        else:
                            Relay_Status = 'ON'
                        
                        FAN = int(buffer[11], 16)
                        if FAN == 0:
                            FAN_Status = 'OFF'
                        else:
                            FAN_Status = 'ON'
                        
                        SW_Ver = round(int(buffer[12], 16) * 0.01, 2)
                        
                        # Dianostic 부분 쉬프트 연산
                        Diagnostic_H = int(buffer[13], 16)
                        Diagnostic_L = int(buffer[14], 16)
                        #print(type(Dianostic_H))
                        Diagnostic_list = []
                        Diagnostic = int(hex((Diagnostic_H * 256 + Diagnostic_L)), 16)
                        # 쉬프트 연산을 시작
                        shift_n = 0x01
                        # 총 2byte길이, 비트로 따지면 2^16임
                        for k in range(0, 16):
                            # Dianostic의 16비트와 16진수의 1을 비트 AND 시행
                            value = Diagnostic & shift_n
                            Diagnostic_list.append(value)
                            # 쉬프트 연산 이동
                            shift_n = (0x01 << (k+1))
                        #print(Diagnostic_list)
                        Vtarget_H = int(buffer[15], 16)
                        Vtarget_L = int(buffer[16], 16)
                        Vtarget = round(float(Vtarget_H *256 + Vtarget_L)*0.001,3)

                        Pre_charge = int(buffer[17],16)
                        #Pre_charge = 1
                        Main_relay = int(buffer[18],16)
                        #Main_relay = 1

                        bit_pre  = self.checkBit(Pre_charge)
                        bit_main = self.checkBit(Main_relay)
                        self.parent().RelayTable.setItem(0,0, bit_pre )
                        self.parent().RelayTable.setItem(1,0, bit_main)

                        display_E = (Vrack, Irack, SOC, BMS_MODE, Relay, FAN, Vtarget)                         
                        csv_data_E = (self.disp_cnt_1, Vrack, Irack, SOC, BMS_MODE, Relay, FAN, Vtarget, Diagnostic)                         

                        for row in range(len(display_E)):
                            item_E = QTableWidgetItem(str(display_E[row]))
                            self.parent().systemTable.setItem(row, 0, item_E)

                        for row in range(0, 11):
                            item_diag = self.checkBit((Diagnostic_list[row]))
                            self.parent().DiagnosticTable.setItem(row, 0, item_diag)    
                    
                        if (self.record_flag_1):
                                with open('Sysdata.csv', 'a', newline='',  encoding='ANSI') as csv_file:
                                    f1b = csv.writer(csv_file)
                                    f1b.writerow(csv_data_E)
        self.parent().Btn_close.setEnabled(True)
        self.parent().Btn_close.setStyleSheet(  "QPushButton { background-color :yellow }");
       


    def setOnClickSystemBtn(self):
        self.ser = self.portSettingServiceInstance.getSerial()
        
        self.disp_cnt_1 = 0               # Enter 1 버튼이 눌리면 display count_1 = 0 부터 시작
        self.parent().inputBtn.setStyleSheet(  "QPushButton { background-color :yellow }");#색상 변경
        self.parent().inputBtn_2.setStyleSheet("QPushButton { background-color : lightgray }");#색상 변경
        
        
        # All cell measurement 중지
        interval = self.parent().input_Interval.text().strip()

        if not self.ser:
            QMessageBox.warning(self.parent(), "Invalid Input", "포트를 연결하지 않았습니다.")
            return 

        if not interval or not interval.replace('.', '', 1).isdigit():
            QMessageBox.warning(self.parent(), "Invalid Input", "올바르지 못한 입력 값 입니다.")
            return
       
        self.period = int(interval) * 1000   # ms 단위 이므로 1000울 곱합니다.
        
        if self.period < 1000:
            QMessageBox.warning(self.parent(), "Invalid Input", "1초 이상의 Interval을 입력해주세요")
            return
        
        self.timer.start(self.period)   # 10000 period
        self.startTimer()               # System measurement 함수 시작


    def csvBtn_Push(self):
        if (self.record_flag_1==False):
            self.record_flag_1 = True
            self.parent().csvBtn.setStyleSheet("background-color: yellow;")
            self.parent().csvBtn.setText('...Saving... Click to Stop')
            with open('AtoE.csv', 'a', newline='',  encoding='ANSI') as csv_file:
                f1a = csv.writer(csv_file)
                header_1a  = ("cnt", "Module #", "Vmodule", "Vcmax", "Vcmin", "Tmax", "Tmin")
                f1a.writerow(header_1a)
            with open('Sysdata.csv', 'a', newline='',  encoding='ANSI') as csv_file:
                f1b = csv.writer(csv_file)
                header_1b  = ("cnt", "Vrack", "Irack", "SOC", "BMS_MODE", "RELAY", "FAN", "Vtarget", "Diagnostic")
                f1b.writerow(header_1b)

        else:
            self.record_flag_1=False
            self.parent().csvBtn.setText('Click to Save')
            self.parent().csvBtn.setStyleSheet("background-color: white;")
    

