mytitle = 'Ademo Cloner - Developed by @Ademo.x'

from os import system
system('title ' + mytitle)

import psutil
from pypresence import Presence
import time
import sys
import discord
import asyncio
import colorama
from colorama import Fore, init, Style
import platform
import os
import webbrowser
import requests

# Intents Discord requis
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True

client = discord.Client(intents=intents)
cls = lambda: os.system('cls')
cls()

# Classe Clone vide à personnaliser
class Clone:
    @staticmethod
    async def guild_edit(guild_to, guild_from):
        pass

    @staticmethod
    async def roles_delete(guild):
        pass

    @staticmethod
    async def channels_delete(guild):
        pass

    @staticmethod
    async def roles_create(guild_to, guild_from):
        pass

    @staticmethod
    async def categories_create(guild_to, guild_from):
        pass

    @staticmethod
    async def channels_create(guild_to, guild_from):
        pass

def mainanswer():
    cls()
    logo = print(f"""{Fore.RED}
   _____       .___                      _________ .__                              
  /  _  \    __| _/____   _____   ____   \_   ___ \|  |   ____   ____   ___________ 
 /  /_\  \  / __ |/ __ \ /     \ /  _ \  /    \  \/|  |  /  _ \ /    \_/ __ \_  __ \\
/    |    \/ /_/ \  ___/|  Y Y  (  <_> ) \     \___|  |_(  <_> )   |  \  ___/|  | \/
/____|__  /\____ |\___  >__|_|  /\____/   \______  /____/\____/|___|  /\___  >__|   
        \/      \/    \/      \/                 \/                 \/     \/       
{Fore.MAGENTA}Developed by: @ademo.x{Style.RESET_ALL}
""")

    print('\n')
    print('[1] > Clone Server')
    print('[2] > Join Ademo Discord')
    print('[3] > Github Link')
    print('\n')
    answer = input('\x1b[1;00m[\x1b[91m>\x1b[1;00m]\x1b[91m\x1b[00m Choose : ')
    if answer == '1':
        unfriender()
    elif answer == '2':
        ademo_discord()
    elif answer == '3':
        website()
    else:
        print('Incorrect selection, please choose a valid number')
        time.sleep(2)
        mainanswer()

def unfriender():
    print('Loading...')
    cls()
    token = input(f'{Fore.MAGENTA} Your Token > {Style.RESET_ALL}')
    head = {'Authorization': str(token)}
    src = requests.get('https://discordapp.com/api/v6/users/@me', headers=head)
    if src.status_code == 200:
        print(f'{Fore.GREEN}[+] Your Token Is Valid {Style.RESET_ALL}')
    else:
        print(f'{Fore.RED}[-] Your Token Is Invalid {Style.RESET_ALL}')
        time.sleep(2)
        mainanswer()

    guild_s = input('Your Server ID That You Want To Copy > ')
    guild = input('Your Server ID To Copy The Server Into > ')
    input_guild_id = guild_s
    output_guild_id = guild
    cls()

    @client.event
    async def on_ready():
        cls()
        print(f'Logged In as : {client.user}')
        print('Cloning Server...')
        guild_from = client.get_guild(int(input_guild_id))
        guild_to = client.get_guild(int(output_guild_id))

        if not guild_from or not guild_to:
            print(f"{Fore.RED}One or both guild IDs are invalid or the bot doesn't have access.{Style.RESET_ALL}")
            await client.close()
            return

        await Clone.guild_edit(guild_to, guild_from)
        await Clone.roles_delete(guild_to)
        await Clone.channels_delete(guild_to)
        await Clone.roles_create(guild_to, guild_from)
        await Clone.categories_create(guild_to, guild_from)
        await Clone.channels_create(guild_to, guild_from)

        await asyncio.sleep(5)
        cls()
        mainanswer()

    client.run(token, bot=False)

def ademo_discord():
    webbrowser.open_new('https://discord.gg/Ka537tb6Xg')  # remplace avec ton vrai lien
    cls()
    mainanswer()

def website():
    webbrowser.open_new('https://github.com/Ademoxx/AdemoMultiTool')  # remplace avec ton vrai site
    cls()
    mainanswer()

mainanswer()
