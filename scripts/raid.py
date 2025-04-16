import sys
import json
import asyncio
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QLineEdit, QTextEdit, QMessageBox, QFileDialog
)
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt, QThread, Signal
import discord
from discord.ext import commands

CONFIG = {
    "BOT_PRESENCE": {
        "type": "playing",
        "text": "AdemoTool #RAID"
    }
}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="+", intents=intents)

class BotThread(QThread):
    log_signal = Signal(str)

    def __init__(self, token):
        super().__init__()
        self.token = token

    def run(self):
        @bot.event
        async def on_ready():
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=CONFIG["BOT_PRESENCE"]["text"]))
            self.log_signal.emit(f"[+] Connecté en tant que {bot.user.name}")

        @bot.command()
        async def dmmembers(ctx):
            await ctx.send("Contenu du message à envoyer à tous les membres ?")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            msg = await bot.wait_for('message', check=check)
            message_content = msg.content
            count = 0

            for member in ctx.guild.members:
                if not member.bot:
                    try:
                        await member.send(message_content)
                        count += 1
                    except:
                        pass
            await ctx.send(f"Message envoyé à {count} membres.")

        @bot.command()
        async def banall(ctx):
            banned = 0
            for member in ctx.guild.members:
                if not member.bot:
                    try:
                        await member.ban(reason="Ban All command")
                        banned += 1
                    except:
                        pass
            await ctx.send(f"Banni {banned} membres.")

        @bot.command()
        async def kickall(ctx):
            kicked = 0
            for member in ctx.guild.members:
                if not member.bot:
                    try:
                        await member.kick(reason="Kick All command")
                        kicked += 1
                    except:
                        pass
            await ctx.send(f"Expulsé {kicked} membres.")

        @bot.command()
        async def spamchannels(ctx):
            await ctx.send("Nombre de messages à envoyer ?")
            def check(m): return m.author == ctx.author and m.channel == ctx.channel
            msg1 = await bot.wait_for('message', check=check)
            count = int(msg1.content)

            await ctx.send("Contenu du message ?")
            msg2 = await bot.wait_for('message', check=check)
            content = msg2.content

            for channel in ctx.guild.text_channels:
                for _ in range(count):
                    try:
                        await channel.send(content)
                    except:
                        pass

        asyncio.run(bot.start(self.token))


class CyberBotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AdemoTool - Discord Raid Tool")
        self.setFixedSize(500, 400)

        # Cyberpunk-style font and color
        self.setStyleSheet("""
            QWidget {
                background-color: #0f0f0f;
                color: #39ff14;
                font-family: Consolas, monospace;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1f1f1f;
                border: 1px solid #39ff14;
                padding: 8px;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #39ff14;
                color: black;
            }
            QLineEdit, QTextEdit {
                background-color: #1a1a1a;
                color: #39ff14;
                border: 1px solid #39ff14;
            }
        """)

        layout = QVBoxLayout()

        self.label = QLabel("Entrez le token du bot :")
        self.token_input = QLineEdit()
        self.token_input.setEchoMode(QLineEdit.Password)

        self.start_button = QPushButton("Lancer le bot")
        self.start_button.clicked.connect(self.launch_bot)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        layout.addWidget(self.label)
        layout.addWidget(self.token_input)
        layout.addWidget(self.start_button)
        layout.addWidget(QLabel("Logs"))
        layout.addWidget(self.log_area)

        self.setLayout(layout)

    def launch_bot(self):
        token = self.token_input.text().strip()
        if not token:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un token.")
            return

        self.thread = BotThread(token)
        self.thread.log_signal.connect(self.log_area.append)
        self.thread.start()
        self.log_area.append("[~] Bot en cours de lancement...")

def main():
    app = QApplication(sys.argv)
    window = CyberBotGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
