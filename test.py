import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidgetItem, QHBoxLayout, QWidget, QMessageBox
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtCore import Qt, QUrl, QObject, QTimer, QThread, pyqtSignal,  QSettings
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from datetime import datetime
import time
import os
import serial
import threading
import time
now = time.time()
 

if getattr(sys, 'frozen', False):
    # Running in PyInstaller bundle
    script_dir = os.path.dirname(sys.executable)
else:
    # Running as a script
    script_dir = os.path.dirname(os.path.abspath(__file__))

ui_file_path = os.path.join(script_dir, "testUserInterface.ui")


form_class = uic.loadUiType(ui_file_path)[0]


class Thread1(QThread):
    #parent = MainWidget을 상속 받음.
    def __init__(self, parent, ser, dataCheckPoint, input_Value_signal, dataCheckPoint_signal, progress_signal, text_list):
        super().__init__(parent)
        self.ser = ser
        self.dataCheckPoint = dataCheckPoint
        self.input_Value_signal = input_Value_signal
        self.dataCheckPoint_signal = dataCheckPoint_signal
        self.progress_signal = progress_signal
        self.text = text_list
    def run(self):

        
        for step, data in enumerate(self.text):
            total_steps = len(self.text)
            self.dataCheckPoint = False
            self.received_data = []
            print("문자열 변환 : ", time.strftime("%H:%M:%S", time.gmtime(now)))
            self.input_Value_signal.emit(data)
            self.dataCheckPoint_signal.emit(self.dataCheckPoint)
            encode_data = data.encode()
            self.ser.write(encode_data)
            # 아래의 값은 serial의 스레드가 데이터를 읽는 시간 * 9 는 되어야함
            time.sleep(1)
            progress_percentage = int((step + 1) / total_steps * 100)
            self.progress_signal.emit(progress_percentage)



