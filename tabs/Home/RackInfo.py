from PyQt5.QtWidgets import QWidget, QPushButton, QTableWidget, QAbstractItemView, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class RackTab(QWidget):
    def __init__(self, parent=None, rack_number=None):
        super().__init__(parent)
        self.tableWidget = None
        self.rack_number = rack_number

        self.setStyleSheet("""
                    QLabel {
                        background-color: #C2C7CB;
                        border: 3px solid #C2C7CB;
                        margin-left: 2px;
                        margin-right: 2px;
                        overflow: visible;
                        border-bottom: none;
                        border-top-left-radius: 2px;
                        border-top-right-radius: 4px;
                        color: #1E2022;
                        font-family: 'Arial', sans-serif;
                        font-size: 8pt;
                        font-weight: bold;
                    }
                    QLabel:hover {
                        background-color: #C8D0D7;
                    }
                """)

    def initRackInfo(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(2)

        self.tableWidget.setFixedSize(252, 775)
        column_headers = ["Contents", "Alarm"]
        self.tableWidget.setHorizontalHeaderLabels(column_headers)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setSelectionMode(QAbstractItemView.NoSelection)

        self.tableWidget.move(200, 100)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)
