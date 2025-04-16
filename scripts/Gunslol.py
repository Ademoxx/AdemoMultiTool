import sys
import random
import string
import requests
from bs4 import BeautifulSoup
import time
import keyboard
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QComboBox, QSpinBox
)
from PySide6.QtCore import Qt, QThread, Signal
import os

pause = False

def toggle_pause():
    global pause
    pause = not pause
    if pause:
        print("\nPause activée. Appuyez sur F6 pour reprendre.\n")
    else:
        print("\nReprise...\n")

keyboard.add_hotkey("F6", toggle_pause)

os.system('cls' if os.name == 'nt' else 'clear')

def is_username_taken(username):
    url = f"https://guns.lol/{username}"
    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        return None

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        claim_button = soup.find("a", href=f"/register?claim={username}")
        return not bool(claim_button)
    elif response.status_code == 404:
        return False
    else:
        return None

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def get_random_word():
    try:
        with open("words.txt", "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
        return random.choice(words)
    except FileNotFoundError:
        print("Erreur : fichier 'words.txt' introuvable.")
        exit()

def get_random_name():
    names = [
        "alice", "bob", "charlie", "david", "emma", "frank", "grace", "henry", "irene", "jack", "karen", "leo",
        "michael", "nancy", "oliver", "paul", "quentin", "rachel", "steve", "tina", "ursula", "victor", "william",
        "xavier", "yvonne", "zach", "adam", "brian", "carl", "daniel", "edward", "felix", "george", "hannah"
    ] * 4
    return random.choice(names)

class SpammerThread(QThread):
    log_signal = Signal(str)

    def __init__(self, username_type, count, custom_usernames):
        super().__init__()
        self.username_type = username_type
        self.count = count
        self.custom_usernames = custom_usernames

    def run(self):
        usernames = []
        if self.username_type == "1":
            usernames = [generate_random_string(3) for _ in range(self.count)]
        elif self.username_type == "2":
            usernames = [generate_random_string(2) for _ in range(self.count)]
        elif self.username_type == "3":
            usernames = [get_random_word() for _ in range(self.count)]
        elif self.username_type == "4":
            usernames = [get_random_name() for _ in range(self.count)]
        elif self.username_type == "5":
            usernames = self.custom_usernames.split(",")

        with open("available.txt", "a", encoding="utf-8") as available_file:
            for username in usernames:
                while pause:
                    self.log_signal.emit("En pause... Appuyez sur F6 pour continuer.")
                    time.sleep(0.5)

                result = is_username_taken(username.strip())
                if result is True:
                    self.log_signal.emit(f"'{username}' est pris.")
                elif result is False:
                    self.log_signal.emit(f"'{username}' est DISPONIBLE !")
                    available_file.write(username.strip() + "\n")
                else:
                    self.log_signal.emit(f"ERREUR pour '{username}' (Utilise un VPN ou change de serveur VPN).")

class CyberpunkGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🟣 AdemoTool Username Gen&Check")
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
            QLineEdit, QComboBox, QSpinBox {
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

        # Title
        self.title = QLabel("Ademo UsernameGen&Check")
        self.title.setStyleSheet("font-size: 24px; color: #39ff14;")
        layout.addWidget(self.title)

        # Choose type of username
        self.username_type_combobox = QComboBox()
        self.username_type_combobox.addItem("3 Letter")
        self.username_type_combobox.addItem("2 Letter")
        self.username_type_combobox.addItem("Everyday Words")
        self.username_type_combobox.addItem("Well-Known Names")
        self.username_type_combobox.addItem("Custom")
        layout.addWidget(QLabel("Choose username type:"))
        layout.addWidget(self.username_type_combobox)

        # Input number of usernames to generate
        self.username_count_spinbox = QSpinBox()
        self.username_count_spinbox.setRange(1, 1000)
        layout.addWidget(QLabel("How many usernames to generate:"))
        layout.addWidget(self.username_count_spinbox)

        # Custom usernames input
        self.custom_usernames_input = QLineEdit()
        self.custom_usernames_input.setPlaceholderText("Enter comma-separated usernames")
        self.custom_usernames_input.setDisabled(True)
        layout.addWidget(self.custom_usernames_input)

        # Connect ComboBox selection to enable custom input
        self.username_type_combobox.currentTextChanged.connect(self.toggle_custom_input)

        # Start button
        self.start_button = QPushButton("Start Spamming")
        self.start_button.clicked.connect(self.start_spamming)
        layout.addWidget(self.start_button)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.setLayout(layout)

    def toggle_custom_input(self):
        if self.username_type_combobox.currentIndex() == 4:
            self.custom_usernames_input.setEnabled(True)
        else:
            self.custom_usernames_input.setDisabled(True)

    def start_spamming(self):
        username_type = str(self.username_type_combobox.currentIndex() + 1)
        count = self.username_count_spinbox.value()
        custom_usernames = self.custom_usernames_input.text() if username_type == "5" else ""
        
        self.thread = SpammerThread(username_type, count, custom_usernames)
        self.thread.log_signal.connect(self.log_area.append)
        self.thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CyberpunkGUI()
    window.resize(600, 600)
    window.show()
    sys.exit(app.exec())
