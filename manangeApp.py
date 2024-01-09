from PyQt5.QtWidgets import QApplication, QWidget
import sys

def create_and_run_app():
    app = QApplication(sys.argv)  # 해당 클래스에 대한 객체를 생성합니다.
    win = QWidget()  # 윈도우에 대한 객체 생성
    win.show()  #
    app.exec_()  # 이벤트 루프 시작 : 이벤트 루프가 시작되면 GUI 프로그램은 사용자가 '닫기' 버틑을 누를 때 까지 종료하지 않고 계속 실행됩니다.
    return


