import sys
import subprocess
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel,
    QGraphicsDropShadowEffect
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt

# === 🔧 CONFIGURATION PERSONNALISÉE ===
buttons_config = [
    {"label": "GithubLookup", "script": "scripts/option1.py"},
    {"label": "CcGen", "script": "scripts/ccgen.py"},
    {"label": "RaidBot", "script": "scripts/raid.py"},
    {"label": "EventSpammer", "script": "scripts/event.py"},
    {"label": "GunsLol UserGEn&Check", "script": "scripts/Gunslol.py"},
    {"label": "WebHook Spammer", "script": "scripts/spammer.py"},
    {"label": "SearchDatabase", "script": "scripts/searcher.py"},
    {"label": "osintTool", "script": "scripts/osinttool.py"},
    {"label": "MailTracker", "script": "scripts/mail.py"},
    {"label": "soon", "script": "scripts/soon.py"},
    {"label": "soon", "script": "scripts/soon.py"},
    {"label": "soon", "script": "scripts/soon.py"},
    {"label": "soon", "script": "scripts/soon.py"},
    {"label": "soon", "script": "scripts/soon.py"},
    {"label": "soon", "script": "scripts/soon.py"},
    {"label": "soon", "script": "scripts/soon.py"},
    {"label": "soon", "script": "scripts/soon.py"},
    {"label": "soon", "script": "scripts/soon.py"},
    {"label": "soon", "script": "scripts/soon.py"},
    {"label": "InfoTool", "script": "scripts/info.py"},
]

class AdemoTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AdemoTool - #FREE")
        self.setMinimumSize(1000, 650)
        self.setStyleSheet(self.get_redtiger_style())
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Titre principal
        title = QLabel("💎 AdemoTool - Tool")
        title.setFont(QFont("Consolas", 34, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: #ff1a1a;
            margin-bottom: 40px;
            letter-spacing: 2px;
        """)
        main_layout.addWidget(title)

        # Grille
        grid_layout = QGridLayout()
        grid_layout.setSpacing(25)

        for i, config in enumerate(buttons_config):
            label = config["label"]
            script = config["script"]

            button = QPushButton(label)
            button.setCursor(Qt.PointingHandCursor)
            button.setMinimumHeight(50)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #0f0f0f;
                    color: #ff1a1a;
                    border: 2px solid #ff1a1a;
                    border-radius: 14px;
                    font-family: 'Consolas';
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px 20px;
                }}
                QPushButton:hover {{
                    background-color: #ff1a1a;
                    color: black;
                    border: 2px solid black;
                }}
            """)

            # Ombre néon rouge
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(25)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QColor("#ff1a1a"))
            button.setGraphicsEffect(shadow)

            button.clicked.connect(lambda _, path=script: self.launch_script(path))
            grid_layout.addWidget(button, i // 4, i % 4)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def launch_script(self, path):
        try:
            subprocess.Popen(["python", path])
        except Exception as e:
            print(f"Erreur lors de l'exécution de {path}: {e}")

    def get_redtiger_style(self):
        return """
            QWidget {
                background-color: #0a0a0a;
            }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdemoTool()
    window.show()
    sys.exit(app.exec())
