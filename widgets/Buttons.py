import os.path
import shutil
import tkinter
import tkinter.simpledialog
from typing import Any

import customtkinter
from PIL import Image

import settings
from utils.directory_manager import get_icon_dir
from widgets.Popups import ErrorPopup


class DefaultButton(customtkinter.CTkButton):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs, corner_radius=5, fg_color='#34495e', text_color='white',
                         hover_color='#596275', width=90, font=('Roboto', 12), compound='top')


class PathObjectButton(customtkinter.CTkButton):
    def __init__(self, master: Any, path, refresh_grid_func, **kwargs):
        super().__init__(master, **kwargs,
                         image=customtkinter.CTkImage(light_image=Image.open(f"{get_icon_dir()}/file.png"),
                                                      size=(32, 32)), fg_color='#596275', hover_color='#303952',
                         text_color='white', compound='top',
                         corner_radius=5)
        self.path = path
        self.item_name = path.split(os.sep)[-1]

        def delete():
            try:
                if not os.path.exists(path):
                    raise FileNotFoundError(f"{path} does not exist!")

                if os.path.isdir(path):
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
            new_renamed_file_name = tkinter.simpledialog.askstring("File Rename", "Enter new file name")
            old_path_split = self.path.split(os.sep)
            # Delete last file name
            del old_path_split[-1]
            current_dir = '/'.join(old_path_split)
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
        right_click_menu.add_command(label="Rename", command=rename)
        right_click_menu.add_command(label="Delete", command=delete)

        def action_menu(event):
            right_click_menu.tk_popup(event.x_root, event.y_root)

        self.bind("<Button-2>", action_menu)
        self.configure(text=self.item_name)


class FolderObjectButton(PathObjectButton):
    def __init__(self, master: Any, path, refresh_grid_func, **kwargs):
        super().__init__(master, path, refresh_grid_func, **kwargs)
        # change to folder icon
        self.configure(image=customtkinter.CTkImage(Image.open(f'{get_icon_dir()}/folder.png'), size=(32, 32)))


class FileObjectButton(PathObjectButton):
    def __init__(self, master: Any, path, refresh_grid_func, **kwargs):
        super().__init__(master, path, refresh_grid_func, **kwargs)
        picture_formats = [".png", ".jpg", "jpeg"]
        is_picture = [True for format_ in picture_formats if path.endswith(format_)]
        is_picture = bool(is_picture)
        if is_picture:
            preview_image = self.load_image(path, (int(settings.settings.get_setting("icon_width", 50)),
                                                   int(settings.settings.get_setting("icon_width", 50))))
            if preview_image:
                self.configure(image=preview_image)

    @staticmethod
    def load_image(path, size):
        try:
            image = Image.open(path)
            image.thumbnail(size, reducing_gap=1.0)
            return customtkinter.CTkImage(image, size=size)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
