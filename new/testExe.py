# _8_2 버전 변경사항
# - All cell measurement 데이터 archive 코딩 수정
# - csv 저장 코딩 수정

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
import serial
import time
import csv
from PyQt5.QtCore import Qt, QUrl, QObject, QTimer, QThread, pyqtSignal,  QSettings
from PyQt5.QtGui import QColor, QFont


# serial port 
ser = serial.Serial(
    port='COM3',\
    baudrate=115200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)

if ser.isOpen() == False: #시리얼 포트가 open인지 확인
    ser.open() #시리얼 포트를 연다

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.

if getattr(sys, 'frozen', False):
    # Running in PyInstaller bundle
    script_dir = os.path.dirname(sys.executable)
else:
    # Running as a script
    script_dir = os.path.dirname(os.path.abspath(__file__))

ui_file_path = os.path.join(script_dir, "My_gui_8_2.ui")

form_class = uic.loadUiType(ui_file_path)[0]


#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.record_flag_1 = False  # system data   file record  = NO
        self.record_flag_2 = False  # All cell data file record  = NO

        self.disp_cnt_1=0   # System  Measurement count  = display count_1
        self.disp_cnt_2=0   # All cell measurement count = display count_2

        #timer 관련
        self.timer = QTimer(self)   # Interval 1 timer - System Measurment
        self.timer_2 = QTimer(self) # Interval 2 timer - All cell measurement
        
        self.timer.timeout.connect(self.Timer_Task)         # System measurement
        self.timer_2.timeout.connect(self.Timer_2_Task)     # All Cell measurement
        
        #Interval Enter 1 버튼에 기능을 연결 => System measurement
        self.inputBtn.clicked.connect(self.inputBtn_Push)
        
        #Interval 2 Enter 2 버튼에 기능을 연결 => All Cell Data
        self.inputBtn_2.clicked.connect(self.inputBtn_2_Push)

        #System save click 버튼에 기능을 연결 => csv file save
        self.csvBtn.clicked.connect(self.csvBtn_Push)   # System measurement save
        
        #Module save click 2 버튼에 기능을 연결 => csv file save 2
        self.csvBtn_2.clicked.connect(self.csvBtn_2_Push)   # All Cell measurement save

    # System measurement time interval set & 측정 시작    
    def inputBtn_Push(self):
        self.disp_cnt_1=0               # Enter 1 버튼이 눌리면 display count_1 = 0 부터 시작
        self.timer_2.stop()             # All cell measurement 중지
        interval = int(self.input_Interval.text())
        self.period = interval * 1000   # ms 단위 이므로 1000울 곱합니다.
        self.timer.start(self.period)   # 10000 period
        self.Timer_Task()               # System measurement 함수 시작

    # All cell measurement time interval set & 측정 시작
    def inputBtn_2_Push(self):
        self.disp_cnt_2=0               # Enter 2 버튼이 눌리면 display count_2 = 0 부터 시작
        self.timer.stop()               # System measurement 중지
        interval_2 = int(self.input_Interval_2.text())
        #print(interval)
        self.period_2 = interval_2 * 1000 # ms 단위 
        self.timer_2.start(self.period_2) # 10000 period
        self.Timer_2_Task()             # All cell measurement 함수 시작   

    # System measurement data 파일 저장 시작 & 종료   
    def csvBtn_Push(self):
        if (self.record_flag_1==False):
            self.record_flag_1 = True
            self.csvBtn.setStyleSheet("background-color: yellow;")
            self.csvBtn.setText('...Saving... Click to Stop')
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
            self.csvBtn.setText('Click to Save')
            self.csvBtn.setStyleSheet("background-color: white;")
                    
    # All cell measurement data 파일 저장 시작 & 종료   
    def csvBtn_2_Push(self):
        if (self.record_flag_2==False):
            self.record_flag_2 = True
            self.csvBtn_2.setStyleSheet("background-color: yellow;")
            self.csvBtn_2.setText('...Saving... Click to Stop')
            with open('atos.csv', 'a', newline='',  encoding='ANSI') as csv_file_2:
                f2a = csv.writer(csv_file_2)
                header_2a = ("Cnt","Module #","V1","V2","V3","V4","V5","V6","V7","V8","V9","V10","V11","V12","V13","V14","V15","V16","V17","V18","V19","V20")
                f2a.writerow(header_2a)
            
            with open('Tall.csv', 'a', newline='',  encoding='ANSI') as csv_file:
                f2b = csv.writer(csv_file)
                header_2b = ("Cnt","Module #","T1","T2","T3","T4","T5","T6","T7","T8","T9","T10","T11","T12","T13","T14","T15","T16","T17","T18","T19","T20")
                f2b.writerow(header_2b)    
        else:
            self.record_flag_2=False
            self.csvBtn_2.setText('Click to Save')
            self.csvBtn_2.setStyleSheet("background-color: white;")
   
    # Diagnostic bit 그래픽 표시
    def bitCheck(self, bit):
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


    def Timer_Task(self): 
        self.disp_cnt_1 += 1   # Measurement 횟수 숫자 표시
        self.label_cnt.setStyleSheet("color: blue")  # Set text color to blue
        self.label_cnt.setText(str(self.disp_cnt_1))
    
        # START => Data Write & Read & Display task
        self.text = ['A', 'B', 'C', 'D', 'E'] 
        csv1_data = []
        for step, data in enumerate(self.text):
            encode_data = data.encode()
            ser.write(encode_data) #Send A~E for request data
            time.sleep(0.1)    
            
            if ser.readable():
                res = ser.read(65)
                hex_representation = ' '.join([format(byte, '02X') for byte in res])
                #print(hex_representation)
                buffer = hex_representation.split()
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
                            self.tableWidget.setItem(step*5+i, col, cdata)

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

                    display_E = (Vrack, Irack, SOC, BMS_MODE, Relay, FAN, Vtarget)                         
                    csv_data_E = (self.disp_cnt_1, Vrack, Irack, SOC, BMS_MODE, Relay, FAN, Vtarget, Diagnostic)                         

                    for row in range(len(display_E)):
                        item_E = QTableWidgetItem(str(display_E[row]))
                        self.systemTable.setItem(row, 0, item_E)

                    for row in range(0, 11):
                        item_diag = self.bitCheck((Diagnostic_list[row]))
                        self.DiagnosticTable.setItem(row, 0, item_diag)    
               
                    if (self.record_flag_1):
                            with open('Sysdata.csv', 'a', newline='',  encoding='ANSI') as csv_file:
                                f1b = csv.writer(csv_file)
                                f1b.writerow(csv_data_E)


