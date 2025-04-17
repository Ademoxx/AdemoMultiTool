import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QLineEdit, QTextEdit, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

class ModernSearchTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔍 AdemoTool - Search Tool")
        self.setGeometry(200, 100, 900, 650)
        self.setStyleSheet(self.get_stylesheet())
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("🔴 AdemoTool Search Tool")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #FF5555;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtext = QLabel("Select a folder and enter a keyword to search in files.")
        subtext.setStyleSheet("color: #AAAAAA; font-size: 13px;")
        subtext.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtext)

        self.btn_choose_folder = QPushButton("📁 Choose Folder")
        self.btn_choose_folder.clicked.connect(self.choose_folder)
        layout.addWidget(self.btn_choose_folder)

        self.folder_path_label = QLabel("No folder selected.")
        self.folder_path_label.setStyleSheet("color: #888888;")
        layout.addWidget(self.folder_path_label)

        hbox = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Enter keyword to search...")
        hbox.addWidget(self.search_input)

        self.btn_search = QPushButton("Start Search")
        self.btn_search.clicked.connect(self.start_search)
        hbox.addWidget(self.btn_search)
        layout.addLayout(hbox)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setFont(QFont("Consolas", 10))
        layout.addWidget(self.result_box)

        self.setLayout(layout)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Database Folder")
        if folder:
            self.folder_path = folder
            self.folder_path_label.setText(f"Selected folder: {folder}")

    def start_search(self):
        search_term = self.search_input.text().strip()
        if not hasattr(self, 'folder_path') or not self.folder_path:
            QMessageBox.warning(self, "⚠️ No Folder", "Please choose a folder first.")
            return
        if not search_term:
            QMessageBox.warning(self, "⚠️ No Keyword", "Please enter a keyword to search.")
            return

        self.result_box.clear()
        self.result_box.append(f"<span style='color:#66D9EF;'>Searching for: <b>{search_term}</b></span>\n")
        files_searched = 0
        results_found = 0

        for root, _, files in os.walk(self.folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                    except UnicodeDecodeError:
                        with open(filepath, 'r', encoding='latin-1') as f:
                            lines = f.readlines()

                    files_searched += 1
                    for i, line in enumerate(lines, 1):
                        if search_term in line:
                            results_found += 1
                            highlighted = line.strip().replace(
                                search_term,
                                f"<span style='background-color:#FF5555;color:#FFFFFF;padding:2px;'>{search_term}</span>"
                            )
                            self.result_box.append(
                                f"<br><b style='color:#FFD700;'>File:</b> {filepath}<br>"
                                f"<b style='color:#5FBE6B;'>Line {i}:</b> {highlighted}"
                            )
                except Exception as e:
                    self.result_box.append(f"<br><b style='color:red;'>Error reading file:</b> {filepath}<br>{e}")

        self.result_box.append(f"<br><hr><br><b>Total files searched:</b> {files_searched}")
        self.result_box.append(f"<b>Total matches found:</b> {results_found}")

    def get_stylesheet(self):
        return """
            QWidget {
                background-color: #1e1e1e;
                color: #FFFFFF;
                font-family: 'Segoe UI';
            }
            QPushButton {
                background-color: #333333;
                color: #ffffff;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
            QLineEdit {
                padding: 10px;
                border-radius: 8px;
                background-color: #2e2e2e;
                color: #ffffff;
            }
            QTextEdit {
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 10px;
            }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernSearchTool()
    window.show()
    sys.exit(app.exec_())
