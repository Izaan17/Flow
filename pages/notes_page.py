from widgets.Page import Page
import customtkinter


class NotesPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color='white')

        # Page title
        notes_label = customtkinter.CTkLabel(self, text="My Notes", font=('Roboto', 36, 'bold'))
        notes_label.pack(padx=10, pady=(50, 0), side='top', anchor='nw')

        customtkinter.CTkLabel(self, text="Coming Soon...", font=('Roboto', 48)).pack()
