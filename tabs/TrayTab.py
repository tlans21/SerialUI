from PyQt5.QtWidgets import QWidget, QPushButton


class TrayTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initTrayUI()

    def initTrayUI(self):
        btn = QPushButton('Tray', self)
