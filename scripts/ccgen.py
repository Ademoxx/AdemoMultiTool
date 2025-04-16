import sys
import os
import random
import string
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
    QComboBox, QTextEdit, QHBoxLayout, QMessageBox, QLineEdit, QFileDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

def generate_random_credit_card(brand):
    if brand == "Visa":
        return '4' + ''.join(random.choice(string.digits) for _ in range(15))
    elif brand == "MasterCard":
        return '5' + ''.join(random.choice(string.digits) for _ in range(15))

def generate_random_expiry_date():
    month = random.randint(1, 12)
    year = random.randint(2025, 2030)
    return f"{month:02}/{year}"

def generate_random_cvv():
    return ''.join(random.choice(string.digits) for _ in range(3))

def luhn(card_number):
    digits = [int(d) for d in str(card_number)][::-1]
    checksum = sum(digits[::2]) + sum(sum(divmod(d * 2, 10)) for d in digits[1::2])
    return checksum % 10 == 0

class CreditCardGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CCGEN - ADEMO TOOL")
        self.setGeometry(200, 100, 700, 550)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")
        self.setup_ui()
        self.valid_cards = []

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("🔥 CCScrapper | discord.gg/database ; https://t.me/leakofdata 🔥")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setStyleSheet("color: #00F2EA; letter-spacing: 1px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        options_layout = QHBoxLayout()

        brand_label = QLabel("Marque :")
        brand_label.setFont(QFont("Segoe UI", 10))
        self.brand_combo = QComboBox()
        self.brand_combo.addItems(["Visa", "MasterCard"])
        self.brand_combo.setStyleSheet("""
            QComboBox {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #00F2EA;
                padding: 5px;
                border-radius: 4px;
            }
        """)

        quantity_label = QLabel("Nombre :")
        quantity_label.setFont(QFont("Segoe UI", 10))
        self.quantity_input = QLineEdit("100")
        self.quantity_input.setFixedWidth(80)
        self.quantity_input.setStyleSheet("""
            QLineEdit {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #00F2EA;
                padding: 4px;
                border-radius: 4px;
            }
        """)

        options_layout.addWidget(brand_label)
        options_layout.addWidget(self.brand_combo)
        options_layout.addSpacing(20)
        options_layout.addWidget(quantity_label)
        options_layout.addWidget(self.quantity_input)
        layout.addLayout(options_layout)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 6px;
                font-family: Consolas;
            }
        """)
        layout.addWidget(self.output)

        button_layout = QHBoxLayout()

        generate_btn = QPushButton("🔁 Générer")
        generate_btn.clicked.connect(self.generate_cards)

        save_btn = QPushButton("💾 Enregistrer les valides")
        save_btn.clicked.connect(self.save_valid_cards)

        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.clicked.connect(self.clear_output)

        for btn in [generate_btn, save_btn, clear_btn]:
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #00F2EA;
                    color: #1e1e1e;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #00CED1;
                }
            """)
            button_layout.addWidget(btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def generate_cards(self):
        brand = self.brand_combo.currentText()
        try:
            count = int(self.quantity_input.text())
            if count < 1:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Entrez un nombre valide (min: 1).")
            return

        self.valid_cards.clear()
        result_lines = []

        for _ in range(count):
            card_number = generate_random_credit_card(brand)
            expiry = generate_random_expiry_date()
            cvv = generate_random_cvv()
            valid = luhn(card_number)
            status = "✅ Valide" if valid else "❌ Invalide"
            line = f"{status} - {card_number} ({brand}) - Exp: {expiry} - CVV: {cvv}"
            result_lines.append(line)
            if valid:
                self.valid_cards.append(line)

        self.output.append("\n".join(result_lines))

    def save_valid_cards(self):
        if not self.valid_cards:
            QMessageBox.information(self, "Info", "Aucune carte valide à enregistrer.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer les CC valides", "valid_cards.txt", "Text Files (*.txt)")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("\n".join(self.valid_cards))
                QMessageBox.information(self, "Succès", "Fichier enregistré avec succès.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement : {e}")

    def clear_output(self):
        self.output.clear()
        self.valid_cards.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CreditCardGenerator()
    window.show()
    sys.exit(app.exec_())
