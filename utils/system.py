import os


# Initialization based on operating systems
if os.name == "nt":
    import ctypes
    right_click_binding_key_code = "<Button-3>"
    file_system_app_name = "Explorer"
    undo_button_sequence = "<Control-z>"
    redo_button_sequence = "<Control-Shift-z>"
    undo_button_name = "Control_L"
    redo_button_name = "Control_R"

else:
    right_click_binding_key_code = "<Button-2>"
    file_system_app_name = "Finder"
    undo_button_sequence = "<Command-z>"
    redo_button_sequence = "<Command-Shift-z>"
    undo_button_name = "Meta_L"
    redo_button_name = "Meta_R"


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
