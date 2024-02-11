from typing import Any

import customtkinter


class TaskCheckBox(customtkinter.CTkCheckBox):
    def __init__(self, master: Any, source, **kwargs):
        self.task_item_frame = customtkinter.CTkFrame(master, fg_color='transparent')
        super().__init__(self.task_item_frame, fg_color='green', hover_color='grey', border_color='light grey',
                         border_width=1, corner_radius=3, font=('Roboto', 16, 'bold'), **kwargs)
        self.source_text_var = customtkinter.StringVar(self.task_item_frame, value=source)
        self.source_label = customtkinter.CTkLabel(self.task_item_frame, text=f"Source: {self.source_text_var.get()}")
        self.source_label.pack(side='bottom', anchor='w')
        self.task_item_frame.pack(anchor='w')
