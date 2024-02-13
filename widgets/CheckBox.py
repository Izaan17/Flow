import datetime
import tkinter
from typing import Any

import customtkinter

from widgets.HyperLink import HyperLink


class TaskCheckBox(customtkinter.CTkCheckBox):
    def __init__(self, master: Any, source, link, details_frame: customtkinter.CTkFrame, due_date=None, **kwargs):
        self.task_item_frame = customtkinter.CTkFrame(master, fg_color='transparent')
        self.task_info_frame = customtkinter.CTkFrame(self.task_item_frame, fg_color='transparent')
        super().__init__(self.task_item_frame, fg_color='#00BF62', hover_color='grey', border_color='light grey',
                         border_width=2, corner_radius=3, font=('Roboto', 15, 'bold'), **kwargs)

        self.details_frame = details_frame
        self.due_date = due_date if due_date else datetime.datetime.now().strftime('%m-%d-%Y-%H-%M')
        print(self.due_date)

        self.source_text_var = customtkinter.StringVar(self.task_item_frame, value=source)
        self.link_text_var = customtkinter.StringVar(self.task_item_frame, value=link)

        self.source_label = customtkinter.CTkLabel(self.task_info_frame, text=f"Source: {self.source_text_var.get()}")
        self.source_label.pack(side='left', padx=(30, 10))

        self.link_hyperlink = HyperLink(self.task_info_frame, text=f"Link: {self.link_text_var.get()}", url=link)
        self.link_hyperlink.pack(side='left', padx=10)

        self.difference_from_now = days_between_dates(datetime.datetime.now().strftime('%m-%d-%Y-%H-%M'), self.due_date)

        self.due_date_label = customtkinter.CTkLabel(self.task_info_frame,
                                                     text=f"{parse_days_difference(self.difference_from_now)}")
        self.due_date_label.pack(side='right', padx=10)

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
        self.task_item_frame.bind("<Button-2>", action_menu)
        self.task_info_frame.bind("<Button-2>", action_menu)

        def display_details(event):
            # Clear frame
            for child in self.details_frame.winfo_children():
                child.destroy()

            task_name = customtkinter.CTkLabel(self.details_frame, text=self.cget("text"))
            task_name.pack()

        self.task_item_frame.bind("<Button-1>", display_details)


def days_between_dates(date1_str, date2_str, date_format='%m-%d-%Y-%H-%M'):
    # Convert date strings to datetime objects
    date1 = datetime.datetime.strptime(date1_str, date_format)
    date2 = datetime.datetime.strptime(date2_str, date_format)

    # Calculate the difference in days
    delta = abs(date2 - date1)
    return delta.days


def parse_days_difference(days_difference):
    # Parse the days between
    if days_difference == 0:
        return "Today"
    elif days_difference == 1:
        return "Tomorrow"
    else:
        return f"In {days_difference} days"
