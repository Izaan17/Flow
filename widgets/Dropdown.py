from typing import Any

import customtkinter


class DefaultDropDown(customtkinter.CTkOptionMenu):
    def __init__(self, master: Any, label_text, **kwargs):
        self.frame = customtkinter.CTkFrame(master, fg_color='transparent')
        super().__init__(self.frame, **kwargs)
        self.drop_down_label = customtkinter.CTkLabel(self.frame, text=label_text)
        # Put frame on left side
        self.frame.pack(anchor='w', pady=10)
        self.drop_down_label.pack(side='left', padx=10)
