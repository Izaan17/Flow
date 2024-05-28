from typing import Any

import utils.widget_utils
from widget_data.notes.note import Note

import customtkinter


class NoteWidget(customtkinter.CTkFrame):
    def __init__(self, master: Any, note: Note, **kwargs):
        super().__init__(master, **kwargs, width=200, height=200, fg_color='transparent')

        self.propagate(False)

        self.note_frame = customtkinter.CTkFrame(self, width=300, corner_radius=8, border_width=3)
        self.note_frame.configure(border_color=self.note_frame.cget('fg_color'))
        self.note_frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.note_content_preview = customtkinter.CTkLabel(self.note_frame, text=note.content, anchor='nw',
                                                           height=85)
        self.note_content_preview.pack(padx=10, pady=10, fill='both', expand=True)

        self.note_title_label = customtkinter.CTkLabel(self, text=note.title,
                                                       font=('Roboto', 14, 'bold'))
        self.note_title_label.pack(padx=10)

        self.note_date_modified_label = customtkinter.CTkLabel(self,
                                                               text=note.date_modified.strftime("%l:%M %p"),
                                                               font=('Roboto', 9))
        self.note_date_modified_label.pack(padx=10)

        # Highlight bind
        utils.widget_utils.bind_all(self, "<Button-1>", self.highlight)

    def highlight(self, event):
        self.note_frame.configure(border_color='yellow')

    def remove_highlight(self):
        self.note_frame.configure(border_color=self.note_frame.cget('fg_color'))


if __name__ == '__main__':
    # Example usage:
    root = customtkinter.CTk()
    root.geometry("400x300")
    root.title("Note Widget Example")
    cnote = Note("Test Note", "Test Contents")
    n = NoteWidget(root, cnote)
    n.pack(fill='both', expand=True)
    root.mainloop()
