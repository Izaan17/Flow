import os
import tkinter.simpledialog

import customtkinter

import utils.directory_manager
from widget_data.notes.note import Note
from widget_data.notes.note_manager import NoteManager
from widgets.Note import NoteWidget
from widgets.Page import Page
from widgets.Buttons import NotesFolderObjectButton, DefaultButton


class NotesPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, page_title="My Notes",
                         subheading="All your notes can be stored here.")

        self.notes_manager = NoteManager()

        self.notes_page_frame = customtkinter.CTkFrame(self, fg_color='white')
        self.notes_page_frame.pack(expand=True, fill='both')

        self.notes_left_menu_bar = customtkinter.CTkScrollableFrame(self.notes_page_frame, fg_color='white', width=125)
        self.notes_left_menu_bar.pack(side='left', fill='y')

        self.add_folder_button = DefaultButton(self.notes_left_menu_bar, text="Add Folder", command=self.add_folder)
        self.add_folder_button.pack()

        self.note_widgets_scrollable_frame = customtkinter.CTkScrollableFrame(self.notes_page_frame, fg_color='white')
        self.note_widgets_scrollable_frame.pack(expand=True, fill='both', side='right')

        self.load_notes_folders()

        notes = [Note(f"Note {i}", f"Content {i}") for i in range(20)]
        for i, note in enumerate(notes):
            note_widget = NoteWidget(self.note_widgets_scrollable_frame, note)
            note_widget.grid(row=i // 5, column=i % 5, padx=10, pady=10, sticky="nsew")

        # Configure the grid to expand
        for row in range((len(notes) + 2) // 5):  # Adjust the range based on the number of rows
            self.note_widgets_scrollable_frame.grid_rowconfigure(row, weight=1)
        for col in range(5):  # Assuming 3 columns
            self.note_widgets_scrollable_frame.grid_columnconfigure(col, weight=1)

    def add_folder(self):
        new_folder_name = tkinter.simpledialog.askstring("New Notes Folder", "Notes Folder Name:")
        self.notes_manager.create_notes_folder(new_folder_name)

    def load_notes_folders(self):
        notes_dir = utils.directory_manager.get_notes_dir()
        for folder in os.listdir(notes_dir):
            folder_path = os.path.join(notes_dir, folder)
            if os.path.isdir(folder_path):
                n = NotesFolderObjectButton(self.notes_left_menu_bar, folder_path, text=folder)
                n.pack(pady=5)
                n.action_menu.add_command(label="Create Note",
                                          command=lambda: self.notes_manager.add_note(folder_path, "Test", "Test"))
                # Amount of notes in folder.
                n.configure(text=f"{folder}\t{len(n.get_note_paths())}")
