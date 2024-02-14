import os
import shutil
import tkinter.filedialog
import tkinter.simpledialog

import customtkinter

from settings import settings
from directory_manager import get_storage_dir, get_icon_dir
from widgets.Buttons import DefaultButton, FolderObjectButton, FileObjectButton
from widgets.CheckBox import TaskCheckBox
from widgets.Popups import ErrorPopup, SuccessPopup
from widgets.Page import Page
from widgets.Dropdown import DefaultDropDown
from PIL import Image


class TasksPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color='white')
        tasks_label = customtkinter.CTkLabel(self, text="My Tasks", font=('Roboto', 36))
        tasks_label.pack(padx=10, pady=(50, 10), side='top', anchor='nw')

        top_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        top_buttons_frame.pack(padx=10, pady=(0, 5), side='top', anchor='nw')

        import_tasks_button = DefaultButton(top_buttons_frame, text="Import Tasks",
                                            image=customtkinter.CTkImage(Image.open(f'{get_icon_dir()}/download.png')))
        import_tasks_button.pack(padx=(0, 10), side='left', anchor='nw')

        add_task_button = DefaultButton(top_buttons_frame, text="Add Task",
                                        image=customtkinter.CTkImage(Image.open(f'{get_icon_dir()}/plus-square.png')))
        add_task_button.pack(padx=(0, 10), side='left', anchor='nw')

        clear_all_tasks_button = DefaultButton(top_buttons_frame, text="Clear All",
                                               image=customtkinter.CTkImage(Image.open(f'{get_icon_dir()}/trash.png')))
        clear_all_tasks_button.pack(padx=(0, 10))

        tasks_list_and_info_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        tasks_list_and_info_frame.pack(fill='both', expand=True)

        tasks_scrollable_frame = customtkinter.CTkScrollableFrame(master=tasks_list_and_info_frame,
                                                                  fg_color='transparent')
        tasks_scrollable_frame.pack(fill='both', expand=True, padx=(5, 10), pady=(5, 5), side='left')

        task_info_frame = customtkinter.CTkFrame(tasks_list_and_info_frame, fg_color='white', width=10)
        task_info_frame.pack(side='right', fill='both', expand=True)

        # check_box = CheckListBox()
        # check_box.pack()

        def add_task_callback():
            TaskCheckBox(tasks_scrollable_frame, text="Veniam laborum fugiat nostrud occaecat sint quis ullamco "
                                                      "fugiat", source="MyOpenMath", link="https://youtube.com",
                         details_frame=task_info_frame).pack(
                fill='both', expand=True,
                pady=(0, 10))

        def clear_tasks_callback():
            for child in tasks_scrollable_frame.winfo_children():
                child.destroy()

        add_task_button.configure(command=add_task_callback)
        clear_all_tasks_button.configure(command=clear_tasks_callback)


