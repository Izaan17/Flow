import datetime
from typing import Any

import customtkinter

from widget_data.CheckBoxData import CheckBoxData
from widgets.HyperLink import HyperLink


class TaskCheckBox(customtkinter.CTkCheckBox):
    def __init__(self, master: Any, task_id, source, link,
                 due_date=None, **kwargs):
        self.task_id = task_id
        self.task_item_frame = customtkinter.CTkFrame(master, fg_color='transparent')
        self.task_info_frame = customtkinter.CTkFrame(self.task_item_frame, fg_color='transparent')
        super().__init__(self.task_item_frame, fg_color='#00BF62', hover_color='grey', border_color='light grey',
                         border_width=2, corner_radius=3, font=('Roboto', 15, 'bold'), **kwargs)

        self.due_date = due_date if due_date else datetime.datetime.now().strftime('%m-%d-%Y-%H-%M')

        self.source_text_var = customtkinter.StringVar(self.task_item_frame, value=source)
        self.link_text_var = customtkinter.StringVar(self.task_item_frame, value=link)

        self.source_label = customtkinter.CTkLabel(self.task_info_frame, text=f"Source: {self.source_text_var.get()}")
        self.source_label.pack(side='left', padx=(30, 10))

        self.link_hyperlink = HyperLink(self.task_info_frame, text=f"Link: {self.link_text_var.get()}", url=link)
        self.link_hyperlink.pack(side='left', padx=10)

        self.difference_from_now = days_between_dates(datetime.datetime.now().strftime('%m-%d-%Y-%H-%M'), self.due_date)

        self.due_date_label = customtkinter.CTkLabel(self.task_info_frame)
        self.due_date_label.pack(side='right', padx=10)

        self.task_item_frame.pack(anchor='w')
        self.task_info_frame.pack(side='bottom', anchor='w')

        def update_due_date_label():
            difference_from_now = days_between_dates(datetime.datetime.now().strftime('%m-%d-%Y-%H-%M'), self.due_date)
            text_color = 'black'
            # Already due
            if difference_from_now < 0:
                text_color = 'red'
            # Tomorrow
            elif difference_from_now <= 3:
                text_color = 'orange'
            # Today
            elif difference_from_now == 0:
                text_color = 'blue'
            self.due_date_label.configure(text=f"{parse_days_difference(difference_from_now)}, "
                                               f"{get_time_suffix(self.due_date)}",
                                          text_color=text_color)
            # Schedule the update after 5 seconds (5000 milliseconds)
            self.after(3000, update_due_date_label)

        update_due_date_label()

    def get_task_name(self):
        return self._text

    def get_task_source(self):
        return self.source_text_var.get()

    def get_task_link(self):
        return self.link_text_var.get()

    def get_task_due_date(self):
        return self.due_date

    def get_task_id(self):
        return self.task_id

    def get_checkbox_data(self):
        return CheckBoxData(self.task_id, self.cget("text"), self.source_text_var.get(), self.link_text_var.get(),
                            self.due_date, self.get())


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
    elif days_difference <= 0:
        return f"Due {-days_difference} days ago"
    else:
        return f"Due in {days_difference} days"


def convert_str_to_datetime(date_str):
    return datetime.datetime.strptime(date_str, '%m-%d-%Y-%H-%M')


def get_day_of_week_string(date_str):
    return convert_str_to_datetime(date_str).strftime("%a")


def get_day(date_str):
    return convert_str_to_datetime(date_str).day


def get_month_abbreviation(date_str):
    return convert_str_to_datetime(date_str).strftime("%b")


def get_time_suffix(date_str):
    return convert_str_to_datetime(date_str).strftime("%I:%M %p")
