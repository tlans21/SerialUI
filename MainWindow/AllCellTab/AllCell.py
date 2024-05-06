from PyQt5.QtWidgets import QApplication, QWidget
import os
from PyQt5.QtWidgets import *
import serial

class ALLCellService(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.all_cell_Servcie_instance = ALLCellService
        self.mediatorInstance = None
        # 타이머 중개자 객체 의존성 주입
        self.cnt = 0
    def setSerial(self, PortSerial):
        self.ser = PortSerial
   
    def setMediatorInstance(self, mediatorInstance):
        self.mediatorInstance = mediatorInstance
    
    def test(self):
        self.cnt += 1
        print(self.cnt)