# Todo: Add current directory label or box.
class CurriculumPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color='white')
        self.MAX_ITEMS_PER_ROW = 5

        self.curriculum_label = customtkinter.CTkLabel(self, text="My Curriculum", font=('Roboto', 36))
        self.curriculum_label.pack(padx=10, pady=(50, 10), side='top', anchor='nw')

        self.top_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.top_buttons_frame.pack(padx=10, pady=(0, 5), side='top', anchor='nw')

        self.home_button = DefaultButton(self.top_buttons_frame, text="Home", image=customtkinter.CTkImage(
            Image.open(f'{get_icon_dir()}/home.png')), command=self.go_home)
        self.home_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.add_folder_button = DefaultButton(self.top_buttons_frame, text="Add Folder", command=self.add_folder,
                                               image=customtkinter.CTkImage(
                                                   Image.open(f'{get_icon_dir()}/folder-plus.png')))
        self.add_folder_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.add_file_button = DefaultButton(self.top_buttons_frame, text="Add File", command=self.add_file,
                                             image=customtkinter.CTkImage(
                                                 Image.open(f'{get_icon_dir()}/folder-plus.png')))
        self.add_file_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.create_folder_button = DefaultButton(self.top_buttons_frame, text="Create Folder",
                                                  command=self.create_folder,
                                                  image=customtkinter.CTkImage(
                                                      Image.open(f'{get_icon_dir()}/folder-plus.png')))
        self.create_folder_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.clear_grid_button = DefaultButton(self.top_buttons_frame, text="Clear", command=self.clear_grid,
                                               image=customtkinter.CTkImage(Image.open(f'{get_icon_dir()}/trash.png')))
        self.clear_grid_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.refresh_grid_button = DefaultButton(self.top_buttons_frame, text="Refresh", command=self.refresh_grid,
                                                 image=customtkinter.CTkImage(
                                                     Image.open(f'{get_icon_dir()}/rotate-ccw.png')))
        self.refresh_grid_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.set_default_directory_button = DefaultButton(self.top_buttons_frame, text="Make Default",
                                                          image=customtkinter.CTkImage(
                                                              Image.open(f'{get_icon_dir()}/bookmark.png')),
                                                          command=self.set_default_dir)
        self.set_default_directory_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.back_button = DefaultButton(self.top_buttons_frame, text="Back", command=self.go_back,
                                         image=customtkinter.CTkImage(Image.open(f'{get_icon_dir()}/arrow-left.png')))
        self.back_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.current_directory = settings.get_setting("default_dir", get_storage_dir())
        self.current_directory_var = customtkinter.StringVar(self, value=self.current_directory)
        self.back_stack = []

        self.current_directory_frame = customtkinter.CTkFrame(self)
        self.current_directory_label = customtkinter.CTkLabel(self.current_directory_frame,
                                                              textvariable=self.current_directory_var,
                                                              font=('Roboto', 14))
        self.current_directory_frame.pack(padx=5, anchor='w')
        self.current_directory_label.pack(padx=10, anchor='w')

        self.content_scrollable_frame = customtkinter.CTkScrollableFrame(master=self, fg_color='#2c3e50')
        self.content_scrollable_frame.pack(fill='both', expand=True, padx=5, pady=5)

        self.refresh_grid()

    @staticmethod
    def open_file(file):
        if os.name == "nt":
            os.system(f'start "" "{file}"')
        else:
            os.system(f'open "" "{file}"')

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
                button = FolderObjectButton(self.content_scrollable_frame, file_path, self.refresh_grid)
                button.bind("<Double-Button-1>", command=lambda event, path=file_path: self.open_directory(path))
                button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
            else:
                file = FileObjectButton(self.content_scrollable_frame, file_path, self.refresh_grid)
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
            self.set_current_dir(directory=self.back_stack.pop())
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

    def add_file(self):
        file_to_copy = tkinter.filedialog.askopenfilenames()
        if file_to_copy:
            for file in file_to_copy:
                shutil.copy(file, self.current_directory)
                self.refresh_grid()

    def set_default_dir(self):
        settings.add_setting("default_dir", self.current_directory)
        SuccessPopup(self.content_scrollable_frame, f"Success! '{self.current_directory}' is now the default!")

    def go_home(self):
        self.set_current_dir(directory=get_storage_dir())
        self.refresh_grid()

    def set_current_dir(self, directory):
        self.current_directory = directory
        self.current_directory_var.set(directory)


class SettingsPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color='white')

        self.all_icon_sizes = ["24x24", "50x50", "100x100", "125x125", "200x200"]

        self.settings_label = customtkinter.CTkLabel(self, text="Settings", font=('Roboto', 36))
        self.settings_label.pack(padx=10, pady=(50, 10), side='top', anchor='nw')

        self.drop_downs_frame = customtkinter.CTkFrame(self, fg_color='white')
        self.drop_downs_frame.pack(fill='both', expand=True)

        self.icon_size_drop_down = DefaultDropDown(self.drop_downs_frame, label_text="Image Preview Size",
                                                   values=self.all_icon_sizes, command=self.on_icon_change)
        self.icon_size_drop_down.pack(anchor='w')
        # Set saved icon size or default
        self.icon_size_drop_down.set(f"{settings.get_setting('icon_width', 50)}x"
                                     f"{settings.get_setting('icon_height', 50)}")

    @staticmethod
    def on_icon_change(choice):
        icon_size = choice.split("x")
        settings.add_setting("icon_width", icon_size[0])
        settings.add_setting("icon_height", icon_size[1])
