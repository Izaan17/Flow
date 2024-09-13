import os
from tkinter import PhotoImage

import customtkinter

import utils.directory_manager
from pages.curriculum_page import CurriculumPage
from pages.notes_page import NotesPage
from pages.settings_page import SettingsPage
from pages.tasks_page import TasksPage
from pages.utilities_page import UtilitiesPage
from utils.icon import load_icon
from widgets.menu_button import MenuButton


class Flow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Set light mode
        customtkinter.set_appearance_mode('light')
        customtkinter.set_default_color_theme('blue')

        # Initialize window
        self.wm_title('Flow')
        self.geometry("1300x650")
        self.configure(fg_color='white')
        self.app_icon = PhotoImage(file=f'{utils.directory_manager.get_icon_dir()}{os.sep}app_icon.png')
        self.wm_iconphoto(False, self.app_icon)

        # Create frames
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.pack(fill='both', expand=True)

        self.left_menu_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color='#2B3950', width=150,
                                                      corner_radius=0)
        self.left_menu_frame.pack(side='left', fill='both')

        self.content_frame = customtkinter.CTkFrame(master=self.main_frame, corner_radius=0)
        self.content_frame.pack(side='right', fill='both', expand=True)

        # Initialize pages
        self.tasks_page = TasksPage(self.content_frame)
        self.curriculum_page = CurriculumPage(self.content_frame)
        self.settings_page = SettingsPage(self.content_frame)
        self.notes_page = NotesPage(self.content_frame)
        self.utilities_page = UtilitiesPage(self.content_frame)

        # Place all pages in the same area
        for page in (self.tasks_page, self.curriculum_page, self.settings_page, self.notes_page, self.utilities_page):
            page.place(in_=self.content_frame, x=0, y=0, relwidth=1, relheight=1)

        # Load icons
        self.check_mark_box_icon = load_icon("check-square.png")

        self.book_icon = load_icon("file-text.png")

        self.settings_icon = load_icon("settings.png")

        self.notes_icon = load_icon("edit.png")

        self.utilities_icon = load_icon("tool.png")

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

        self.utilities_button = MenuButton(self.left_menu_frame, self.utilities_icon, "Utilities",
                                           command=self.utilities_page.show)
        self.utilities_button.grid(padx=self.button_padx, pady=self.button_pady, sticky='nsew')

        self.settings_button = MenuButton(self.left_menu_frame, self.settings_icon, "Settings",
                                          command=self.settings_page.show)
        self.settings_button.grid(padx=self.button_padx, pady=self.button_pady, sticky='nsew')

        # Show the initial page
        self.tasks_page.show()

if __name__ == '__main__':
    app = Flow()
    app.mainloop()
