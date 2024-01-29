import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QPushButton
from PyQt5.QtCore import QTimer

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Progress Bar Example')
        self.setGeometry(100, 100, 300, 150)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create a progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        # Create a button to start the cycle
        self.start_button = QPushButton('Start Cycle')
        self.start_button.clicked.connect(self.start_cycle)

        # Add widgets to the layout
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.start_button)

        # Set the layout for the main window
        self.setLayout(layout)

        # Timer for updating the progress bar
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)

        self.show()

    def start_cycle(self):
        # Start the cycle
        self.cycle_duration = 10000  # Example: 10 seconds
        self.elapsed_time = 0
        self.timer.start(100)  # Update progress every 100 milliseconds
        self.start_button.setEnabled(False)

    def update_progress(self):
        # Increment elapsed time
        self.elapsed_time += 100  # 100 milliseconds

        # Calculate progress percentage
        progress = (self.elapsed_time / self.cycle_duration) * 100

        # Update the progress bar value
        self.progress_bar.setValue(min(progress, 100))

        # If the cycle is completed, stop the timer
        if self.elapsed_time >= self.cycle_duration:
            self.timer.stop()
            self.start_button.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())