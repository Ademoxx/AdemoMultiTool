import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QTabWidget
)
from PySide6.QtCore import Qt

class OSINTTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🕵️ OSINT MultiTool - Ademo")
        self.setMinimumSize(800, 600)
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
            }
            QPushButton {
                background-color: #111;
                border: 2px solid #00ffff;
                border-radius: 6px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #00ffff;
                color: black;
            }
        """)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_ip_lookup_tab(), "🌍 IP Lookup")
        self.tabs.addTab(self.create_phone_lookup_tab(), "📞 Phone Lookup")
        self.tabs.addTab(self.create_username_tracker_tab(), "👤 Username Tracker")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_ip_lookup_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IP address")
        self.ip_result = QTextEdit()
        self.ip_result.setReadOnly(True)

        search_btn = QPushButton("Lookup")
        search_btn.clicked.connect(self.lookup_ip)

        layout.addWidget(self.ip_input)
        layout.addWidget(search_btn)
        layout.addWidget(self.ip_result)
        tab.setLayout(layout)
        return tab

    def lookup_ip(self):
        ip = self.ip_input.text()
        try:
            res = requests.get(f"http://ip-api.com/json/{ip}").json()
            if res['status'] == 'fail':
                self.ip_result.setText("[!] IP not found or invalid.")
            else:
                result = f"IP: {res['query']}\nCountry: {res['country']}\nRegion: {res['regionName']}\nCity: {res['city']}\nISP: {res['isp']}"
                self.ip_result.setText(result)
        except Exception as e:
            self.ip_result.setText(f"[!] Error: {e}")

    def create_phone_lookup_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number with country code (e.g. +336...)")
        self.phone_result = QTextEdit()
        self.phone_result.setReadOnly(True)

        search_btn = QPushButton("Lookup")
        search_btn.clicked.connect(self.lookup_phone)

        layout.addWidget(self.phone_input)
        layout.addWidget(search_btn)
        layout.addWidget(self.phone_result)
        tab.setLayout(layout)
        return tab

    def lookup_phone(self):
        number = self.phone_input.text()
        try:
            res = requests.get(f"http://apilayer.net/api/validate?access_key=YOUR_ACCESS_KEY&number={number}&format=1").json()
            if not res.get("valid"):
                self.phone_result.setText("[!] Numéro invalide ou non trouvé.")
            else:
                result = f"Pays: {res['country_name']}\nOpérateur: {res['carrier']}\nLocalisation: {res['location']}"
                self.phone_result.setText(result)
        except Exception as e:
            self.phone_result.setText(f"[!] Erreur: {e}")

    def create_username_tracker_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_result = QTextEdit()
        self.username_result.setReadOnly(True)

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.track_username)

        layout.addWidget(self.username_input)
        layout.addWidget(search_btn)
        layout.addWidget(self.username_result)
        tab.setLayout(layout)
        return tab

    def track_username(self):
        username = self.username_input.text()
        if not username:
            self.username_result.setText("[!] Enter a username.")
            return

        self.username_result.setText("[⏳] Scanning...")
        QApplication.processEvents()

        sites = {
            "GitHub": f"https://github.com/{username}",
            "Twitter": f"https://twitter.com/{username}",
            "Instagram": f"https://instagram.com/{username}",
            "Facebook": f"https://facebook.com/{username}",
            "Reddit": f"https://www.reddit.com/user/{username}",
            "TikTok": f"https://www.tiktok.com/@{username}",
            "Pinterest": f"https://www.pinterest.com/{username}",
            "SoundCloud": f"https://soundcloud.com/{username}",
            "Twitch": f"https://www.twitch.tv/{username}",
            "YouTube": f"https://www.youtube.com/@{username}",
            "Medium": f"https://medium.com/@{username}",
            "GitLab": f"https://gitlab.com/{username}",
            "Replit": f"https://replit.com/@{username}",
            "BuyMeACoffee": f"https://www.buymeacoffee.com/{username}",
            "Keybase": f"https://keybase.io/{username}",
            "AskFM": f"https://ask.fm/{username}",
            "Wattpad": f"https://www.wattpad.com/user/{username}",
            "Linktree": f"https://linktr.ee/{username}",
            "Bandcamp": f"https://{username}.bandcamp.com",
            "Disqus": f"https://disqus.com/by/{username}",
            "CashApp": f"https://cash.app/${username}",
            "Pastebin": f"https://pastebin.com/u/{username}",
        }

        found = []
        for name, url in sites.items():
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    found.append(f"✅ {name}: {url}")
                elif r.status_code in [301, 403]:
                    found.append(f"⚠️ {name} (privé?): {url}")
            except:
                continue

        if not found:
            self.username_result.setText("[❌] Aucun résultat trouvé.")
        else:
            self.username_result.setText("\n".join(found))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OSINTTool()
    window.show()
    sys.exit(app.exec())

