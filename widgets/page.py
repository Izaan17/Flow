from typing import Any

import customtkinter


class Page(customtkinter.CTkFrame):
    def __init__(self, master: Any, page_title: str = "Page Title", subheading: str = "Subheading", *args, **kwargs):
        super().__init__(master, **kwargs, corner_radius=0, fg_color='white')

        self.page_title = customtkinter.CTkLabel(self, text=page_title, font=('Roboto', 36, 'bold'))
        self.page_title.pack(padx=10, pady=(50, 0), side='top', anchor='nw')

        self.subheading = customtkinter.CTkLabel(self, text=subheading, font=('Roboto', 18), text_color='#9C9C9E')
        self.subheading.pack(padx=10, pady=(0, 10), anchor='w')

    def show(self):
        self.lift()
