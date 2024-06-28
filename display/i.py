import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QDesktopWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QScreen, QGuiApplication

class ScreenRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Screen Recorder")
        self.setWindowIcon(QIcon('icon.png'))

        self.layout = QVBoxLayout()

        # 화면 선택 콤보박스 생성
        self.screen_combo = QComboBox(self)
        self.screen_combo.addItem("Select a Screen")
        self.layout.addWidget(self.screen_combo)

        # 시작 및 정지 버튼
        self.start_button = QPushButton("Start Recording", self)
        self.stop_button = QPushButton("Stop Recording", self)
        self.stop_button.setEnabled(False)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        self.layout.addLayout(button_layout)

        # 화면 표시 라벨
        self.screen_label = QLabel(self)
        self.layout.addWidget(self.screen_label)

        self.setLayout(self.layout)

        # 버튼 연결
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

        # 타이머 초기화
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_screen)

        # 열린 화면 목록 업데이트
        self.update_screen_list()

        self.setGeometry(100, 100, 800, 600)
        self.show()

    def update_screen_list(self):
        # 열린 화면 목록 업데이트
        self.screen_combo.clear()
        self.screen_combo.addItem("Select a Screen")

        desktop = QDesktopWidget()
        for i in range(desktop.screenCount()):
            screen_rect = desktop.screenGeometry(i)
            self.screen_combo.addItem(f"Screen {i+1}", userData=screen_rect)

    def start_recording(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        # 선택된 화면 객체 가져오기
        selected_screen = self.screen_combo.currentData()

        if selected_screen:
            self.timer.start(1000)  # 1초마다 캡처
        else:
            self.stop_recording()

    def stop_recording(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.timer.stop()

    def capture_screen(self):
        # 선택된 화면 객체 가져오기
        selected_screen = self.screen_combo.currentData()

        if selected_screen:
            # 화면의 스크린샷 찍기
            screen = QGuiApplication.primaryScreen().grabWindow(0,
                                        selected_screen.x(), selected_screen.y(),
                                        selected_screen.width(), selected_screen.height())
            self.screen_label.setPixmap(screen)
            self.screen_label.setAlignment(Qt.AlignCenter)
        else:
            self.stop_recording()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenRecorder()
    sys.exit(app.exec_())
