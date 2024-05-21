import os
from PyQt5.QtWidgets import *
import serial
import time
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QUrl, QObject, QTimer, QSettings
import csv

class ALLCellService(QWidget):
    def __init__(self, parent, portSettingServiceInstance):
        super().__init__(parent)
        
        self.portSettingServiceInstance = portSettingServiceInstance
        self.ser = self.portSettingServiceInstance.getSerial()


        # 타이머 중개자 객체 의존성 주입
        

        # 타이머 생성
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.startTimer2)
        self.record_flag_2 = False
        self.parent().csvBtn_2.clicked.connect(self.csvBtn_2_Push)
        
    def setOnClickAllCellBtn(self):
        self.ser = self.portSettingServiceInstance.getSerial()
        
        self.disp_cnt_2 = 0               # Enter 1 버튼이 눌리면 display count_1 = 0 부터 시작
        self.parent().inputBtn.setStyleSheet(  "QPushButton { background-color :lightgray }");#색상 변경
        self.parent().inputBtn_2.setStyleSheet("QPushButton { background-color : yellow }");#색상 변경
        
        
        # All cell measurement 중지
        interval = self.parent().input_Interval_2.text().strip()

        if not self.ser:
            QMessageBox.warning(self.parent(), "Invalid Input", "포트를 연결하지 않았습니다.")
            return 

        if not interval or not interval.replace('.', '', 1).isdigit():
            QMessageBox.warning(self.parent(), "Invalid Input", "올바르지 못한 입력 값 입니다.")
            return
       
        self.period_2 = int(interval) * 1000   # ms 단위 이므로 1000울 곱합니다.
        
        if self.period_2 < 5000:
            QMessageBox.warning(self.parent(), "Invalid Input", "1초 이상의 Interval을 입력해주세요")
            return
        
        self.timer2.start(self.period_2)   # 10000 period
        self.startTimer2()               # System measurement 함수 시작

    # All Cell measurement 함수
    def startTimer2(self): 
        self.disp_cnt_2 += 1    # Measurement 횟수 숫자 표시
        self.parent().label_cnt2.setStyleSheet("color: red")  # Set text color to red
        self.parent().label_cnt2.setText(str(self.disp_cnt_2))
        # START => Data Write & Read & Display task
        self.text_2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's'] 
        for step2, data2 in enumerate(self.text_2):
            encode_data2 = data2.encode()
            self.ser.write(encode_data2) #Send A~E for request data
            time.sleep(0.1)  
            
            buffer2 = [0 for i in range(72)] 

            if self.ser.readable():
                print(self.ser.in_waiting)
                res = self.ser.read(72)

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
                    self.parent().tableWidget_2.setItem(step2, col, alldata)

                for col in range(0, len(display_T)):
                    #self.tableWidget_2.setItem(index, col, QTableWidgetItem(str(csv2_data[col])))
                    T_data = QTableWidgetItem(str(display_T[col]))
                    T_data.setTextAlignment(0x0004 | 0x0080)  # Qt.AlignCenter
                    self.parent().Temp_table.setItem(step2, col, T_data)    

            if (self.record_flag_2):
                with open('atos.csv', 'a', newline='',  encoding='ANSI') as csv_file:
                    f2a = csv.writer(csv_file)
                    f2a.writerow(csv2_V)
                
                with open('Tall.csv', 'a', newline='',  encoding='ANSI') as csv_file:
                    f2b = csv.writer(csv_file)
                    f2b.writerow(csv2_T)
                
            self.ser.reset_input_buffer()
    
    def csvBtn_2_Push(self):
        if (self.record_flag_2==False):
            self.record_flag_2 = True
            self.parent().csvBtn_2.setStyleSheet("background-color: yellow;")
            self.parent().csvBtn_2.setText('...Saving... Click to Stop')
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
            self.parent().csvBtn_2.setText('Click to Save')
            self.parent().csvBtn_2.setStyleSheet("background-color: white;")
    