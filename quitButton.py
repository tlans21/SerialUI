from PyQt5.QtWidgets import QPushButton


class QuitButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.move(770, 650)
        self.clicked.connect(self.quit_application)



    def quit_application(self):
        self.window().close()