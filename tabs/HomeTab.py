from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from tabs.StyleTabWidget import StyleTabWidget
from tabs.Home.RackInfo import RackTab
from PyQt5.QtCore import Qt

class HomeTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rack_number_label = None
        self.initHomeUI()

    def initHomeUI(self):
        # Create instances of tabs 1, 2, and 3 that inform you of the rack status.
        rack_1 = RackTab(self, '1')
        rack_2 = RackTab(self, '2')
        rack_3 = RackTab(self, '3')
        rack_4 = RackTab(self, '4')

        # Label showing the current rack number
        self.rack_number_label = QLabel("Rack Num : 1", self)

        tabs = StyleTabWidget(self)
        tabs.addTab(rack_1, '1')
        tabs.addTab(rack_2, '2')
        tabs.addTab(rack_3, '3')
        tabs.addTab(rack_4, '4')

        hbox = QHBoxLayout()
        hbox.addWidget(tabs, Qt.AlignLeft)
        hbox.addWidget(self.rack_number_label, Qt.AlignLeft)
        self.setLayout(hbox)

        # Connect the currentChanged signal to the handle_tab_change method
        tabs.currentChanged.connect(lambda index: self.handle_tab_change(index))

    def handle_tab_change(self, index):
        # Slot to handle the currentChanged signal
        # Update the rack_number_label with the current tab number
        print(f"handle_tab_change called with index: {index}")
        self.rack_number_label.setText(f"Rack Num: {index + 1}")