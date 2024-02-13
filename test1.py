import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidgetItem, QHBoxLayout, QWidget, QMessageBox, QFileDialog
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
import csv
from buttonService import ButtonService

if getattr(sys, 'frozen', False):
    # Running in PyInstaller bundle
    script_dir = os.path.dirname(sys.executable)
else:
    # Running as a script
    script_dir = os.path.dirname(os.path.abspath(__file__))

ui_file_path = os.path.join(script_dir, "customBtnTest.ui")


form_class = uic.loadUiType(ui_file_path)[0]


class WindowClass(QMainWindow, form_class): 
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button_service = ButtonService(self.customBtn) # ui 버튼 오브젝트명 customBtn을 대상으로 초기화자를 파라미터 입력, 버튼 서비스 객체를 생성
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())    
        