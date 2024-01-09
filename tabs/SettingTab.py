from PyQt5.QtWidgets import QWidget, QPushButton


class SettingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initSettingUI()

    def initSettingUI(self):
        btn = QPushButton('Setting', self)
