# 
# 'python -m serial.tools.list_ports'  will print a list of available ports. 
# It is also possible to add a regexp as first argument and the list will only include entries that matched.
#
#

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
import serial
import time
import csv
from PyQt5.QtCore import Qt, QUrl, QObject, QTimer, QSettings
from PyQt5.QtGui import QColor, QFont
from MainWindow.SystemTab.System import SystemService
from MainWindow.AllCellTab.AllCell import ALLCellService
from MainWindow.Mediator.TimerMediator import TimerMediatorService
from MainWindow.PortSettings.PortSetting import PortSettingService
#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.

if getattr(sys, 'frozen', False):
    # Running in PyInstaller bundle
    script_dir = os.path.dirname(sys.executable)
else:
    # Running as a script
    script_dir = os.path.dirname(os.path.abspath(__file__))

ui_file_path = os.path.join(script_dir, "My_gui_test_4.ui")

form_class = uic.loadUiType(ui_file_path)[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.tabWidget_1.setTabEnabled(0, False)
        # Port 서비스 객체 생성
        self.portSettingServiceInstacne = PortSettingService(self)
        # system 서비스 생성
        self.systemServiceInstance = SystemService(self, self.portSettingServiceInstacne)
        # all Cell 서비스 객체 생성
        self.allCellServiceInstance = ALLCellService(self, self.portSettingServiceInstacne)
        # system, allCell Service, portSettingService 객체 중개자 인스턴스 생성 
        self.TimerMediatorInstance = TimerMediatorService(self, self.systemServiceInstance, self.allCellServiceInstance)
        




if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()