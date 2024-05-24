import os
import shutil
import threading
import tkinter
from tkinter import messagebox
from tkinter.simpledialog import askstring
from typing import Any

import customtkinter
from PIL import Image

import utils.system
from utils import settings
from utils.string import shorten_text
from utils.directory_manager import get_icon_dir
from utils.system import get_file_system_app_name
from widgets.popups.Popups import ErrorPopup

FOLDER_ICON = customtkinter.CTkImage(Image.open(os.path.join(get_icon_dir(), 'folder.png')), size=(32, 32))


class DefaultButton(customtkinter.CTkButton):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs, corner_radius=5, fg_color='#34495e', text_color='white',
                         hover_color='#155A8A', width=90, font=('Roboto', 12), compound='top')


class PathObjectButton(customtkinter.CTkButton):
    def __init__(self, master: Any, path: str, refresh_grid_func, **kwargs):
        super().__init__(master, **kwargs,
                         image=customtkinter.CTkImage(light_image=Image.open(os.path.join(get_icon_dir(), "file.png")),
                                                      size=(32, 32)), fg_color='#D3D3D3', hover_color='#BFBFBF',
                         text_color='black', compound='top', corner_radius=5)
        self.path = path
        self.item_name = os.path.basename(path)
        self.refresh_grid_func = refresh_grid_func
        self.master = master

        self._configure_right_click_menu()
        self._configure_text()

    def _configure_right_click_menu(self):
        right_click_menu = tkinter.Menu()
        right_click_menu.add_command(label="Copy Path", command=lambda: self.clipboard_append(self.path))
        right_click_menu.add_command(label="Rename", command=self._rename)
        right_click_menu.add_command(label="Delete", command=self._delete)
        right_click_menu.add_separator()
        right_click_menu.add_command(label=f"Open in {get_file_system_app_name()}",
                                     command=lambda: utils.system.open_file(self.path))

        self.bind("<Button-2>", lambda event: right_click_menu.tk_popup(event.x_root, event.y_root))

    def _configure_text(self):
        max_text_length = int(settings.settings.get_setting("max_text_length", 30))
        self.configure(text=shorten_text(self.item_name, max_text_length))

    def _delete(self):
        if messagebox.askyesno("Delete", f"Are you sure you want to delete '{self.item_name}'?"):
            try:
                if not os.path.exists(self.path):
                    raise FileNotFoundError(f"{self.path} does not exist!")

                if os.path.isdir(self.path):
                    if settings.settings.get_setting("allow_full_dir_deletion", "False") == "True":
                        shutil.rmtree(self.path)
                    else:
                        os.rmdir(self.path)
                else:
                    os.remove(self.path)

                self.destroy()
            except Exception as e:
                ErrorPopup(self.master, str(e))

    def _rename(self):
        new_item_name = askstring("File Rename", "Enter new file name", initialvalue=self.item_name)
        if new_item_name:
            new_item_path = os.path.join(os.path.dirname(self.path), new_item_name)
            if os.path.exists(new_item_path):
                ErrorPopup(self.master, "File already exists")
                return
            try:
                shutil.move(self.path, new_item_path)
                self.refresh_grid_func()
            except Exception as e:
                ErrorPopup(self.master, f"Error renaming file: {e}")


class FolderObjectButton(PathObjectButton):
    def __init__(self, master: Any, path: str, refresh_grid_func, **kwargs):
        super().__init__(master, path, refresh_grid_func, **kwargs)
        self.configure(image=FOLDER_ICON)


class FileObjectButton(PathObjectButton):
    def __init__(self, master: Any, path: str, refresh_grid_func, **kwargs):
        super().__init__(master, path, refresh_grid_func, **kwargs)
        if path.lower().endswith(('.png', '.jpg', '.jpeg')) and settings.settings.get_setting("show_img_preview",
                                                                                              "False") == "True":
            threading.Thread(target=self._load_image_preview, args=(path,), daemon=True).start()

    @staticmethod
    def _load_image(path: str, size: tuple[int, int]) -> customtkinter.CTkImage | None:
        try:
            image = Image.open(path)
            image.thumbnail(size, reducing_gap=1.0)
            return customtkinter.CTkImage(image, size=size)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def _load_image_preview(self, path: str):
        icon_size = (int(settings.settings.get_setting("icon_height", 50)),
                     int(settings.settings.get_setting("icon_width", 50)))
        preview_image = self._load_image(path, icon_size)
        if preview_image:
            self.configure(image=preview_image)
