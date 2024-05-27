from typing import Any

from widgets.Page import Page
import customtkinter


class UtilitiesPage(Page):
    def __init__(self, master: Any, *args, **kwargs):
        super().__init__(master, *args, **kwargs, page_title="Utilities Page", subheading="Useful tools.")

        customtkinter.CTkLabel(self, text="Coming Soon...", font=('Roboto', 48)).pack()
