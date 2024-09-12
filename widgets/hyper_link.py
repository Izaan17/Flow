import webbrowser
from typing import Any

import customtkinter


class HyperLink(customtkinter.CTkLabel):
    def __init__(self, master: Any, url, **kwargs):
        super().__init__(master, text_color='#1E90FF', font=('Roboto', 12, 'underline'), **kwargs)
        self.url = url
        self.bind("<Button-1>", lambda e: self.open_url(url))

    @staticmethod
    def open_url(url):
        if url:
            webbrowser.open_new(url)
