from typing import Any

import customtkinter


class DefaultSwitch(customtkinter.CTkSwitch):
    def __init__(self, master: Any, label_text, **kwargs):
        self.frame = customtkinter.CTkFrame(master, fg_color='transparent')
        super().__init__(self.frame, **kwargs)
        self.configure(fg_color="#155A8A", progress_color="#155A8A", button_color="light gray")
        self.switch_label = customtkinter.CTkLabel(self.frame, text=label_text, font=('Roboto', 14))
        # Put frame on left side
        self.frame.pack(anchor='w', pady=(0, 10), padx=10)
        self.switch_label.pack(side='top', pady=5, anchor='w')
