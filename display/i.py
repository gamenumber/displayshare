import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 화면 선택 콤보박스 생성
        self.screen_combo = QComboBox()
        for i in range(QApplication.desktop().screenCount()):
            self.screen_combo.addItem(f"Screen {i}")
        layout.addWidget(self.screen_combo)

        # 화면 공유 버튼 생성
        self.share_button = QPushButton("Share Screen")
        self.share_button.clicked.connect(self.share_screen)
        layout.addWidget(self.share_button)

        # 화면 공유 라벨 생성
        self.screen_label = QLabel()
        layout.addWidget(self.screen_label)

        self.setLayout(layout)
        self.setWindowTitle("My PyQt Window")
        self.show()

    def share_screen(self):
        # 선택한 화면의 인덱스 가져오기
        screen_index = self.screen_combo.currentIndex()

        # 선택한 화면의 QScreen 객체 가져오기
        screen = QApplication.screens()[screen_index]

        # 선택한 화면의 스크린샷 찍기
        screenshot = screen.grabWindow(0)

        # QLabel에 QPixmap으로 표시
        self.screen_label.setPixmap(screenshot)
        self.screen_label.setAlignment(Qt.AlignCenter)

        # 1초마다 스크린샷 업데이트
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_screen)
        self.timer.start(1000)

    def update_screen(self):
        # 선택한 화면의 인덱스 가져오기
        screen_index = self.screen_combo.currentIndex()

        # 선택한 화면의 QScreen 객체 가져오기
        screen = QApplication.screens()[screen_index]

        # 선택한 화면의 스크린샷 찍기
        screenshot = screen.grabWindow(0)

        # QLabel에 QPixmap으로 표시
        self.screen_label.setPixmap(screenshot)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
