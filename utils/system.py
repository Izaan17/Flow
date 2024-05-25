import os


def get_file_system_app_name():
    return "Explorer" if os.name == "nt" else "Finder"


def open_file_or_folder(file, reveal=False):
    arg = ""
    if reveal:
        arg = "/select" if os.name == 'nt' else '-R'
    command = f'start "" "{file}" {arg}' if os.name == "nt" else f'open {arg} "{file}"'
    return os.system(command)
