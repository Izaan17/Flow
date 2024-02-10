import os
import shutil
import tkinter.filedialog
import tkinter.simpledialog

import customtkinter

from directory_manager import get_storage_dir, get_icon_dir
from widgets.Buttons import DefaultButton, FolderObjectButton, FileObjectButton
from widgets.CheckBox import TaskCheckBox
from widgets.ErrorPopup import ErrorPopup
from widgets.Page import Page
from PIL import Image, ImageTk


class TasksPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color='white')
        tasks_label = customtkinter.CTkLabel(self, text="My Tasks", font=('Roboto', 36))
        tasks_label.pack(padx=10, pady=(50, 10), side='top', anchor='nw')

        top_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        top_buttons_frame.pack(padx=10, pady=(0, 5), side='top', anchor='nw')

        import_tasks_button = DefaultButton(top_buttons_frame, text="Import Tasks",
                                            image=ImageTk.PhotoImage(Image.open(f'{get_icon_dir()}/download.png')))
        import_tasks_button.pack(padx=(0, 10), side='left', anchor='nw')

        add_task_button = DefaultButton(top_buttons_frame, text="Add Task",
                                        image=ImageTk.PhotoImage(Image.open(f'{get_icon_dir()}/plus-square.png')))
        add_task_button.pack(padx=(0, 10), side='right', anchor='nw')

        tasks_scrollable_frame = customtkinter.CTkScrollableFrame(master=self, fg_color='#2c3e50')
        tasks_scrollable_frame.pack(fill='both', expand=True, padx=(5, 10), pady=(5, 5))

        # check_box = CheckListBox()
        # check_box.pack()

        def add_task_callback():
            print('added task')
            TaskCheckBox(tasks_scrollable_frame, text="Text").pack(fill='both', expand=True, pady=(0, 10))

        add_task_button.configure(command=add_task_callback)


class CurriculumPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color='white')
        self.MAX_ITEMS_PER_ROW = 5

        self.curriculum_label = customtkinter.CTkLabel(self, text="My Curriculum", font=('Roboto', 36))
        self.curriculum_label.pack(padx=10, pady=(50, 10), side='top', anchor='nw')

        self.top_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.top_buttons_frame.pack(padx=10, pady=(0, 5), side='top', anchor='nw')

        self.add_folder_button = DefaultButton(self.top_buttons_frame, text="Add Folder", command=self.add_folder,
                                               image=ImageTk.PhotoImage(Image.open(f'{get_icon_dir()}/folder-plus.png')))
        self.add_folder_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.create_folder_button = DefaultButton(self.top_buttons_frame, text="Create Folder",
                                                  command=self.create_folder,
                                                  image=ImageTk.PhotoImage(Image.open(f'{get_icon_dir()}/folder-plus.png')))
        self.create_folder_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.clear_grid_button = DefaultButton(self.top_buttons_frame, text="Clear", command=self.clear_grid,
                                               image=ImageTk.PhotoImage(Image.open(f'{get_icon_dir()}/trash.png')))
        self.clear_grid_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.refresh_grid_button = DefaultButton(self.top_buttons_frame, text="Refresh", command=self.refresh_grid,
                                                 image=ImageTk.PhotoImage(Image.open(f'{get_icon_dir()}/rotate-ccw.png')))
        self.refresh_grid_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.back_button = DefaultButton(self.top_buttons_frame, text="Back", command=self.go_back,
                                         image=ImageTk.PhotoImage(Image.open(f'{get_icon_dir()}/arrow-left.png')))
        self.back_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.content_scrollable_frame = customtkinter.CTkScrollableFrame(master=self, fg_color='#2c3e50')
        self.content_scrollable_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.current_directory = get_storage_dir()
        self.back_stack = []

        self.refresh_grid()

    @staticmethod
    def open_file(file):
        os.system(f'open "" "{file}"')

    def open_directory(self, directory):
        self.back_stack.append(self.current_directory)
        self.current_directory = directory
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
                button = FolderObjectButton(self.content_scrollable_frame, file_path)
                button.bind("<Double-Button-1>", command=lambda event, path=file_path: self.open_directory(path))
                button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
            else:
                file = FileObjectButton(self.content_scrollable_frame, file_path)
                file.bind("<Double-Button-1>", command=lambda event, path=file_path: self.open_file(path))
                file.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

            column += 1
            if column == self.MAX_ITEMS_PER_ROW:
                row += 1
                column = 0

        # Update back button state
        if len(self.back_stack) == 0:
            self.back_button.configure(state=tkinter.DISABLED)
        else:
            self.back_button.configure(state=tkinter.NORMAL)

    def go_back(self):
        if self.back_stack:
            self.current_directory = self.back_stack.pop()
            self.refresh_grid()

    def create_folder(self):
        new_folder_name = tkinter.simpledialog.askstring("New Folder", "Folder Name:")
        if new_folder_name:
            try:
                os.mkdir(os.path.join(self.current_directory, new_folder_name))
                self.refresh_grid()
            except OSError as error:
                ErrorPopup(self.content_scrollable_frame, error)

    def add_folder(self):
        folder_to_copy = tkinter.filedialog.askdirectory()
        if folder_to_copy:
            template_folder_path = os.path.join(os.getcwd(), folder_to_copy)
            if not os.path.exists(template_folder_path):
                ErrorPopup(self.content_scrollable_frame, "Template folder not found!")
                return

            new_folder_name = tkinter.simpledialog.askstring("Add Folder", "Enter folder name:")
            if new_folder_name:
                new_folder_path = os.path.join(self.current_directory, new_folder_name)
                shutil.copytree(template_folder_path, new_folder_path)
                self.refresh_grid()


class SettingsPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color='white')
        settings_label = customtkinter.CTkLabel(self, text="Settings", font=('Roboto', 36))
        settings_label.pack(padx=10, pady=(50, 10), side='top', anchor='nw')
