import os
from PyQt5.QtWidgets import *
import serial
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QUrl, QObject, QTimer, QSettings

class ALLCellService(QWidget):
    def __init__(self, parent, portSettingServiceInstance):
        super().__init__(parent)
        
        self.portSettingServiceInstance = portSettingServiceInstance
        self.ser = self.portSettingServiceInstance.getSerial


        # 타이머 중개자 객체 의존성 주입
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.startTimer2)

    def startTimer2(self):
        self.disp_cnt_1 += 1

    