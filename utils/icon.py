import os

import customtkinter
from PIL import Image
import utils.directory_manager


def load_icon(icon_name: str, size: tuple[int, int] = (22, 22)):
    return customtkinter.CTkImage(
        light_image=Image.open(f'{utils.directory_manager.get_icon_dir()}{os.sep}{icon_name}'),
        size=size)
