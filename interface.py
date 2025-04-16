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
    {"label": "soon", "script": "scripts/soon.py"},
    {"label": "soon", "script": "scripts/soon.py"},
    {"label": "soon", "script": "scripts/soon.py"},
    {"label": "InfoTool", "script": "scripts/info.py"},
]

class AdemoTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AdemoTool")
        self.setMinimumSize(1000, 650)
        self.setStyleSheet(self.get_cyberpunk_style())
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Titre principal
        title = QLabel("🧠 AdemoTool #FREE")
        title.setFont(QFont("Orbitron", 34, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: #00ffff;
            margin-bottom: 40px;
        """)
        main_layout.addWidget(title)

        # Grille
        grid_layout = QGridLayout()
        grid_layout.setSpacing(25)

        # Couleurs cycliques
        colors = [
            "#00ffff", "#ff00ff", "#39ff14", "#ff6ec7", "#ffd700",
            "#ff4500", "#00ffcc", "#ff1493", "#7fff00", "#ff6347"
        ]

        for i, config in enumerate(buttons_config):
            label = config["label"]
            script = config["script"]
            color = colors[i % len(colors)]

            button = QPushButton(label)
            button.setCursor(Qt.PointingHandCursor)
            button.setMinimumHeight(50)
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #111111;
                    color: {color};
                    border: 2px solid {color};
                    border-radius: 14px;
                    font-family: 'Consolas';
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px 20px;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    color: black;
                }}
            """)

            # Ombre néon
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setBlurRadius(20)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QColor(color))
            button.setGraphicsEffect(shadow)

            # Connexion au script
            button.clicked.connect(lambda _, path=script: self.launch_script(path))
            grid_layout.addWidget(button, i // 4, i % 4)

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)

    def launch_script(self, path):
        try:
            subprocess.Popen(["python", path])
        except Exception as e:
            print(f"Erreur lors de l'exécution de {path}: {e}")

    def get_cyberpunk_style(self):
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
