import os
import shutil
import tkinter
import tkinter.filedialog
import tkinter.simpledialog

import customtkinter
from PIL import Image

from utils.directory_manager import get_icon_dir, get_storage_dir
from utils.settings import settings
from widgets.Buttons import DefaultButton, FolderObjectButton, FileObjectButton
from widgets.Page import Page
from widgets.Popups import ErrorPopup, SuccessPopup


class CurriculumPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color='white')
        self.MAX_ITEMS_PER_ROW = 5

        self.curriculum_label = customtkinter.CTkLabel(self, text="My Curriculum", font=('Roboto', 36))
        self.curriculum_label.pack(padx=10, pady=(50, 10), side='top', anchor='nw')

        self.top_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.top_buttons_frame.pack(padx=10, pady=(0, 5), side='top', anchor='nw')

        self.home_button = DefaultButton(self.top_buttons_frame, text="Home", image=customtkinter.CTkImage(
            Image.open(f'{get_icon_dir()}{os.sep}home.png')), command=self.go_home)
        self.home_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.open_current_folder = DefaultButton(self.top_buttons_frame, text="Open", image=customtkinter.CTkImage(
            Image.open(f'{get_icon_dir()}{os.sep}link-2.png')), command=lambda: self.open_file(self.current_directory))
        self.open_current_folder.pack(padx=(0, 10), side='left', anchor='nw')

        self.create_folder_button = DefaultButton(self.top_buttons_frame, text="Create Folder",
                                                  command=self.create_folder,
                                                  image=customtkinter.CTkImage(
                                                      Image.open(f'{get_icon_dir()}{os.sep}folder-plus.png')))
        self.create_folder_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.add_folder_button = DefaultButton(self.top_buttons_frame, text="Add Folder", command=self.add_folder,
                                               image=customtkinter.CTkImage(
                                                   Image.open(f'{get_icon_dir()}{os.sep}folder-plus.png')))
        self.add_folder_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.add_file_button = DefaultButton(self.top_buttons_frame, text="Add File", command=self.add_file,
                                             image=customtkinter.CTkImage(
                                                 Image.open(f'{get_icon_dir()}{os.sep}file-plus.png')))
        self.add_file_button.pack(padx=(0, 10), side='left', anchor='nw')

        # self.clear_grid_button = DefaultButton(self.top_buttons_frame, text="Clear", command=self.clear_grid,
        #                                        image=customtkinter.CTkImage(Image.open(f'{get_icon_dir()}'
        #                                                                                f'{os.sep}trash.png')))
        # self.clear_grid_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.set_default_directory_button = DefaultButton(self.top_buttons_frame, text="Make Default",
                                                          image=customtkinter.CTkImage(
                                                              Image.open(f'{get_icon_dir()}{os.sep}bookmark.png')),
                                                          command=self.set_default_dir)
        self.set_default_directory_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.refresh_grid_button = DefaultButton(self.top_buttons_frame, text="Refresh", command=self.refresh_grid,
                                                 image=customtkinter.CTkImage(
                                                     Image.open(f'{get_icon_dir()}{os.sep}rotate-ccw.png')))
        self.refresh_grid_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.back_button = DefaultButton(self.top_buttons_frame, text="Back", command=self.go_back,
                                         image=customtkinter.CTkImage(Image.open(f'{get_icon_dir()}'
                                                                                 f'{os.sep}arrow-left.png')))
        self.back_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.current_directory = settings.get_setting("default_dir", get_storage_dir())
        self.current_directory_var = customtkinter.StringVar(self, value=self.current_directory)
        self.back_stack = []

        self.current_directory_frame = customtkinter.CTkFrame(self)
        self.current_directory_label = customtkinter.CTkLabel(self.current_directory_frame,
                                                              textvariable=self.current_directory_var,
                                                              font=('Roboto', 14))
        self.current_directory_frame.pack(padx=10, anchor='w')
        self.current_directory_label.pack(padx=10, anchor='w')

        self.content_scrollable_frame = customtkinter.CTkScrollableFrame(master=self, fg_color='white')
        self.content_scrollable_frame.pack(fill='both', expand=True, padx=5, pady=0)

        self.refresh_grid()

    def open_file(self, file):
        if os.name == "nt":
            command = f'start "{file}"'
        else:
            command = f'open "{file}"'

        if os.system(command) != 0:
            # An error occurred
            ErrorPopup(self, f"No Application knows how to open this file! -> {file}")

    def open_directory(self, directory):
        self.back_stack.append(self.current_directory)
        self.set_current_dir(directory)
        self.refresh_grid()

    def clear_grid(self):
        for widget in self.content_scrollable_frame.winfo_children():
            widget.destroy()

    def refresh_grid(self):
        self.clear_grid()
        files = os.listdir(self.current_directory)
        row = 0
        column = 0
        for name in files:
            file_path = os.path.join(self.current_directory, name)
            if os.path.isdir(file_path):
                # Creates a folder button
                button = FolderObjectButton(self.content_scrollable_frame, file_path, self.refresh_grid)
                button.bind("<Double-Button-1>", command=lambda event, path=file_path: self.open_directory(path))
                button.grid(row=row, column=column, padx=(0, 10), pady=10, sticky="nsew")
            else:
                # Creates a file object button
                file = FileObjectButton(self.content_scrollable_frame, file_path, self.refresh_grid)
                file.bind("<Double-Button-1>", command=lambda event, path=file_path: self.open_file(path))
                file.grid(row=row, column=column, padx=(0, 10), pady=10, sticky="nsew")

            column += 1
            if column == self.MAX_ITEMS_PER_ROW:
                row += 1
                column = 0

        # Update back button state
        if len(self.back_stack) == 0:
            self.back_button.configure(state=customtkinter.DISABLED)
        else:
            self.back_button.configure(state=customtkinter.NORMAL)

    def go_back(self):
        if self.back_stack:
            self.set_current_dir(directory=self.back_stack.pop())
            self.refresh_grid()

    def create_folder(self):
        new_folder_name = tkinter.simpledialog.askstring("New Folder", "Folder Name:")
        if new_folder_name:
            try:
                os.mkdir(os.path.join(self.current_directory, new_folder_name))
                self.refresh_grid()
            except OSError as error:
                ErrorPopup(self, error)

    def add_folder(self):
        folder_to_copy = tkinter.filedialog.askdirectory()
        if folder_to_copy:
            template_folder_path = os.path.join(os.getcwd(), folder_to_copy)
            if not os.path.exists(template_folder_path):
                ErrorPopup(self, "Template folder not found!")
                return

            new_folder_name = tkinter.simpledialog.askstring("Add Folder", "Enter folder name:",
                                                             initialvalue=folder_to_copy.split(os.sep)[-1])
            if new_folder_name:
                new_folder_path = os.path.join(self.current_directory, new_folder_name)
                try:
                    shutil.copytree(template_folder_path, new_folder_path)
                    self.refresh_grid()
                except Exception as error:
                    ErrorPopup(self, f"Error copying folder: {error}")

    def add_file(self):
        file_to_copy = tkinter.filedialog.askopenfilenames()
        if file_to_copy:
            for file in file_to_copy:
                shutil.copy(file, self.current_directory)
                self.refresh_grid()

    def set_default_dir(self):
        settings.add_setting("default_dir", self.current_directory)
        SuccessPopup(self, f"Success! '{self.current_directory}' is now the default!")

    def go_home(self):
        self.set_current_dir(directory=get_storage_dir())
        self.refresh_grid()

    def set_current_dir(self, directory):
        self.current_directory = directory
        self.current_directory_var.set(directory)
