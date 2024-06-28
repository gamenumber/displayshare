import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer, Qt

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

        self.setGeometry(100, 100, 800, 600)
        self.show()

    def update_window_list(self):
        # 창 목록 업데이트
        self.window_combo.clear()
        self.window_combo.addItem("Select a Window")

        # AppleScript를 사용하여 열린 창의 목록 가져오기
        script = """
        tell application "System Events"
            set windowList to {}
            repeat with proc in processes
                tell proc
                    repeat with win in windows
                        set end of windowList to name of proc & ":" & title of win
                    end repeat
                end tell
            end repeat
            return windowList
        end tell
        """
        applescript = subprocess.Popen(['osascript', '-'],
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True)
        stdout, stderr = applescript.communicate(script)
        
        if applescript.returncode == 0:
            window_list = stdout.strip().split(',')
            for window_info in window_list:
                try:
                    name, title = window_info.split(':')
                    self.window_combo.addItem(f"{name.strip()}: {title.strip()}")
                except ValueError:
                    # Splitting failed, handle the error (e.g., print warning)
                    print(f"Error parsing window info: {window_info}")

    def start_recording(self):
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.recording_label.setText("Recording...")  # 녹화 중임을 표시하는 레이블 변경

        # 선택된 창 객체 가져오기
        selected_window_text = self.window_combo.currentText()
        selected_window_name = selected_window_text.split(":")[0].strip()

        # TODO: 선택된 창을 녹화하는 코드 작성

        # 타이머 시작
        self.timer.start(1000)  # 1초마다 capture_screen 메서드 호출

    def stop_recording(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.recording_label.setText("Not Recording")  # 녹화 중이 아님을 표시하는 레이블 변경
        self.timer.stop()

    def capture_screen(self):
        # 선택된 창 객체 가져오기
        selected_window_text = self.window_combo.currentText()
        selected_window_name = selected_window_text.split(":")[0].strip()

        # TODO: 선택된 창의 스크린샷을 캡처하고 표시하는 코드 작성

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenRecorder()
    sys.exit(app.exec_())
