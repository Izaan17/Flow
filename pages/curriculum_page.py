import os
import shutil
import tkinter
import tkinter.filedialog
import tkinter.simpledialog

import customtkinter
from PIL import Image

import utils.system
from utils.directory_manager import get_icon_dir, get_storage_dir
from utils.settings import settings
from widgets.Buttons import DefaultButton, FolderObjectButton, FileObjectButton
from widgets.Page import Page
from widgets.popups.Popups import ErrorPopup, SuccessPopup


# Todo: Optimize big file copying when adding a folder.
#  2 - Add a way to drag and drop folders both ways from the directory panel.
#  3 - Optimize deleting big folders.

class CurriculumPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color='white')

        # Page title
        self.curriculum_label = customtkinter.CTkLabel(self, text="Curriculum", font=('Roboto', 36, 'bold'))
        self.curriculum_label.pack(padx=10, pady=(50, 10), side='top', anchor='nw')

        self.top_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.top_buttons_frame.pack(padx=10, pady=(0, 5), side='top', anchor='nw')

        self.home_button = DefaultButton(self.top_buttons_frame, text="Home",
                                         image=customtkinter.CTkImage(Image.open(f'{get_icon_dir()}{os.sep}home.png')),
                                         command=self.go_home)
        self.home_button.pack(padx=(0, 10), side='left', anchor='nw')

        # self.open_current_folder = DefaultButton(self.top_buttons_frame, text="Open",
        #                                          image=customtkinter.CTkImage(
        #                                              Image.open(f'{get_icon_dir()}{os.sep}folder.png')),
        #                                          command=lambda: self.open_file(self.current_directory))
        # self.open_current_folder.pack(padx=(0, 10), side='left', anchor='nw')

        self.create_folder_button = DefaultButton(self.top_buttons_frame, text="New Folder",
                                                  command=self.create_folder,
                                                  image=customtkinter.CTkImage(
                                                      Image.open(f'{get_icon_dir()}{os.sep}folder-plus.png')))
        self.create_folder_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.add_folder_button = DefaultButton(self.top_buttons_frame, text="Import Folder", command=self.add_folder,
                                               image=customtkinter.CTkImage(
                                                   Image.open(f'{get_icon_dir()}{os.sep}folder-plus.png')))
        self.add_folder_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.add_file_button = DefaultButton(self.top_buttons_frame, text="Import File", command=self.add_file,
                                             image=customtkinter.CTkImage(
                                                 Image.open(f'{get_icon_dir()}{os.sep}file-plus.png')))
        self.add_file_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.set_default_directory_button = DefaultButton(self.top_buttons_frame, text="Set Default",
                                                          image=customtkinter.CTkImage(
                                                              Image.open(f'{get_icon_dir()}{os.sep}bookmark.png')),
                                                          command=self.set_default_dir)
        self.set_default_directory_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.refresh_grid_button = DefaultButton(self.top_buttons_frame, text="Refresh", command=self.refresh_grid,
                                                 image=customtkinter.CTkImage(
                                                     Image.open(f'{get_icon_dir()}{os.sep}rotate-ccw.png')))
        self.refresh_grid_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.back_button = DefaultButton(self.top_buttons_frame, text="Back", command=self.go_back,
                                         image=customtkinter.CTkImage(
                                             Image.open(f'{get_icon_dir()}{os.sep}arrow-left.png')))
        self.back_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.current_directory = settings.get_setting("default_dir", get_storage_dir())
        self.current_directory_var = customtkinter.StringVar(self, value=self.current_directory)
        self.back_stack = []

        self.current_directory_frame = customtkinter.CTkFrame(self)
        self.current_directory_label = customtkinter.CTkLabel(self.current_directory_frame,
                                                              textvariable=self.current_directory_var,
                                                              font=('Roboto', 14))

        self.current_directory_label.bind("<Button-2>", self.show_directory_menu)
        self.current_directory_menu = tkinter.Menu(self.current_directory_frame)
        self.current_directory_menu.add_command(label="Copy Directory",
                                                command=lambda: self.clipboard_append(self.current_directory))

        self.current_directory_menu.add_separator()
        self.current_directory_menu.add_command(label=f"Open in {utils.system.get_file_system_app_name()}",
                                                command=lambda: self.open_file(self.current_directory))

        self.current_directory_frame.pack(padx=10, anchor='w')
        self.current_directory_label.pack(padx=10, anchor='w')

        self.content_scrollable_frame = customtkinter.CTkScrollableFrame(master=self, fg_color='white',
                                                                         scrollbar_button_color='white')
        self.content_scrollable_frame.pack(fill='both', expand=True, padx=5, pady=3)

        self.refresh_grid()

    def show_directory_menu(self, event):
        try:
            self.current_directory_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.current_directory_menu.grab_release()

    def open_file(self, file):
        if utils.system.open_file(file) != 0:
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
        row, column = 0, 0
        max_items_per_row = int(settings.get_setting("max_items_per_row", 5))

        for name in files:
            file_path = os.path.join(self.current_directory, name)
            if os.path.isdir(file_path):
                button = FolderObjectButton(self.content_scrollable_frame, file_path, self.refresh_grid)
                button.bind("<Double-Button-1>", lambda event, path=file_path: self.open_directory(path))
            else:
                button = FileObjectButton(self.content_scrollable_frame, file_path, self.refresh_grid)
                button.bind("<Double-Button-1>", lambda event, path=file_path: self.open_file(path))

            button.grid(row=row, column=column, padx=(0, 10), pady=10, sticky="nsew")
            column += 1
            if column == max_items_per_row:
                row += 1
                column = 0

        self.back_button.configure(state=customtkinter.NORMAL if self.back_stack else customtkinter.DISABLED)

    def go_back(self):
        if self.back_stack:
            self.set_current_dir(self.back_stack.pop())
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
        folder_to_copy = tkinter.filedialog.askdirectory().replace('/', os.sep)
        if folder_to_copy:
            template_folder_path = os.path.join(os.getcwd(), folder_to_copy)
            if not os.path.exists(template_folder_path):
                ErrorPopup(self, "Template folder not found!")
                return

            new_folder_name = tkinter.simpledialog.askstring("Add Folder", "Enter folder name:",
                                                             initialvalue=os.path.basename(folder_to_copy))
            if new_folder_name:
                new_folder_path = os.path.join(self.current_directory, new_folder_name)
                try:
                    shutil.copytree(template_folder_path, new_folder_path)
                    self.refresh_grid()
                except Exception as error:
                    ErrorPopup(self, f"Error copying folder: {error}")

    def add_file(self):
        files_to_copy = tkinter.filedialog.askopenfilenames()
        for file in files_to_copy:
            shutil.copy(file, self.current_directory)
        self.refresh_grid()

    def set_default_dir(self):
        settings.add_setting("default_dir", self.current_directory)
        SuccessPopup(self, f"Success! '{self.current_directory}' is now the default!")

    def go_home(self):
        self.set_current_dir(get_storage_dir())
        self.refresh_grid()

    def set_current_dir(self, directory):
        self.current_directory = directory
        self.current_directory_var.set(directory)
