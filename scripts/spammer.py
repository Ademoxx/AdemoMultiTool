import sys
import json
import requests
import threading
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QSpinBox
from PySide6.QtCore import Qt, QThread, Signal

# Style cyberpunk colors
cyberpunk_style = """
    QWidget {
        background-color: #0f0f0f;
        color: #39ff14;
        font-family: Consolas;
        font-size: 14px;
    }
    QPushButton {
        background-color: #222;
        border: 1px solid #39ff14;
        padding: 8px;
    }
    QPushButton:hover {
        background-color: #111;
    }
    QLineEdit, QSpinBox {
        background-color: #1e1e1e;
        border: 1px solid #39ff14;
        color: #39ff14;
    }
    QTextEdit {
        background-color: #1a1a1a;
        border: 1px solid #39ff14;
        color: #39ff14;
    }
"""

class WebhookSpammer(QThread):
    log_signal = Signal(str)

    def __init__(self, webhook_url, message, threads_number):
        super().__init__()
        self.webhook_url = webhook_url
        self.message = message
        self.threads_number = threads_number

    def send_webhook(self):
        headers = {'Content-Type': 'application/json'}
        payload = {
            'content': self.message,
            'username': 'WebhookBot',  # Customize this if needed
            'avatar_url': 'https://example.com/avatar.png'  # Customize this if needed
        }
        try:
            response = requests.post(self.webhook_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            self.log_signal.emit(f"Message: {self.message} Status: Sent")
        except requests.exceptions.RequestException:
            self.log_signal.emit(f"Message: {self.message} Status: Rate Limit")

    def run(self):
        threads = []
        try:
            for _ in range(int(self.threads_number)):
                t = threading.Thread(target=self.send_webhook)
                t.start()
                threads.append(t)
        except Exception as e:
            self.log_signal.emit(f"Error: {str(e)}")

        for thread in threads:
            thread.join()

class WebhookGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AdemoTool Webhook Spammer")
        self.setStyleSheet(cyberpunk_style)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Title
        self.title = QLabel("Cyberpunk Webhook Spammer")
        self.title.setStyleSheet("font-size: 24px; color: #39ff14;")
        layout.addWidget(self.title)

        # Webhook URL
        self.webhook_url_input = QLineEdit()
        self.webhook_url_input.setPlaceholderText("Enter Webhook URL")
        layout.addWidget(QLabel("Webhook URL:"))
        layout.addWidget(self.webhook_url_input)

        # Message
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Enter the message to spam")
        layout.addWidget(QLabel("Message:"))
        layout.addWidget(self.message_input)

        # Number of threads
        self.thread_count_input = QSpinBox()
        self.thread_count_input.setRange(1, 1000)
        layout.addWidget(QLabel("Number of threads:"))
        layout.addWidget(self.thread_count_input)

        # Start Button
        self.start_button = QPushButton("Start Spamming")
        self.start_button.clicked.connect(self.start_spamming)
        layout.addWidget(self.start_button)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.setLayout(layout)

    def start_spamming(self):
        webhook_url = self.webhook_url_input.text()
        message = self.message_input.text()
        threads_number = self.thread_count_input.value()

        if webhook_url and message:
            self.spammer = WebhookSpammer(webhook_url, message, threads_number)
            self.spammer.log_signal.connect(self.log_area.append)
            self.spammer.start()
        else:
            self.log_area.append("Please enter both the Webhook URL and Message.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebhookGUI()
    window.resize(600, 600)
    window.show()
    sys.exit(app.exec())
