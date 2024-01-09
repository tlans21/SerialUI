from PyQt5.QtWidgets import QWidget, QPushButton


class RackTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initRackUI()

    def initRackUI(self):
        btn = QPushButton('Rack', self)
