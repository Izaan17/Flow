import os
import tkinter
from tkinter import PhotoImage

import customtkinter
from PIL import Image

from pages.curriculum_page import CurriculumPage
from pages.settings_page import SettingsPage
from pages.tasks_page import TasksPage
from pages.notes_page import NotesPage
from widgets.MenuButton import MenuButton
from utils.directory_manager import get_icon_dir


class Flow(tkinter.Tk):
    def __init__(self):
        # Set light mode
        super().__init__()
        customtkinter.set_appearance_mode('light')
        customtkinter.set_default_color_theme('blue')

        # Initialize main window
        self.wm_title('Flow')
        self.geometry("1300x650")
        self.configure(bg='white')
        self.app_icon = PhotoImage(file=f'{get_icon_dir()}{os.sep}app_icon.png')
        self.wm_iconphoto(False, self.app_icon)

        # Create frames
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.pack(fill='both', expand=True)

        self.left_menu_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color='#2B3950', width=150,
                                                      corner_radius=0)
        self.left_menu_frame.pack(side='left', fill='both')

        self.content_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color='blue', corner_radius=0)
        self.content_frame.pack(side='right', fill='both', expand=True)

        # Initialize pages
        self.tasks_page = TasksPage(self.content_frame)
        self.curriculum_page = CurriculumPage(self.content_frame)
        self.settings_page = SettingsPage(self.content_frame)
        self.notes_page = NotesPage(self.content_frame)

        # Place all pages in the same area
        for page in (self.tasks_page, self.curriculum_page, self.settings_page, self.notes_page):
            page.place(in_=self.content_frame, x=0, y=0, relwidth=1, relheight=1)

        # Load icons
        self.default_icon_size = (22, 22)
        self.icon_dir = f'{get_icon_dir()}{os.sep}'
        self.check_mark_box_icon = customtkinter.CTkImage(light_image=Image.open(f'{self.icon_dir}check-square.png'),
                                                          size=self.default_icon_size)
        self.book_icon = customtkinter.CTkImage(light_image=Image.open(f'{self.icon_dir}file-text.png'),
                                                size=self.default_icon_size)
        self.settings_icon = customtkinter.CTkImage(light_image=Image.open(f'{self.icon_dir}settings.png'),
                                                    size=self.default_icon_size)
        self.notes_icon = customtkinter.CTkImage(light_image=Image.open(f'{self.icon_dir}edit.png'),
                                                 size=self.default_icon_size)

        # Button padding
        self.button_padx = (5, 5)
        self.button_pady = (0, 10)

        # Create menu buttons
        self.tasks_button = MenuButton(self.left_menu_frame, self.check_mark_box_icon, "Tasks",
                                       command=self.tasks_page.show)
        self.tasks_button.grid(padx=self.button_padx, pady=(10, self.button_pady[1]), sticky='nsew')

        self.curriculum_button = MenuButton(self.left_menu_frame, self.book_icon, "Curriculum",
                                            command=self.curriculum_page.show)
        self.curriculum_button.grid(padx=self.button_padx, pady=self.button_pady, sticky='nsew')

        self.notes_button = MenuButton(self.left_menu_frame, self.notes_icon, "Notes",
                                       command=self.notes_page.show)
        self.notes_button.grid(padx=self.button_padx, pady=self.button_pady, sticky='nsew')

        self.settings_button = MenuButton(self.left_menu_frame, self.settings_icon, "Settings",
                                          command=self.settings_page.show)
        self.settings_button.grid(padx=self.button_padx, pady=self.button_pady, sticky='nsew')

        # Show the initial page
        self.tasks_page.show()

        # At exit save all checkbox states
        self.wm_protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.tasks_page.check_box_manager.save_to_file()
        self.destroy()


if __name__ == '__main__':
    app = Flow()
    app.mainloop()
