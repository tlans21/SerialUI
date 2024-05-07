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
        self.allCellServiceInstance = allCellServiceInstance
    
        # 타이머 
        self.timer = None
        self.timer2 = None
        # 시그널 슬롯 설정
        self.parent().inputBtn.clicked.connect(self.check)

    def check(self):
        self.timer2 = self.allCellServiceInstance.timer2

        if self.timer2.isActive():
            self.timer2.stop()
            print("실행중이던 Timer2를 중지시키고 Timer1을 실행")

        self.systemServiceInstance.setOnClickSystemBtn() # systemTab Start 버튼 클릭 이벤트
        




    

        

