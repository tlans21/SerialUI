from PyQt5.QtWidgets import QPushButton, QMessageBox

class ButtonService:
    def __init__(self, button: QPushButton):
        self.button = button
        self.setup_button()

    def setup_button(self):
        self.button.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        QMessageBox.information(None, "Button Clicked", "The button was clicked!")

