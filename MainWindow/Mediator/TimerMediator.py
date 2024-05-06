from PyQt5.QtWidgets import QApplication, QWidget
import os
from PyQt5.QtWidgets import *
import serial
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from MainWindow.AllCellTab.AllCell import ALLCellService
from MainWindow.SystemTab.System import SystemService

class TimerMediatorService(QWidget):
    
    def __init__(self, parent, systemServiceInstance, allCellServiceInstance, portSettingServiceInstance):
        super().__init__(parent)
        self.portSettingSerivce = portSettingServiceInstance
        
        self.systemServiceInstance = systemServiceInstance
        self.systemServiceInstance.setMediatorInstance(self)
        self.systemServiceInstance.setSerial(self.portSettingSerivce.getSerial)

        self.allCellServiceInstance = allCellServiceInstance
        self.allCellServiceInstance.setMediatorInstance(self)
        self.allCellServiceInstance.setSerial(self.portSettingSerivce.getSerial)
        


        
    def notify(self, sender, event):
        if event == "A":
            print("A신호 보냄")
            self.allCellServiceInstance.test()



    

        