# All Cell measurement 함수
    def Timer_2_Task(self): 
        self.disp_cnt_2 += 1    # Measurement 횟수 숫자 표시
        self.label_cnt2.setStyleSheet("color: red")  # Set text color to red
        self.label_cnt2.setText(str(self.disp_cnt_2))
        # START => Data Write & Read & Display task
        self.text_2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's'] 
        for step2, data2 in enumerate(self.text_2):
            encode_data2 = data2.encode()
            ser.write(encode_data2) #Send A~E for request data
            time.sleep(0.1)    

            if ser.readable():
                res = ser.read(72)
                hex_representation = ' '.join([format(byte, '02X') for byte in res])
                buffer2 = hex_representation.split()
                        
                Vcell_list = []              
                Mod =  int(buffer2[3],16) 
                Vcell_list = [Mod]
                for i in range(0,20):                  
                    Vcell_H = int(buffer2[2*i + 4],16)
                    Vcell_L = int(buffer2[2*i + 5],16)
                    Vcell = round(float(Vcell_H *256 + Vcell_L) * 0.001, 3)
                    Vcell_list.append(Vcell)
               
                display_V= Vcell_list   # Mod번호 + V1~V20
                csv2_V=[]
                csv2_V =[self.disp_cnt_2]
                csv2_V += Vcell_list    # Cnt + Mod번호 + V1~V20

                Tcell_list = []
                for i in range(48,68):                  
                    Tcell =  int(buffer2[i],16) -50
                    Tcell_list.append(Tcell)

                display_T= Tcell_list   # T1 ~ T20
                csv2_T=[]
                csv2_T=[self.disp_cnt_2, Mod]
                csv2_T += Tcell_list    # Cnt + Mod번호 + V1~V20

                cnt =  int(buffer2[70],16)

                for col in range(0, len(display_V)):
                    #self.tableWidget_2.setItem(step2, col, QTableWidgetItem(str(csv2_data[col])))
                    alldata = QTableWidgetItem(str(display_V[col]))
                    alldata.setTextAlignment(0x0004 | 0x0080)  # Qt.AlignCenter
                    self.tableWidget_2.setItem(step2, col, alldata)

                for col in range(0, len(display_T)):
                    #self.tableWidget_2.setItem(index, col, QTableWidgetItem(str(csv2_data[col])))
                    T_data = QTableWidgetItem(str(display_T[col]))
                    T_data.setTextAlignment(0x0004 | 0x0080)  # Qt.AlignCenter
                    self.Temp_table.setItem(step2, col, T_data)    

            if (self.record_flag_2):
                with open('atos.csv', 'a', newline='',  encoding='ANSI') as csv_file:
                    f2a = csv.writer(csv_file)
                    f2a.writerow(csv2_V)
                
                with open('Tall.csv', 'a', newline='',  encoding='ANSI') as csv_file:
                    f2b = csv.writer(csv_file)
                    f2b.writerow(csv2_T)
                
        
            
if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()