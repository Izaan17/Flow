import os


def get_file_system_app_name():
    return "Explorer" if os.name == "nt" else "Finder"


def open_file_or_folder(file, reveal=False):
    arg = ""
    if reveal:
        arg = '-R'
    command = f'start "" "{file}"' if os.name == "nt" else f'open {arg} "{file}"'
    return os.system(command)


def get_button_binding_key():
    return "<Button-3>" if os.name == "nt" else "<Button-2>"
