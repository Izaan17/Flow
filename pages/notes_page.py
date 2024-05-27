from widgets.Page import Page
import customtkinter


class NotesPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, page_title="My Notes",
                         subheading="All your notes can be stored here.")

        customtkinter.CTkLabel(self, text="Coming Soon...", font=('Roboto', 48)).pack()
