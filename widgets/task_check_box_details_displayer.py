from typing import Any

import customtkinter
import utils
from widgets.hyper_link import HyperLink
from widgets.task_check_box import TaskCheckBox


class TaskCheckBoxDetailsDisplayer:
    def __init__(self, master: Any, details_frame: customtkinter.CTkFrame):
        self.master = master
        self.details_frame = details_frame
        self.active_task_check_box: TaskCheckBox | None = None
        self.master.bind_all('<Double Button-1>', self.display_details)

    def display_details(self, event):
        header_font = ('Roboto', 12)
        header_color = 'grey'
        default_wrap_length = 380
        default_justification = 'left'

        # Check if the click was on a TaskCheckBox
        widget = event.widget

        while widget is not self.master and not isinstance(widget, TaskCheckBox) and widget:
            widget = widget.master

        if not isinstance(widget, TaskCheckBox):
            return

        # If the frame is already packed, and it's the same widget, close it
        if self.details_frame.winfo_ismapped() and widget == self.active_task_check_box:
            self.details_frame.pack_forget()
            self.active_task_check_box = None
            return

        # If it's a different widget or the frame is not packed, display the details
        self.active_task_check_box = widget
        self.details_frame.pack(side='right', fill='both', expand=True)

        self.clear_info_frame()

        task_name_label = customtkinter.CTkLabel(self.details_frame,
                                                 text=widget.task.name, font=('Roboto', 26),
                                                 wraplength=default_wrap_length,
                                                 justify=default_justification)
        task_name_label.pack()

        about_label = customtkinter.CTkLabel(self.details_frame, text="About",
                                             font=('Roboto bold', 14, 'bold'),
                                             wraplength=default_wrap_length,
                                             justify=default_justification)
        about_label.pack()

        source_header_label = customtkinter.CTkLabel(self.details_frame, text="Source",
                                                     font=header_font,
                                                     text_color=header_color,
                                                     wraplength=default_wrap_length,
                                                     justify=default_justification)
        source_header_label.pack(anchor='w')

        source_label = customtkinter.CTkLabel(self.details_frame, text=widget.task.source,
                                              wraplength=default_wrap_length,
                                              justify=default_justification)
        source_label.pack(anchor='w')

        link_header_label = customtkinter.CTkLabel(self.details_frame, text="Link", font=header_font,
                                                   text_color=header_color, wraplength=default_wrap_length,
                                                   justify=default_justification)
        link_header_label.pack(anchor='w')

        link_hyperlink = HyperLink(self.details_frame, text=widget.task.link,
                                   url=widget.task.link, wraplength=default_wrap_length,
                                   justify=default_justification)
        link_hyperlink.pack(anchor='w')

        due_date_header = customtkinter.CTkLabel(self.details_frame, text="Due Date", font=header_font,
                                                 text_color=header_color, wraplength=default_wrap_length,
                                                 justify=default_justification)
        due_date_header.pack(anchor='w')

        task_due_date = widget.task.due_date
        task_due_date_label = customtkinter.CTkLabel(
            self.details_frame,
            text=f"{utils.date.get_day_of_week_string(task_due_date)}, "
                 f"{utils.date.get_month_string(task_due_date)} "
                 f"{utils.date.get_day_string(task_due_date)}, "
                 f"{utils.date.get_time_suffix_string(task_due_date)}",
            wraplength=default_wrap_length, justify=default_justification)
        task_due_date_label.pack(anchor='w')

    def clear_info_frame(self):
        # Clear details frame
        for child in self.details_frame.winfo_children():
            child.destroy()