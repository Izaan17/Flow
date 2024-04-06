from typing import Any

import customtkinter


class DefaultDropDown(customtkinter.CTkOptionMenu):
    def __init__(self, master: Any, label_text, **kwargs):
        self.frame = customtkinter.CTkFrame(master, fg_color='transparent')
        super().__init__(self.frame, **kwargs)
        self.drop_down_label = customtkinter.CTkLabel(self.frame, text=label_text, font=('Roboto', 14))
        # Put frame on left side
        self.frame.pack(anchor='w', pady=(0, 10), padx=5)
        self.drop_down_label.pack(side='top', pady=5)
