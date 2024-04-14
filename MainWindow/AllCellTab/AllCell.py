from PyQt5.QtWidgets import QApplication, QWidget
import os
from PyQt5.QtWidgets import *
import serial

class ALLCellService(QWidget):
    def __init__(self, parent, AllCellSerivce):
        super().__init__(parent)
        self.all_cell_Servcie_instance = ALLCellService
        