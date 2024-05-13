import os.path
import shutil
import threading
import tkinter
import tkinter.simpledialog
from typing import Any

import customtkinter
from PIL import Image

from tkinter import messagebox
from utils import settings
from utils.directory_manager import get_icon_dir
from widgets.Popups import ErrorPopup

FOLDER_ICON = customtkinter.CTkImage(Image.open(f'{get_icon_dir()}{os.sep}folder.png'), size=(32, 32))


def shorten_text(text, max_length):
    if len(text) <= max_length:
        return text
    else:
        return text[:max_length - 3] + "..."  # truncate text and add ellipsis


class DefaultButton(customtkinter.CTkButton):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs, corner_radius=5, fg_color='#34495e', text_color='white',
                         hover_color='#596275', width=90, font=('Roboto', 12), compound='top')


class PathObjectButton(customtkinter.CTkButton):
    def __init__(self, master: Any, path, refresh_grid_func, **kwargs):
        super().__init__(master, **kwargs,
                         image=customtkinter.CTkImage(light_image=Image.open(f"{get_icon_dir()}{os.sep}file.png"),
                                                      size=(32, 32)), fg_color='#A9A9A9', hover_color='#D3D3D3',
                         text_color='black', compound='top',
                         corner_radius=5)
        self.path = path
        self.item_name = path.split(os.sep)[-1]

        def delete():
            if messagebox.askyesno("Delete", f"Are you sure you want to delete '{self.item_name}'?"):
                try:
                    if not os.path.exists(path):
                        raise FileNotFoundError(f"{path} does not exist!")

                    if os.path.isdir(path):
                        # Check settings
                        if settings.settings.get_setting("allow_full_dir_deletion", "False") == "True":
                            shutil.rmtree(path)
                        else:
                            os.rmdir(path)
                    else:
                        os.remove(path)

                    # If no exceptions were raised, destroy the widget
                    refresh_grid_func()

                except FileNotFoundError as e:
                    ErrorPopup(master, str(e))

                except OSError as e:
                    ErrorPopup(master, f"{e}")

                except Exception as e:
                    ErrorPopup(master, f"An error occurred: {e}")

        def rename():
            new_renamed_file_name = tkinter.simpledialog.askstring("File Rename", "Enter new file name",
                                                                   initialvalue=self.item_name)
            old_path_split = self.path.split(os.sep)
            # Delete last file name
            del old_path_split[-1]
            current_dir = os.sep.join(old_path_split)
            if new_renamed_file_name:
                new_file_name = os.path.join(current_dir, new_renamed_file_name)
                if os.path.exists(new_file_name):
                    ErrorPopup(master, "File already exists")
                try:
                    shutil.move(self.path, new_file_name)
                    refresh_grid_func()
                except Exception as error:
                    ErrorPopup(master, f"Error renaming file: {error}")

        # Right Click menu
        right_click_menu = tkinter.Menu()
        right_click_menu.add_command(label="Copy Path", command=lambda: self.clipboard_append(self.path))
        right_click_menu.add_command(label="Rename", command=rename)
        right_click_menu.add_command(label="Delete", command=delete)

        def action_menu(event):
            right_click_menu.tk_popup(event.x_root, event.y_root)

        self.bind("<Button-2>", action_menu)
        # Text name
        self.configure(text=shorten_text(self.item_name, int(settings.settings.get_setting("max_text_length", 30))))


class FolderObjectButton(PathObjectButton):
    def __init__(self, master: Any, path, refresh_grid_func, **kwargs):
        super().__init__(master, path, refresh_grid_func, **kwargs)
        # change to folder icon
        self.configure(image=FOLDER_ICON)


class FileObjectButton(PathObjectButton):
    def __init__(self, master: Any, path, refresh_grid_func, **kwargs):
        super().__init__(master, path, refresh_grid_func, **kwargs)
        picture_formats = (".png", ".jpg", ".jpeg")
        is_picture = path.endswith(picture_formats)
        if is_picture and settings.settings.get_setting("show_img_preview", "False") == "True":
            threading.Thread(target=self.load_image_preview, args=(path,), daemon=True).start()

    @staticmethod
    def load_image(path, size):
        try:
            image = Image.open(path)
            image.thumbnail(size, reducing_gap=1.0)
            return customtkinter.CTkImage(image, size=size)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def load_image_preview(self, path):
        preview_image = self.load_image(path, (int(settings.settings.get_setting("icon_height", 50)),
                                               int(settings.settings.get_setting("icon_width", 50))))
        if preview_image:
            try:
                self.configure(image=preview_image)
            except Exception:
                pass
