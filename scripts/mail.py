import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QTextEdit, QPushButton, QLabel
)
from PySide6.QtCore import Qt

class EmailTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📧 Email Tracker - OSINT v2")
        self.setMinimumSize(650, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #0a0a0a;
                color: #00ffff;
                font-family: 'Consolas';
                font-size: 14px;
            }
            QLineEdit, QTextEdit {
                background-color: #111;
                border: 1px solid #00ffff;
                border-radius: 6px;
                color: #00ffff;
                padding: 4px;
            }
            QPushButton {
                background-color: #111;
                border: 2px solid #00ffff;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #00ffff;
                color: black;
            }
        """)

        layout = QVBoxLayout()
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email (example@gmail.com)")
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        track_btn = QPushButton("Track Email")
        track_btn.clicked.connect(self.track_email)

        layout.addWidget(QLabel("🔍 Email to investigate:"))
        layout.addWidget(self.email_input)
        layout.addWidget(track_btn)
        layout.addWidget(self.result_box)
        self.setLayout(layout)

    def track_email(self):
        email = self.email_input.text().strip()
        if not email:
            self.result_box.setText("[!] Please enter a valid email.")
            return

        self.result_box.setText("[⏳] Scanning email across multiple services...")
        QApplication.processEvents()

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        services = {
            "Twitter": ("https://twitter.com/account/begin_password_reset", {"account_identifier": email}),
            "Spotify": ("https://www.spotify.com/us/password-reset/", {"email": email}),
            "Instagram": ("https://www.instagram.com/accounts/account_recovery_send_ajax/", {"email_or_username": email}),
            "Facebook": ("https://www.facebook.com/login/identify", {"email": email}),
            "Snapchat": ("https://accounts.snapchat.com/accounts/password_reset_request", {"email": email}),
            "Pinterest": ("https://www.pinterest.com/password/reset/", {"email": email}),
            "Dropbox": ("https://www.dropbox.com/forgot", {"email": email}),
            "Twitch": ("https://www.twitch.tv/user/account-recovery", {"email": email}),
            "Microsoft": ("https://account.live.com/ResetPassword.aspx", {"email": email}),
            "Apple ID": ("https://iforgot.apple.com/password/verify/appleid", {"appleId": email}),
            "Reddit": ("https://www.reddit.com/password", {"email": email}),
            "LinkedIn": ("https://www.linkedin.com/checkpoint/rp/request-password-reset", {"userName": email}),
            "GitHub": ("https://github.com/password_reset", {"email": email}),
            "TikTok": ("https://www.tiktok.com/forgot-password", {"email": email}),
            "Yahoo": ("https://login.yahoo.com/forgot", {"username": email}),
            "Adobe": ("https://account.adobe.com/recovery", {"email": email}),
            "Deezer": ("https://www.deezer.com/password/reset", {"mail": email}),
            "Slack": ("https://slack.com/signin/find", {"email": email}),
            "Amazon": ("https://www.amazon.com/ap/forgotpassword", {"email": email}),
            "Netflix": ("https://www.netflix.com/LoginHelp", {"email": email}),
            "Discord": ("https://discord.com/api/v9/auth/forgot", {"email": email}),
        }

        results = []

        for name, (url, payload) in services.items():
            try:
                r = requests.post(url, data=payload, headers=headers, timeout=7)
                if r.status_code == 200 and "error" not in r.text.lower():
                    results.append(f"✅ {name}: response received (possible match)")
                else:
                    results.append(f"❌ {name}: no match or blocked")
            except Exception as e:
                results.append(f"⚠️ {name}: error - {str(e)}")

        self.result_box.setText("\n".join(results))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailTracker()
    window.show()
    sys.exit(app.exec())