class WindowClass(QMainWindow, form_class):
    input_Value_signal = pyqtSignal(str)
    dataCheckPoint_signal = pyqtSignal(bool)
    # Home Tab의 데이터 프레임 A~E에서의 프로그레스 시그널
    progress_signal = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # -------------------------------------------Home TAB ---------------------------------------------------------------------------------
        self.input_Value = None
        self.input_Value_signal.connect(self.updateInputValue)
        self.dataCheckPoint_signal.connect(self.updateDataCheckPoint)
        self.progress_signal.connect(self.updateProgressBar)
        self.received_data = []
        
        
        # 시스템 테이블 column 헤더와 row 헤더 안보이도록 설정
        self.SystemTable.horizontalHeader().setVisible(False)
        self.SystemTable.verticalHeader().setVisible(False)
        
        # Dianostic 테이블 column 헤더와 row 헤더 안보이도록 설정
        self.dianostic_table.horizontalHeader().setVisible(False)
        self.dianostic_table.verticalHeader().setVisible(False)

        # 탭 변경할 때마다 테이블 위젯의 값을 갱신
        self.RackInfoTab.currentChanged.connect(self.updateContent)
        # Initialize the content
        self.updateContent(0)
        # period_pbar = progressbar를 뜻함. Home Tab 초기는 0 % 임.
        self.period_pbar_value = 0
        self.period_pbar.setValue(self.period_pbar_value)
    
        self.load_settings() 
        # 주기적으로 버튼이 클릭되어 데이터가 나타나도록 함.
        self.simulate_timer = QTimer(self)
        self.period = 15000
        # 주기적으로 작동되는 태스크를 설정
        self.simulate_timer.timeout.connect(self.startPeriodicTask)
        # 버튼 눌렀을 때의 시그널 설정
        self.inputBtn.setEnabled(False)
        self.inputBtn.clicked.connect(self.inputBtn_Push)
        # 포트를 여는 Open 버튼을 눌렀을때 발생하는 이벤트 설정
        self.closeBtn.setEnabled(False)
        self.openBtn.setEnabled(True)
        self.openBtn.clicked.connect(self.openPort)
        
        self.closeBtn.clicked.connect(self.closePort)
        # -------------------------------------------Home TAB ---------------------------------------------------------------------------------

        # ---------------------------------------------------------- Moudle Tab 부분 ---------------------------------------------------------
        
        # module탭의 테이블 헤더 삭제하는 메서드
        self.module_table_HeaderRemove()

        # ---------------------------------------------------------- Moudle Tab 부분 ---------------------------------------------------------

        # ---------------------------------------------------------- Setting Tab 부분 ---------------------------------------------------------
        self.inputBtn2.clicked.connect(self.inputBtn2_Push)
        self.inputBtn2_period = 30000
        self.simulate_timer2 = QTimer()
        self.simulate_timer2.timeout.connect(self.startPeriodicTask2)

        # ---------------------------------------------------------- Setting Tab 부분 ---------------------------------------------------------
    def load_settings_for_combo_box(self, key, combo_box):
        settings = QSettings("test", "test1")
        saved_index = settings.value(key, 0, type=int)
        combo_box.setCurrentIndex(saved_index)

    def load_settings(self):
        self.load_settings_for_combo_box("portCBox", self.portCBox)
        self.load_settings_for_combo_box("BaudCBox", self.BaudCBox)
        self.load_settings_for_combo_box("DataBitCBox", self.DataBitCBox)
        self.load_settings_for_combo_box("parityBitCBox", self.parityBitCBox)
        self.load_settings_for_combo_box("StopBitCBox", self.StopBitCBox)
    
    
    def save_settings(self):
        self.save_settings_for_combo_box("portCBox", self.portCBox)
        self.save_settings_for_combo_box("BaudCBox", self.BaudCBox)
        self.save_settings_for_combo_box("DataBitCBox", self.DataBitCBox)
        self.save_settings_for_combo_box("parityBitCBox", self.parityBitCBox)
        self.save_settings_for_combo_box("StopBitCBox", self.StopBitCBox)
        
    def save_settings_for_combo_box(self, key, combo_box):
        settings = QSettings("test", "test1")
        settings.setValue(key, combo_box.currentIndex()) 



    def updateInputValue(self, value):
        self.input_Value = value

    def updateDataCheckPoint(self, datacheckPoint):
        self.dataCheckPoint = datacheckPoint

    def openPort(self):
        # 시리얼 통신을 위한 콤보박스 지정하는 것을 저장
        self.inputBtn.setEnabled(True)
        self.save_settings()

        selected_Port = self.portCBox.currentText()
        selected_BaudRate = self.BaudCBox.currentText()
        selected_DataBit = self.DataBitCBox.currentText()
        selected_ParityBit= self.parityBitCBox.currentText()
        selected_StopBit = self.StopBitCBox.currentText()
           
        # 시리얼 통신 시작
        self.ser = serial.Serial(port = selected_Port, baudrate = int(selected_BaudRate), stopbits= int(selected_StopBit))

        def readthread():
            while True:
                
                if self.ser and self.ser.readable():
                    try:
                        res = self.ser.read(8)

                        hex_representation = ' '.join([format(byte, '02X') for byte in res])
                        print(hex_representation)
                        buffer = hex_representation.split()
                        for i in range(len(buffer)):
                            self.received_data.append(buffer[i])
                        
                        # 8byte를 읽고나서 8바이트 미만의 나머지 바이트를 읽어들이는 코드
                        time.sleep(0.05)
                        if self.ser.in_waiting < 8:
                            res = self.ser.read(self.ser.in_waiting) 
                            hex_representation = ' '.join([format(byte, '02X') for byte in res])
                            print(hex_representation)
                            buffer = hex_representation.split()

                            for i in range(len(buffer)):
                                self.received_data.append(buffer[i])
                            print(len(self.received_data))
                            self.updateTable()
                        
                    except serial.SerialException as e:
                        print(f"시리얼 포트에서 읽을 때 오류 발생: {e}")
                        return
                    except Exception as e:
                        print(f"Unexpected error: {e}")
                        return
                else:
                    # If self.ser is None or is unreadable
                    print("시리얼 포트가 열려 있지 않거나 읽을 수 없습니다.")
                    time.sleep(1)  # Set appropriate sleep time as needed
        if not self.ser.is_open:
            return    

        thread = threading.Thread(target=readthread)
        thread.start()

        self.closeBtn.setEnabled(True)
        self.openBtn.setEnabled(False)
        
    def closePort(self):
        print(self.ser)
        print(hasattr(self, 'ser'))
        print(self.ser.is_open)
        if hasattr(self, 'ser') and self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial port closed.")
            print(self.ser.is_open)
            self.openBtn.setEnabled(True)
            # 포트를 닫았으므로 입력 버튼 비활성화
            self.inputBtn.setEnabled(False)
        else:
            print("Serial port is not open.")
            self.openBtn.setEnabled(True)
            
    
    
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

    def startPeriodicTask(self):
        self.period_pbar_value = 0
        self.period_pbar.setValue(self.period_pbar_value)
        
        # 테이블들 비우기
        self.df_table.clearContents()
        
        for row in range(0, self.SystemTable.rowCount()):
            self.SystemTable.takeItem(row, 1)

        for row in range(0, self.dianostic_table.rowCount()):
            self.dianostic_table.takeItem(row, 1)
        self.text_list = ['A', 'B', 'C', 'D', 'E']
        periodicTaksThread = Thread1(self, self.ser, self.dataCheckPoint, self.input_Value_signal, self.dataCheckPoint_signal, self.progress_signal, self.text_list)
        periodicTaksThread.start()

        # self.period_pbar_Timer = QTimer(self)
        # self.period_pbar_Timer.timeout.connect()
        # self.period_pbar_Timer.start(200)  
        
    def inputBtn_Push(self):
        #데이터 체크포인트 설정
        self.dataCheckPoint = False
        # 입력된 주기
        interval = int(self.lineEdit_Interval.text())

        # 주기가 0.1 * 9 * 6 미만으로는 안됨. 약 6초이하로는 설정 안되도록 하고 종료시킴
        if interval < 8:
            notification = QMessageBox(self)
            notification.setWindowTitle("알림 메세지")
            notification.setText("8초 미만으로는 Interval을 설정할 수 없습니다.")
            notification.setIcon(QMessageBox.Information)
            notification.exec_()
            return
        
        self.period = interval * 1000 # ms 단위 이므로 1000울 곱합니다.


        # 주기적인 작업을 시작합니다.
        self.startPeriodicTask()

        # 주기적으로 버튼을 클릭하는 것을 시뮬레이션하기 위해 QTimer를 사용합니다.
        self.simulate_timer.start(self.period) # 10000 period
    
    def updateProgressBar(self, value):
        self.period_pbar_value = value
        self.period_pbar.setValue(self.period_pbar_value)

    
            
        
    def updateTable(self):
        print(len(self.received_data))
        main_table = getattr(self, 'df_table')
        print(self.text_list)
        # Home Tab 부분의 테이블 실행
        if self.text_list == ['A', 'B', 'C', 'D', 'E']:
            self.updateHomeTab()
            return
        elif self.text_list == ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']:
            self.updateModuleTab()
            return


    def updateHomeTab(self):
        STX = self.received_data[0]
        return_cmd = self.received_data[1]
        rack_num = self.received_data[2]
        
        # 한 번만 시행됨.
        if self.dataCheckPoint == False:
            print("datacheck")
            
            self.dataCheckPoint = True
            self.received_data.pop(0)
            self.received_data.pop(0)
            self.received_data.pop(0)

        
        # 입력 값이 'A', 'B', 'C', 'D' 일때 
        if 65 <= ord(self.input_Value) <= 68:
            separated_LengthList_12 = []
            for i in range(0, len(self.received_data) // 12):
                temp_list = []

                Vmodule_H = int(self.received_data[(i*12) + 1], 16)
                Vmodule_L = int(self.received_data[(i*12) + 2], 16)
                Voltage = round(float(Vmodule_H *256 + Vmodule_L) * 0.1, 2) 
                temp_list.append(str(Voltage) + " " + "V")
                
                
                Balance_H = int(self.received_data[i*12 + 9], 16) 
                Balance_M = int(self.received_data[i*12 + 10], 16)
                Balance_L = int(self.received_data[i*12 + 11], 16) 
                Balance_Value = hex(Balance_H * (256 **2) + Balance_M * 256 + Balance_L) 
                temp_list.append(Balance_Value)

                Vcell_max_H = int(self.received_data[(i*12) + 3], 16)
                Vcell_max_L = int(self.received_data[(i*12) + 4], 16)
                max_Cell = round(float(Vcell_max_H *256 + Vcell_max_L) * 0.001, 3)
                temp_list.append(str(max_Cell) + " "+ "V")            

                Vcell_min_H = int(self.received_data[(i*12) + 5], 16)
                Vcell_min_L = int(self.received_data[(i*12) + 6], 16)
                min_Cell = round(float(Vcell_min_H * 256 + Vcell_min_L) * 0.001, 3)
                temp_list.append(str(min_Cell) + " " + "V")
                Diff_V = round(abs(max_Cell - min_Cell), 3)
                temp_list.append(str(Diff_V) + " " + "V")
                max_T = int(self.received_data[(i*12) + 7], 16) - 50
                min_T = int(self.received_data[(i*12) + 8], 16) - 50
                temp_list.append(str(max_T) + " " + chr(176) + "C")
                temp_list.append(str(min_T) + " " + chr(176) + "C")
                diff_T = abs(max_T - min_T)
                temp_list.append(str(diff_T) + " " + chr(176) + "C")
                separated_LengthList_12.append(temp_list)
        # 입력 값이 'E' 일때
        elif ord(self.input_Value) == 69:
            list_fromDataFrame_E = []
            
            Vrack_H = int(self.received_data[0], 16)
            Vrack_L = int(self.received_data[1], 16)
            Vrack = Vrack_H *256 + Vrack_L
            list_fromDataFrame_E.append(Vrack)

           
            lrack_H = int(self.received_data[2], 16)
            lrack_L = int(self.received_data[3], 16)
            lrack = ((lrack_H * 256 + lrack_L) * 0.1) - 500
            list_fromDataFrame_E.append(lrack)
            
            
            SOC_H = int(self.received_data[4], 16)
            SOC_L = int(self.received_data[5], 16)
            SOC = round((SOC_H * 256 + SOC_L) * 0.1, 1)
            list_fromDataFrame_E.append(SOC)

            
            Relay = int(self.received_data[7], 16)
            # Relay의 상태
            if Relay == 0:
                Relay_Status = 'OFF'
            else:
                Relay_Status = 'ON'
            list_fromDataFrame_E.append(Relay_Status)


            FAN = int(self.received_data[8], 16)
            if FAN == 0:
                FAN_Status = 'OFF'
            else:
                FAN_Status = 'ON'
            list_fromDataFrame_E.append(FAN_Status)


            BMS_MODE = int(self.received_data[6], 16)
            Mode = ""
            if BMS_MODE == 2:
                Mode = 'Fault '
            elif BMS_MODE == 1:
                Mode = 'Warning'
            elif BMS_MODE == 0:
                Mode = 'Normal'
            list_fromDataFrame_E.append(Mode) 


            SW_Ver = round(int(self.received_data[9], 16) * 0.01, 2)
            print(SW_Ver)


            # Dianostic 부분 쉬프트 연산
            Dianostic_H = int(self.received_data[10], 16)
            Dianostic_L = int(self.received_data[11], 16)
            print(type(Dianostic_H))
            Dianostic_list = []
            Dianostic = int(hex((Dianostic_H * 256 + Dianostic_L)), 16)
            
            # 쉬프트 연산을 시작
            shift_n = 0x01
            # 총 2byte길이, 비트로 따지면 2^16임
            print(type(Dianostic))
            for k in range(0, 16):
                # Dianostic의 16비트와 16진수의 1을 비트 AND 시행
                value = Dianostic & shift_n
                Dianostic_list.append(value)
                # 쉬프트 연산 이동
                shift_n = (0x01 << (k+1))
            print(Dianostic_list)

        #입력 값이 'A'면, 모듈의 개수만큼의 행들의 값들이 채워진다.

        if self.input_Value == 'A':
            for row in range(len(separated_LengthList_12)):
                for column in range(len(separated_LengthList_12[row])):
                    item = QTableWidgetItem(str(separated_LengthList_12[row][column]))
                    self.df_table.setItem(row, column, item)
        elif self.input_Value == 'B':
            for row in range(len(separated_LengthList_12)):
                for column in range(len(separated_LengthList_12[row])):
                    item = QTableWidgetItem(str(separated_LengthList_12[row][column]))
                    self.df_table.setItem(row+5, column, item)
        elif self.input_Value == 'C':
            for row in range(len(separated_LengthList_12)):
                for column in range(len(separated_LengthList_12[row])):
                    item = QTableWidgetItem(str(separated_LengthList_12[row][column]))
                    self.df_table.setItem(row+10, column, item)
        elif self.input_Value == 'D':
            for row in range(len(separated_LengthList_12)):
                for column in range(len(separated_LengthList_12[row])):
                    item = QTableWidgetItem(str(separated_LengthList_12[row][column]))
                    self.df_table.setItem(row+15, column, item)
        elif self.input_Value == 'E':
            # System 배치
            for row in range(len(list_fromDataFrame_E)):
                # columnIdx가 1이므로 2번째 컬럼 시작. 
                columnIdx = 1
                item = QTableWidgetItem(str(list_fromDataFrame_E[row]))
                self.SystemTable.setItem(row, columnIdx, item)
            
            # Dianostic 배치
                
            # OverChangeCurrent    
            OverChangeCurrent = Dianostic_list[0]
            item = self.bitCheck(OverChangeCurrent)
            self.dianostic_table.setItem(0, 1, item)
            # OverDisChrageCurrent
            OverDisChrageCurrent = Dianostic_list[1]
            item = self.bitCheck(OverDisChrageCurrent)
            self.dianostic_table.setItem(1, 1, item)
            # OverTemperature
            OverTemperature = Dianostic_list[2]
            item = self.bitCheck(OverTemperature)
            self.dianostic_table.setItem(2, 1, item)
            # UnderTemperature
            UnderTemperature = Dianostic_list[3]
            item = self.bitCheck(UnderTemperature)
            self.dianostic_table.setItem(3, 1, item)
            # OverTemperatureDiff
            OverTemperatureDiff = Dianostic_list[7]
            item = self.bitCheck(OverTemperatureDiff)
            self.dianostic_table.setItem(7, 1, item)
            # Rack OVP
            Rack_OVP = Dianostic_list[8]
            item = self.bitCheck(Rack_OVP)
            self.dianostic_table.setItem(8, 1, item)

            # Rack DCDC Relay
            Rack_DCDC_Relay = Dianostic_list[11]
            item = self.bitCheck(Rack_DCDC_Relay)
            self.dianostic_table.setItem(11, 1, item)
        # 다시 초기화
        self.received_data = []
    def updateModuleTab(self):

        STX = self.received_data[0]
        return_cmd = self.received_data[1]
        rack_num = int(self.received_data[2], 16)
        Module_num = int(self.received_data[3], 16)
        # 한 번만 시행됨.
       
        
        self.received_data.pop(0) # STX 팝
        self.received_data.pop(0) # return_cmd 팝
        self.received_data.pop(0) # rack_num 팝
        self.received_data.pop(0) # Module_num 팝
        # Vcell
        
        Vcell_list = []
        for i in range(0, 22):
            # Vcell 부분
            # 0 ~ 43, 0~1 0, 2, 3 1    4,5, 2  40, 41 20 42 43, 21
            if i < 20:
                Vcell_H = int(self.received_data[2*i], 16)
                Vcell_L = int(self.received_data[2*i + 1], 16)
                Vcell = round(float(Vcell_H  * 256 + Vcell_L) * 0.001, 3) 
            # Vcell max
            elif i == 20:
                Vcell_max_H = int(self.received_data[2*i], 16)
                Vcell_max_L = int(self.received_data[2*i + 1], 16)
                Vcell = round(float(Vcell_max_H * 256 + Vcell_max_L) * 0.001, 3)
            # Vcell min
            elif i == 21:
                Vcell_max_H = int(self.received_data[2*i], 16)
                Vcell_max_L = int(self.received_data[2*i + 1], 16)
                Vcell = round(float(Vcell_max_H * 256 + Vcell_max_L) * 0.001, 3)
            # 0~19 인덱스까지 Vcell, 20, 21 max, min
            Vcell_list.append(Vcell)
        # Tcell
        Tcell_list = []
        for i in range(44, 64):
            # offset -50
            Tcell = int(self.received_data[i], 16) - 50
            Tcell_list.append(Tcell)
        # Tcell max, min
        Tcell_max = int(self.received_data[64], 16) - 50
        Tcell_list.append(Tcell_max)
        Tcell_min = int(self.received_data[65], 16) - 50
        Tcell_list.append(Tcell_min)

        # 값을 입력할 테이블 지정
        current_tableWidget = getattr(self, f'Module_table_{Module_num}')
        
        print(Module_num)
        
        for row in range(0, len(Vcell_list)):
            item = QTableWidgetItem(str(Vcell_list[row]))
            current_tableWidget.setItem(row, 0, item)

            item2 = QTableWidgetItem(str(Tcell_list[row]))
            current_tableWidget.setItem(row, 1, item2)

        self.received_data = []
        
        print("self.recived 비우기 성공")

    def module_table_HeaderRemove(self):
        for i in range(1, 21):
            # 테이블 1번부터 20번까지 지정
            current_tableWidget = getattr(self, f'Module_table_{i}')
            # 수직, 수평 헤더 안보이게 설정.
            current_tableWidget.horizontalHeader().setVisible(False)
            
    
    def updateContent(self, index):
        # 레이아웃이 누적되지 않도록 클릭때마다 지우기
        while self.horizontalLayout.count():
            item = self.horizontalLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            else:
                self.horizontalLayout.removeItem(item)


        current_rackWidget = getattr(self, f'Rack_{index + 1}')
        # current_tableWidget = getattr(self, f'rackTable_{index + 1}')

        # if current_rackWidget is None or current_tableWidget is None:
        #     print("Error: current_rackWidget or current_tableWidget is None")
        #     return
        
        

        # 테이블 값 갱신
        # for row in range(current_tableWidget.rowCount()):
        #     for column in range(current_tableWidget.columnCount()):
        #         item = QTableWidgetItem(f"a")
        #         item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # Make the item read-only
        #         current_tableWidget.setItem(row, column, item)

       
        

        # Create and set up QQuickWidget
        quickWidget = QQuickWidget(current_rackWidget)
        qml_file_path = os.path.join(script_dir, 'gauge.qml')
        quickWidget.setSource(QUrl.fromLocalFile(qml_file_path))
        quickWidget.setMinimumSize(100, 100)
        

        # 초침 바꾸기.
        qml_root_object = quickWidget.rootObject()
        print("qml_root_object:", qml_root_object)
        qml_child_object = qml_root_object.findChild(QObject, "myName")
        print("qml_child_object:", qml_child_object)
        gauge_value = qml_child_object.property("gauge_value")
        print("Current gauge_value:", gauge_value)
        gauge_value = qml_child_object.setProperty("gauge_value", 0.0)
        
        
       
        
       
        quickWidget2 = QQuickWidget(current_rackWidget)
        qml_file_path = os.path.join(script_dir, 'gauge.qml')
        quickWidget2.setSource(QUrl.fromLocalFile(qml_file_path))
        quickWidget2.setMinimumSize(100, 100)

        qml_root_object2 = quickWidget2.rootObject()
        qml_child_object2 = qml_root_object2.findChild(QObject, "myName")
        gauge_value = qml_child_object2.property("gauge_value")
        print("Current gauge_value:", gauge_value)
        # 최대 200.0, 최소 -200.0으로 속성 값 수정
        qml_child_object2.setProperty("maximumValue", 200.0)
        qml_child_object2.setProperty("minimumValue", -200.0)
        # 하위 계층의 하위인 circularGaugeStyle_object2 불러오기
        circularGaugeStyle_object2 = qml_child_object2.findChild(QObject, "Style")
        #간격을 나타내는 속성을 40으로 수정
        circularGaugeStyle_object2.setProperty("tickmarkStepSize", 40) 
        

        quickWidget3 = QQuickWidget(current_rackWidget)
        qml_file_path = os.path.join(script_dir, 'gauge.qml')
        quickWidget3.setSource(QUrl.fromLocalFile(qml_file_path))
        quickWidget3.setMinimumSize(100, 100)
        # 최상위 오브젝트 불러오기
        qml_root_object3 = quickWidget3.rootObject()
        
        qml_child_object3 = qml_root_object3.findChild(QObject, "myName")
        # 최대 100.0, 최소 0.0으로 속성 값 수정
        qml_child_object3.setProperty("maximumValue", 100.0)
        qml_child_object3.setProperty("minimumValue", 0.0)
        # 하위 계층의 하위인 circularGaugeStyle_object3 불러오기
        circularGaugeStyle_object3 = qml_child_object3.findChild(QObject, "Style")
        #간격을 나타내는 속성을 10으로 수정
        circularGaugeStyle_object3.setProperty("tickmarkStepSize", 10)

        self.horizontalLayout.addWidget(quickWidget)
        self.horizontalLayout.addWidget(quickWidget2)
        self.horizontalLayout.addWidget(quickWidget3)
    # --------------------------------------------------Setting Tab 부분의 메서드
    def inputBtn2_Push(self):
        interval = int(self.lineEdit_Interval_2.text())


        # 주기가 0.1 * 9 * 6 미만으로는 안됨. 약 6초이하로는 설정 안되도록 하고 종료시킴
        if interval < 30 :
            notification = QMessageBox(self)
            notification.setWindowTitle("알림 메세지")
            notification.setText("30초 미만으로는 Interval을 설정할 수 없습니다.")
            notification.setIcon(QMessageBox.Information)
            notification.exec_()
            return
        
        self.period2 = interval * 1000 # ms 단위 이므로 1000울 곱합니다.
        
        #데이터 체크포인트 설정
        self.dataCheckPoint = False
        # 주기적인 작업을 시작합니다.
        self.startPeriodicTask2()

        self.simulate_timer2.start(self.period2) # 30000 period


    def startPeriodicTask2(self):
        self.period_pbar_value = 0
        self.period_pbar.setValue(self.period_pbar_value)
        
        # 테이블들 비우기
        for i in range(1, 21):
            # 테이블 1번부터 20번까지 지정
            current_tableWidget = getattr(self, f'Module_table_{i}')
            # 테이블 비우기
            current_tableWidget.clearContents()
        # 
            
        self.text_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']
        periodicTaksThread2 = Thread1(self, self.ser, self.dataCheckPoint, self.input_Value_signal, self.dataCheckPoint_signal, self.progress_signal, self.text_list)
        periodicTaksThread2.start()
        
        # self.period_pbar_Timer = QTimer(self)
        # self.period_pbar_Timer.timeout.connect()
        # self.period_pbar_Timer.start(200)  


    # --------------------------------------------------Setting Tab 부분의 메서드
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())
