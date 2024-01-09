from manangeApp import create_and_run_app

# connect = sqlite3.connect('../database/project')

# 커서 생성
# print('Debug')
# cursor = connect.cursor()


# cursor.execute("SELECT * FROM topics WHERE id = 1")

# data = cursor.fetchall()

# for row in data:
#     print(f'ID: {row[0]}, Name: {row[1]}')

# 테이블 생성

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QCheckBox, QTabWidget, QHBoxLayout
from tabs.HomeTab import HomeTab
from tabs.RackTab import RackTab
from tabs.SettingTab import SettingTab
from tabs.TrayTab import TrayTab
from tabs.AlarmTab import AlarmTab
from tabs.StyleTabWidget import StyleTabWidget
from PyQt5 import uic


from PyQt5.QtGui import QIcon
from statusBar import StatusBar
from PyQt5.QtWidgets import QPushButton
from quitButton import QuitButton
from PyQt5.QtCore import Qt


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.checkBox = None
        self.RackNum = None
        self.initUI()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 각 탭의 인스턴스를 생성합니다.
        tab_home = HomeTab(self)
        tab_rack = RackTab(self)
        tab_tray = TrayTab(self)
        tab_alarm = AlarmTab(self)
        tab_setting = SettingTab(self)

        # 탭들을 styleTabWidget 인스턴스를 생성하여 탭을 더합니다.
        tabs = StyleTabWidget(self)

        tabs.addTab(tab_home, 'Home')
        tabs.addTab(tab_rack, 'Rack')
        tabs.addTab(tab_tray, 'Tray')
        tabs.addTab(tab_alarm, 'Alarm')
        tabs.addTab(tab_setting, 'Setting')

        hbox = QHBoxLayout()
        hbox.addWidget(tabs)
        # RackInfo 탭을 클릭했을 때 각 번호에 맞는 폰트를 생성하기 위해 라벨 인스턴스를 생성합니다.

        self.setLayout(hbox)

        self.setWindowTitle('모니터링 프로그램')
        self.setGeometry(300, 200, 1300, 950)
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())