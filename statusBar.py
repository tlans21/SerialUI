from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem,QVBoxLayout
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtCore import Qt, QUrl


class StatusBar(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.quick_widget = QQuickWidget()
        self.quick_widget.setSource(QUrl.fromLocalFile('./gauge.qml'))
        self.setGeometry(200, 200, 1000, 700)

        layout = QVBoxLayout(self)
        layout.addWidget(self.quick_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = StatusBar()
    myWindow.show()
    app.exec_()
