from PyQt5.QtWidgets import QWidget, QPushButton, QTabWidget


class StyleTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
                    QTabWidget::pane {
                        border: 1px solid #C2C7CB;
                        border-radius: 5px;
                        background-color: #F2F4F8;
                    }

                    QTabWidget::tab-bar {
                        alignment: left;
                    }

                    QTabBar::tab {
                        padding: 10px 40px;  /* Adjusted padding to move text to the left */
                        background-color: #C2C7CB;
                        border: 3px solid #C2C7CB;
                        margin-left: 2px;  /* Adjusted left margin to move text to the left */
                        margin-right: 2px;
                        overflow: visible;
                        border-bottom: none;
                        border-top-left-radius: 1px;
                        border-top-right-radius: 1px;
                        color: #000000;
                        font:sans-serif;
                        font-size: 8pt;
                        font-weight: bold;
                    }
                    QTabBar::tab:selected, QTabBar::tab:hover {
                        background-color: #C8D0D7;
                    }
                """)
