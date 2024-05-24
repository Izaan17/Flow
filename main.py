import os
from tkinter import PhotoImage

import customtkinter
from PIL import Image

from pages.curriculum_page import CurriculumPage
from pages.settings_page import SettingsPage
from pages.tasks_page import TasksPage
from widgets.MenuButton import MenuButton
from utils.directory_manager import get_icon_dir

# Set light mode
customtkinter.set_appearance_mode('light')
customtkinter.set_default_color_theme('blue')

# Initialize main window
root = customtkinter.CTk()
root.wm_title('Flow')
root.geometry("1500x650")
root.configure(fg_color='white')
app_icon = PhotoImage(file=f'{get_icon_dir()}{os.sep}app_icon.png')
root.wm_iconphoto(False, app_icon)

# Load icons
default_icon_size = (25, 25)
icon_dir = get_icon_dir()
check_mark_box_icon = customtkinter.CTkImage(light_image=Image.open(f'{icon_dir}{os.sep}check-square.png'),
                                             size=default_icon_size)
book_icon = customtkinter.CTkImage(light_image=Image.open(f'{icon_dir}{os.sep}book.png'), size=default_icon_size)
settings_icon = customtkinter.CTkImage(light_image=Image.open(f'{icon_dir}{os.sep}settings.png'),
                                       size=default_icon_size)

# Create frames
left_menu_frame = customtkinter.CTkFrame(master=root, fg_color='#2B3950', width=150, corner_radius=0)
left_menu_frame.pack(side='left', fill='y')

content_frame = customtkinter.CTkFrame(master=root, fg_color='blue', corner_radius=0)
content_frame.pack(fill='both', expand=True)

# Initialize pages
tasks_page = TasksPage(content_frame)
curriculum_page = CurriculumPage(content_frame)
settings_page = SettingsPage(content_frame)

# Place all pages in the same area
for page in (tasks_page, curriculum_page, settings_page):
    page.place(in_=content_frame, x=0, y=0, relwidth=1, relheight=1)

# Button padding
button_padx = (5, 5)
button_pady = (0, 10)

# Create menu buttons
tasks_button = MenuButton(left_menu_frame, check_mark_box_icon, "Tasks", command=tasks_page.show, button_width=65)
tasks_button.grid(padx=button_padx, pady=(10, button_pady[1]), sticky='nsew')

curriculum_button = MenuButton(left_menu_frame, book_icon, "Education", command=curriculum_page.show, button_width=65)
curriculum_button.grid(padx=button_padx, pady=button_pady, sticky='nsew')

settings_button = MenuButton(left_menu_frame, settings_icon, "Settings", command=settings_page.show, button_width=65)
settings_button.grid(padx=button_padx, pady=button_pady, sticky='nsew')

# Show the initial page
tasks_page.show()

root.mainloop()
