from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import sys

class CyberpunkGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Info Tool")
        self.setFixedSize(500, 250)
        self.setStyleSheet("background-color: #0f0f1a;")  # fond noir-violet
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Label "made by ademo"
        label = QLabel("made by ademo")
        label.setFont(QFont("Consolas", 20, QFont.Bold))
        label.setStyleSheet("""
            color: #39ff14;
            padding: 10px;
            border: 2px solid #39ff14;
            border-radius: 10px;
        """)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Lien cliquable
        self.link_url = "https://discord.gg/ademotool"
        link_label = QLabel(f'<a href="{self.link_url}">{self.link_url}</a>')
        link_label.setFont(QFont("Consolas", 16))
        link_label.setAlignment(Qt.AlignCenter)
        link_label.setOpenExternalLinks(True)
        link_label.setStyleSheet("""
            QLabel {
                color: #00ffff;
                padding: 8px;
                border: 1px solid #00ffff;
                border-radius: 8px;
            }
            QLabel:hover {
                color: #ff00ff;
                border: 1px solid #ff00ff;
            }
        """)
        layout.addWidget(link_label)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CyberpunkGUI()
    window.show()
    sys.exit(app.exec())
