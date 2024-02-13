import os.path
import tkinter
from typing import Any

import customtkinter
from PIL import Image

import settings
from directory_manager import get_icon_dir
from widgets.ErrorPopup import ErrorPopup


class DefaultButton(customtkinter.CTkButton):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs, corner_radius=5, fg_color='#34495e', text_color='white',
                         hover_color='#596275', width=90, font=('Roboto', 12), compound='top')


class PathObjectButton(customtkinter.CTkButton):
    def __init__(self, master: Any, path, **kwargs):
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
                self.destroy()

            except FileNotFoundError as e:
                ErrorPopup(master, str(e))

            except OSError as e:
                ErrorPopup(master, f"{e}")

            except Exception as e:
                ErrorPopup(master, f"An error occurred: {e}")

        # Right Click menu
        right_click_menu = tkinter.Menu()
        right_click_menu.add_command(label="Delete", command=delete)

        def action_menu(event):
            right_click_menu.tk_popup(event.x_root, event.y_root)

        self.bind("<Button-2>", action_menu)
        self.configure(text=self.item_name)


class FolderObjectButton(PathObjectButton):
    def __init__(self, master: Any, path, **kwargs):
        super().__init__(master, path, **kwargs)
        # change to folder icon
        self.configure(image=customtkinter.CTkImage(Image.open(f'{get_icon_dir()}/folder.png'), size=(32, 32)))


class FileObjectButton(PathObjectButton):
    def __init__(self, master: Any, path, **kwargs):
        super().__init__(master, path, **kwargs)
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
