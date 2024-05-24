import os


def get_file_system_app_name():
    return "Explorer" if os.name == "nt" else "Finder"


def open_file(file):
    command = f'start "" "{file}"' if os.name == "nt" else f'open "{file}"'
    return os.system(command)
