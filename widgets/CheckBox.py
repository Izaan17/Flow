from typing import Any

import customtkinter


class TaskCheckBox(customtkinter.CTkCheckBox):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)
