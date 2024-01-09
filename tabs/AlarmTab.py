from PyQt5.QtWidgets import QWidget, QPushButton


class AlarmTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initAlarmUI()

    def initAlarmUI(self):
        btn = QPushButton('Alarm', self)