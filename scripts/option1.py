import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QLineEdit, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class GitHubEmailFinder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitHubLookup by ADEMO")
        self.setFixedSize(400, 280)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 12, 15, 12)

        title = QLabel("📡 GitHubLookup https://t.me/leakofdata")
        title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00F2EA;")
        layout.addWidget(title)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Pseudo GitHub")
        self.input.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                color: white;
                padding: 6px;
                border-radius: 4px;
                border: 1px solid #00F2EA;
                font-size: 10pt;
            }
        """)
        layout.addWidget(self.input)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setFixedHeight(130)
        self.result.setStyleSheet("""
            QTextEdit {
                background-color: #2a2a2a;
                color: #00ff90;
                border-radius: 4px;
                padding: 6px;
                font-family: Consolas;
                font-size: 9.5pt;
            }
        """)
        layout.addWidget(self.result)

        search_btn = QPushButton("🔍 Rechercher")
        search_btn.clicked.connect(self.search)
        search_btn.setCursor(Qt.PointingHandCursor)
        search_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #00F2EA;
                color: #1e1e1e;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #00CED1;
            }
        """)
        layout.addWidget(search_btn)

        self.setLayout(layout)

    def search(self):
        username = self.input.text().strip()
        if not username:
            QMessageBox.warning(self, "Erreur", "Entre un pseudo GitHub valide.")
            return

        url = f"https://api.github.com/users/{username}/events/public"
        response = requests.get(url)

        if response.status_code == 200:
            emails = set()
            events = response.json()
            for event in events:
                if 'payload' in event and 'commits' in event['payload']:
                    for commit in event['payload']['commits']:
                        email = commit['author'].get('email')
                        if email and '@users.noreply.github.com' not in email:
                            emails.add(email)

            if emails:
                self.result.setText("✅ Emails trouvés:\n" + "\n".join(emails))
            else:
                self.result.setText("⚠️ Aucun email public trouvé.")
        elif response.status_code == 404:
            self.result.setText("❌ Utilisateur introuvable.")
        else:
            self.result.setText(f"❌ Erreur HTTP : {response.status_code}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GitHubEmailFinder()
    window.show()
    sys.exit(app.exec_())
