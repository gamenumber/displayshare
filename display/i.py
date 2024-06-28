import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt
from PIL import ImageGrab
from threading import Thread
from http.server import SimpleHTTPRequestHandler, HTTPServer
from Quartz.CoreGraphics import CGWindowListCopyWindowInfo, kCGWindowListOptionAll, kCGNullWindowID


class ScreenRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Screen Recorder")
        self.setWindowIcon(QIcon('icon.png'))

        self.layout = QVBoxLayout()

        # 창 선택 콤보박스 생성
        self.window_combo = QComboBox(self)
        self.window_combo.addItem("Select a Window")
        self.layout.addWidget(self.window_combo)

        # 시작 및 정지 버튼
        self.start_button = QPushButton("Start Recording", self)
        self.stop_button = QPushButton("Stop Recording", self)
        self.stop_button.setEnabled(False)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        self.layout.addLayout(button_layout)

        # 녹화 상태 표시 라벨
        self.recording_label = QLabel("Not Recording", self)
        self.recording_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.recording_label)

        # 창 목록 업데이트 버튼
        self.update_button = QPushButton("Update Window List", self)
        self.layout.addWidget(self.update_button)

        self.setLayout(self.layout)

        # 버튼 연결
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        self.update_button.clicked.connect(self.update_window_list)

        # 타이머 초기화
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_screen)

        # Set up the local web server
        self.server_thread = Thread(target=self.run_server)
        self.server_thread.daemon = True
        self.server_thread.start()

        self.setGeometry(100, 100, 800, 600)
        self.show()

    def update_window_list(self):
        # 창 목록 업데이트
        self.window_combo.clear()
        self.window_combo.addItem("Select a Window")

        # Quartz를 사용하여 macOS 창 목록 가져오기
        window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)

        for window in window_list:
            try:
                window_name = window.get("kCGWindowOwnerName", "")
                window_title = window.get("kCGWindowName", "")
                if window_name and window_title:
                    self.window_combo.addItem(f"{window_name}: {window_title}")
            except Exception as e:
                print(f"Error accessing window info: {e}")

    def start_recording(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.recording_label.setText("Recording...")  # 녹화 중임을 표시하는 레이블 변경

        # 타이머 시작
        self.timer.start(250)  # 0.25초마다 capture_screen 메서드 호출

    def stop_recording(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.recording_label.setText("Not Recording")  # 녹화 중이 아님을 표시하는 레이블 변경
        self.timer.stop()

    def capture_screen(self):
        # Get selected window
        selected_window_text = self.window_combo.currentText()
        if selected_window_text == "Select a Window":
            return

        selected_window_name, selected_window_title = selected_window_text.split(":")
        selected_window_name = selected_window_name.strip()
        selected_window_title = selected_window_title.strip()

        # Use PyObjC to fetch window information
        import Quartz
        for window in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID):
            try:
                window_name = window.get("kCGWindowOwnerName", "")
                window_title = window.get("kCGWindowName", "")
                if window_name == selected_window_name and window_title == selected_window_title:
                    window_bounds = window.get("kCGWindowBounds", {})
                    x = int(window_bounds["X"])
                    y = int(window_bounds["Y"])
                    width = int(window_bounds["Width"])
                    height = int(window_bounds["Height"])
                    screenshot = QApplication.primaryScreen().grabWindow(0, x, y, width, height)
                    screenshot.save("screenshot.png")
                    break
            except Exception as e:
                print(f"Error capturing screenshot: {e}")

    def run_server(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Change directory to script's directory
        server_address = ('', 5001)
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        httpd.serve_forever()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenRecorder()
    sys.exit(app.exec_())
