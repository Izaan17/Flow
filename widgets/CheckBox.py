import tkinter
from typing import Any

import customtkinter

from widgets.HyperLink import HyperLink


class TaskCheckBox(customtkinter.CTkCheckBox):
    def __init__(self, master: Any, source, link, **kwargs):
        self.task_item_frame = customtkinter.CTkFrame(master, fg_color='transparent')
        self.task_info_frame = customtkinter.CTkFrame(self.task_item_frame, fg_color='transparent')
        super().__init__(self.task_item_frame, fg_color='#00BF62', hover_color='grey', border_color='light grey',
                         border_width=2, corner_radius=3, font=('Roboto', 15, 'bold'), **kwargs)

        self.source_text_var = customtkinter.StringVar(self.task_item_frame, value=source)
        self.link_text_var = customtkinter.StringVar(self.task_item_frame, value=link)

        self.source_label = customtkinter.CTkLabel(self.task_info_frame, text=f"Source: {self.source_text_var.get()}")
        self.source_label.pack(side='left', padx=(30, 10))

        self.link_hyperlink = HyperLink(self.task_info_frame, text=f"Link: {self.link_text_var.get()}", url=link)
        self.link_hyperlink.pack(side='right', padx=10)

        self.task_item_frame.pack(anchor='w')
        self.task_info_frame.pack(side='bottom', anchor='w')

        def delete():
            self.task_item_frame.destroy()

        # Right Click menu
        right_click_menu = tkinter.Menu()
        right_click_menu.add_command(label="Delete", command=delete)

        def action_menu(event):
            right_click_menu.tk_popup(event.x_root, event.y_root)

        self.bind("<Button-2>", action_menu)
