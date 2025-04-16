import sys
import random
import string
import json
import requests
import threading
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                               QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QSpinBox)
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt


class NitroGenGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nitro Generator - Cyberpunk Edition")
        self.setFixedSize(600, 500)
        self.init_ui()
        self.webhook_url = ""
        self.threads = []

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("⚡ Discord Nitro Generator ⚡")
        title.setFont(QFont("Orbitron", 18))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Webhook section
        self.webhook_input = QLineEdit()
        self.webhook_input.setPlaceholderText("Enter Webhook URL (optional)")
        layout.addWidget(self.webhook_input)

        # Threads input
        thread_layout = QHBoxLayout()
        thread_label = QLabel("Threads:")
        self.thread_input = QSpinBox()
        self.thread_input.setRange(1, 1000)
        self.thread_input.setValue(10)
        thread_layout.addWidget(thread_label)
        thread_layout.addWidget(self.thread_input)
        layout.addLayout(thread_layout)

        # Start button
        self.start_btn = QPushButton("💥 Start Generating")
        self.start_btn.clicked.connect(self.start_generating)
        layout.addWidget(self.start_btn)

        # Log output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)
        self.setStyle()

    def setStyle(self):
        # Cyberpunk dark mode style
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#0f0f0f"))
        palette.setColor(QPalette.Base, QColor("#1f1f1f"))
        palette.setColor(QPalette.Text, QColor("#39ff14"))
        palette.setColor(QPalette.Button, QColor("#8000ff"))
        palette.setColor(QPalette.ButtonText, QColor("#ffffff"))
        self.setPalette(palette)
        self.setFont(QFont("Courier New", 10))

        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #8000ff;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #a64dff;
            }
        """)

        self.webhook_input.setStyleSheet("background-color: #1f1f1f; color: #39ff14; padding: 5px;")
        self.output.setStyleSheet("background-color: #1f1f1f; color: #39ff14;")

    def log(self, message):
        self.output.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def send_webhook(self, code):
        payload = {
            'embeds': [{
                'title': 'Nitro Valid !',
                'description': f"**Nitro:**\n```{code}```",
                'color': 0x00ff00
            }],
            'username': 'Nitro Generator',
        }
        headers = {'Content-Type': 'application/json'}
        try:
            requests.post(self.webhook_url, data=json.dumps(payload), headers=headers)
        except:
            self.log("❌ Failed to send webhook")

    def check_nitro(self):
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        url = f"https://discord.gift/{code}"
        try:
            response = requests.get(
                f"https://discordapp.com/api/v6/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true",
                timeout=2
            )
            if response.status_code == 200:
                self.log(f"✅ VALID -> {url}")
                if self.webhook_url:
                    self.send_webhook(url)
            else:
                self.log(f"❌ INVALID -> {url}")
        except:
            self.log("⚠️ Connection error or timeout.")

    def thread_worker(self):
        self.check_nitro()

    def start_generating(self):
        self.webhook_url = self.webhook_input.text().strip()
        thread_count = self.thread_input.value()
        self.log("🚀 Starting Nitro Generation...")

        for _ in range(thread_count):
            t = threading.Thread(target=self.thread_worker)
            t.start()
            self.threads.append(t)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NitroGenGUI()
    window.show()
    sys.exit(app.exec())
