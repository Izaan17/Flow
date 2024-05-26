import os


# Initialization based on operating systems
if os.name == "nt":
    import ctypes
    right_click_binding_key_code = "<Button-3>"
    file_system_app_name = "Explorer"

elif os.name == "posix":
    right_click_binding_key_code = "<Button-2>"
    file_system_app_name = "Finder"


def open_file_or_folder(file, reveal=False):
    arg = ""
    if reveal:
        arg = '-R'
    command = f'start "" "{file}"' if os.name == "nt" else f'open {arg} "{file}"'
    return os.system(command)


def notify(title, message):
    if os.name == "posix":
        os.system(f"""
                  osascript -e 'display notification "{message}" with title "{title}"'
                  """)
    elif os.name == "nt":
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

