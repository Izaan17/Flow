import customtkinter

from widgets.Page import Page
from widgets.Buttons import DefaultButton


class NotesPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, page_title="My Notes",
                         subheading="All your notes can be stored here.")

        self.notes_page_frame = customtkinter.CTkFrame(self, fg_color='white')
        self.notes_page_frame.pack(expand=True, fill='both')

        self.notes_left_menu_bar = customtkinter.CTkScrollableFrame(self.notes_page_frame, fg_color='white', width=200)
        self.notes_left_menu_bar.pack(side='left', fill='y')

        self.add_folder_button = DefaultButton(self.notes_left_menu_bar, text="Add Folder", command=None)
        self.add_folder_button.pack()

        self.note_widgets_scrollable_frame = customtkinter.CTkScrollableFrame(self.notes_page_frame, fg_color='white')
        self.note_widgets_scrollable_frame.pack(expand=True, fill='both', side='right')
