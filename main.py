import customtkinter
from tkinter import PhotoImage

from widgets import MenuButton
from PIL import Image
from pages.pages import TasksPage, CurriculumPage, SettingsPage

# Set light mode
customtkinter.set_appearance_mode('light')
customtkinter.set_default_color_theme('blue')

root = customtkinter.CTk()
root.wm_title('LuminFlow')
root.geometry("1300x650")
root.configure(fg_color='white')
app_icon = PhotoImage(file='icons/hat.png')
root.wm_iconphoto(False, app_icon)


# ===LOAD ICONS===
default_icon_size = (25, 25)
check_mark_box_icon = customtkinter.CTkImage(light_image=Image.open('icons/check-square.png'), size=default_icon_size)
book_icon = customtkinter.CTkImage(light_image=Image.open('icons/book.png'), size=default_icon_size)
settings_icon = customtkinter.CTkImage(light_image=Image.open('icons/settings.png'), size=default_icon_size)

left_menu_frame = customtkinter.CTkFrame(master=root, fg_color='#17325B', width=150, corner_radius=0)
left_menu_frame.pack(side='left', fill='y')

content_frame = customtkinter.CTkFrame(master=root, fg_color='blue', corner_radius=0)
content_frame.pack(fill='both', expand=True)

# All pages
tasks_page = TasksPage(content_frame)
curriculum_page = CurriculumPage(content_frame)
settings_page = SettingsPage(content_frame)

# Place all pages in the same area
tasks_page.place(in_=content_frame, x=0, y=0, relwidth=1, relheight=1)
curriculum_page.place(in_=content_frame, x=0, y=0, relwidth=1, relheight=1)
settings_page.place(in_=content_frame, x=0, y=0, relwidth=1, relheight=1)

# Default padding for buttons
button_padx = (5, 10)
button_pady = (0, 10)
tasks_button = MenuButton.MenuButton(left_menu_frame, check_mark_box_icon, "Tasks", command=tasks_page.show)
tasks_button.grid(padx=button_padx, pady=(10, button_pady[1]), sticky='w')
curriculum_button = MenuButton.MenuButton(left_menu_frame, book_icon, "Education", command=curriculum_page.show)
curriculum_button.grid(padx=button_padx, pady=button_pady, sticky='w')
settings_button = MenuButton.MenuButton(left_menu_frame, settings_icon, "Settings", command=settings_page.show)
settings_button.grid(padx=button_padx, pady=button_pady, sticky='w')

# The first page to be shown is the tasks page
tasks_page.show()

root.mainloop()
