import customtkinter

from widget_data.notes.note import Note
from widgets.Note import NoteWidget
from widgets.Page import Page


class NotesPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, page_title="My Notes",
                         subheading="All your notes can be stored here.")
        self.note_widgets_scrollable_frame = customtkinter.CTkScrollableFrame(self, fg_color='white')
        self.note_widgets_scrollable_frame.pack(expand=True, fill='both')

        notes = [Note(f"Note {i}", f"Content {i}") for i in range(20)]
        for i, note in enumerate(notes):
            note_widget = NoteWidget(self.note_widgets_scrollable_frame, note)
            note_widget.grid(row=i // 5, column=i % 5, padx=10, pady=10, sticky="nsew")

        # Configure the grid to expand
        for row in range((len(notes) + 2) // 5):  # Adjust the range based on the number of rows
            self.note_widgets_scrollable_frame.grid_rowconfigure(row, weight=1)
        for col in range(5):  # Assuming 3 columns
            self.note_widgets_scrollable_frame.grid_columnconfigure(col, weight=1)

