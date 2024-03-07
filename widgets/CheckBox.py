import datetime
import tkinter
from typing import Any

import customtkinter

from widgets.HyperLink import HyperLink


class TaskCheckBox(customtkinter.CTkCheckBox):
    def __init__(self, master: Any, source, link, details_frame: customtkinter.CTkFrame, checkbox_manager,
                 due_date=None, **kwargs):
        self.task_item_frame = customtkinter.CTkFrame(master, fg_color='transparent')
        self.task_info_frame = customtkinter.CTkFrame(self.task_item_frame, fg_color='transparent')
        super().__init__(self.task_item_frame, fg_color='#00BF62', hover_color='grey', border_color='light grey',
                         border_width=2, corner_radius=3, font=('Roboto', 15, 'bold'), **kwargs)

        self.details_frame = details_frame
        self.check_box_manager = checkbox_manager
        self.due_date = due_date if due_date else datetime.datetime.now().strftime('%m-%d-%Y-%H-%M')

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
            self.check_box_manager.remove_checkbox(self)

        # Right Click menu
        right_click_menu = tkinter.Menu()
        right_click_menu.add_command(label="Delete", command=delete)

        def action_menu(event):
            right_click_menu.tk_popup(event.x_root, event.y_root)

        self.master.bind("<Button-2>", action_menu)
        self.task_item_frame.bind("<Button-2>", action_menu)
        self.task_info_frame.bind("<Button-2>", action_menu)

        def display_details(event):
            # Clear details frame
            for child in self.details_frame.winfo_children():
                child.destroy()
            task_header_font = ('Roboto', 12)
            task_header_color = 'grey'
            task_name = customtkinter.CTkLabel(self.details_frame, text=self.cget("text"), font=('Roboto', 26))
            task_name.pack()

            about_label = customtkinter.CTkLabel(self.details_frame, text="About", font=('Roboto bold', 14, 'bold'))
            about_label.pack()

            source_header_label = customtkinter.CTkLabel(self.details_frame, text="Source", font=task_header_font,
                                                         text_color=task_header_color)
            source_header_label.pack(anchor='w')

            source_label = customtkinter.CTkLabel(self.details_frame, text=self.source_text_var.get())
            source_label.pack(anchor='w')

            link_header_label = customtkinter.CTkLabel(self.details_frame, text="Link", font=task_header_font,
                                                       text_color=task_header_color)
            link_header_label.pack(anchor='w')

            link_hyperlink = HyperLink(self.details_frame, url=self.link_text_var.get())
            link_hyperlink.pack(anchor='w')

            due_date_header = customtkinter.CTkLabel(self.details_frame, text="Due Date", font=task_header_font,
                                                     text_color=task_header_color)
            due_date_header.pack(anchor='w')

            task_due_date = customtkinter.CTkLabel(self.details_frame, text=self.due_date)
            task_due_date.pack(anchor='w')

        self.master.bind("<Button-1>", display_details)

        def update_due_date_label():
            difference_from_now = days_between_dates(datetime.datetime.now().strftime('%m-%d-%Y-%H-%M'), self.due_date)
            self.due_date_label.configure(text=parse_days_difference(difference_from_now))
            # Schedule the update after 5 seconds (5000 milliseconds)
            self.after(3000, update_due_date_label)

        update_due_date_label()


def days_between_dates(date1_str, date2_str, date_format='%m-%d-%Y'):
    # Convert date strings to datetime objects
    date1 = datetime.datetime.strptime(date1_str, '%m-%d-%Y-%H-%M')
    date2 = datetime.datetime.strptime(date2_str, '%m-%d-%Y-%H-%M')
    # Convert strings to not include hours
    date1 = date1.strftime('%m-%d-%Y')
    date2 = date2.strftime('%m-%d-%Y')
    # Convert them back into datetime objects
    date1 = datetime.datetime.strptime(date1, date_format)
    date2 = datetime.datetime.strptime(date2, date_format)

    # Calculate the difference in days
    delta = date2 - date1
    return delta.days


def parse_days_difference(days_difference):
    # Parse the days between
    if days_difference == 0:
        return "Today"
    elif days_difference == -1:
        return "Yesterday"
    elif days_difference == 1:
        return "Tomorrow"
    elif 7 >= days_difference > 0:
        return "This week"
    elif days_difference <= 0:
        return f"Due {-days_difference} days ago"
    else:
        return f"In {days_difference} days"
