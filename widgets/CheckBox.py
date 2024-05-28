import datetime
from typing import Any

import customtkinter

from utils.date import days_between_dates, parse_days_difference, get_time_suffix_string
from widget_data.CheckBoxData import CheckBoxData
from widgets.HyperLink import HyperLink
from utils.string_utils import shorten_text
from utils.system import notify


class TaskCheckBox(customtkinter.CTkCheckBox):
    def __init__(self, master: Any, task_id, source, link,
                 due_date=None, **kwargs):
        self.task_id = task_id
        self.task_item_frame = customtkinter.CTkFrame(master, fg_color='transparent')
        self.task_info_frame = customtkinter.CTkFrame(self.task_item_frame, fg_color='transparent')
        super().__init__(self.task_item_frame, fg_color='#00BF62', hover_color='grey', border_color='light grey',
                         border_width=3, corner_radius=4, font=('Inter', 16, 'bold'), **kwargs)

        self.due_date = due_date if due_date else datetime.datetime.now().strftime('%m-%d-%Y-%H-%M')
        self.notification_shown = False
        self.source_text_var = customtkinter.StringVar(self.task_item_frame, value=source)
        self.link_text_var = customtkinter.StringVar(self.task_item_frame, value=link)

        self.source_label = customtkinter.CTkLabel(self.task_info_frame, text=f"{self.source_text_var.get()}",
                                                   text_color='grey')
        self.source_label.pack(side='left', padx=(35, 10))

        self.link_hyperlink = HyperLink(self.task_info_frame,
                                        text=f"{shorten_text(self.link_text_var.get(), 30)}", url=link)
        self.link_hyperlink.pack(side='left', padx=10)

        self.difference_from_now = days_between_dates(datetime.datetime.now().strftime('%m-%d-%Y-%H-%M'), self.due_date)

        self.due_date_label = customtkinter.CTkLabel(self.task_info_frame)
        self.due_date_label.pack(side='right', padx=(10, 35))

        self.task_item_frame.pack(anchor='w', expand=True, fill='both', pady=4)
        self.task_info_frame.pack(side='bottom', anchor='w', expand=True, fill='both')

        def update_due_date_label():
            difference_from_now = days_between_dates(datetime.datetime.now().strftime('%m-%d-%Y-%H-%M'), self.due_date)
            text_color = 'black'
            # Already due
            if difference_from_now < 0:
                text_color = 'red'
            # Tomorrow
            elif difference_from_now <= 3 and difference_from_now != 0:
                text_color = 'orange'
            # Today
            elif difference_from_now == 0:
                text_color = 'blue'
            self.due_date_label.configure(text=f"{parse_days_difference(difference_from_now)}, "
                                               f"{get_time_suffix_string(self.due_date)}", text_color=text_color)
            self.check_due_date()
            # Schedule the update after 3 seconds (3000 milliseconds)
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

    def get_root_label(self):
        return self._text_label

    def check_due_date(self):
        if self.notification_shown:
            return

        due_date_obj = datetime.datetime.strptime(self.due_date, '%m-%d-%Y-%H-%M')
        current_date = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M')
        current_date = datetime.datetime.strptime(current_date, '%m-%d-%Y-%H-%M')
        time_difference = (due_date_obj - current_date).total_seconds() / 60  # Difference in minutes
        if 0 <= time_difference < 1:
            notification_title = f"{self.get_task_name()}"
            notification_message = (f"Due Date: {due_date_obj.strftime('%m-%d-%Y %H:%M')}\n"
                                    f"Source: {self.get_task_source()}\nLink: {self.get_task_link()}")
            notify(title=notification_title, message=notification_message)
            self.notification_shown = True
