import datetime
import tkinter.messagebox
from typing import Any

import customtkinter
from tkcalendar import dateentry

import utils
from constants import ALL_TASK_SOURCES
from database.task_manager import TaskManager
from models import Task
from utils.string_utils import isolate_string
from widgets.entry import DefaultEntry
from widgets.popups.PopupForm import PopupForm
from widgets.popups.validation.widget_data_validator import NonEmptyValidator, NumericValidator
from widgets.task_check_box import TaskCheckBox


class TaskContextMenu:
    def __init__(self, master: Any, task_manager: TaskManager):
        self.master = master
        self.task_manager = task_manager
        self.selected_task_check_box: TaskCheckBox | None = None

        # Create the context menu
        self.context_menu = tkinter.Menu(self.master, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_task)
        self.context_menu.add_command(label="Duplicate", command=self.duplicate_task)
        self.context_menu.add_command(label="Delete", command=self.delete_task)

        # Bind the right-click event to the master widget
        self.master.bind_all(utils.system.right_click_binding_key_code, self.show_context_menu)

    def show_context_menu(self, event):
        # Check if the click was on a TaskCheckBox
        widget = event.widget

        while widget is not self.master and not isinstance(widget, TaskCheckBox) and widget:
            widget = widget.master

        if isinstance(widget, TaskCheckBox):
            self.selected_task_check_box = widget
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def edit_task(self):
        if self.selected_task_check_box:
            edit_task_form = PopupForm(self.master, fg_color='white')
            edit_task_form.wm_title("Edit Task")

            task_entries_frame = customtkinter.CTkFrame(edit_task_form)
            task_entries_frame.pack(fill='both', expand=True, padx=10, pady=10)

            task_name_entry = DefaultEntry(task_entries_frame, placeholder_text='Task Name')
            task_name_entry.insert(0, self.selected_task_check_box.task.name)

            task_source_entry = customtkinter.CTkComboBox(task_entries_frame,
                                                          values=ALL_TASK_SOURCES)
            task_source_entry.set(self.selected_task_check_box.task.source)

            task_link_entry = DefaultEntry(task_entries_frame, placeholder_text='Task Link')
            task_link_entry.insert(0, self.selected_task_check_box.task.link if self.selected_task_check_box.task.link else '')

            task_date = self.selected_task_check_box.task.due_date.split("-")
            task_hour = task_date[3]
            task_minute = task_date[4]
            hour_entry = DefaultEntry(task_entries_frame, placeholder_text='Hour')
            hour_entry.insert(0, task_hour)
            minute_entry = DefaultEntry(task_entries_frame, placeholder_text='Minutes')
            minute_entry.insert(0, task_minute)

            due_date_calendar = dateentry.Calendar(task_entries_frame)
            due_date_calendar.pack(padx=10, pady=10)
            due_date_calendar.selection_set(self.selected_task_check_box.task.due_date)

            task_name_entry.pack(padx=20, pady=15)
            task_source_entry.pack(padx=20, pady=10)
            task_link_entry.pack(padx=20, pady=15)
            hour_entry.pack(padx=20, pady=15)
            minute_entry.pack(padx=20, pady=15)

            edit_task_form.add_widget(task_name_entry, [NonEmptyValidator()])
            edit_task_form.add_widget(task_source_entry)
            edit_task_form.add_widget(task_link_entry)
            edit_task_form.add_widget(hour_entry, [NonEmptyValidator(), NumericValidator(1, 23)])
            edit_task_form.add_widget(minute_entry, [NonEmptyValidator(), NumericValidator(0, 60)])

            self.master.wait_window(edit_task_form)

            if edit_task_form.data_ready:
                task_name = edit_task_form.get_data(task_name_entry)
                task_source = edit_task_form.get_data(task_source_entry)
                task_link = edit_task_form.get_data(task_link_entry)
                original_format_string = '%m/%d/%y %H:%M'
                desired_format_string = '%m-%d-%Y-%H-%M'
                parsed_date = datetime.datetime.strptime(
                    f"{due_date_calendar.get_date()} "
                    f"{edit_task_form.get_data(hour_entry)}:"
                    f"{isolate_string('0', edit_task_form.get_data(minute_entry))}",
                    original_format_string)
                formatted_date = parsed_date.strftime(desired_format_string)
                new_edited_task = Task(self.selected_task_check_box.task.id, task_name, task_source, task_link, formatted_date, is_complete=self.selected_task_check_box.task.is_complete)
                new_edited_check_box = TaskCheckBox(self.master, task=new_edited_task)

                self.task_manager.update_task(new_edited_check_box.task)
                self.selected_task_check_box.destroy()
                new_edited_check_box.pack(fill='both', expand=True, pady=(0, 10))

    def duplicate_task(self):
        if self.selected_task_check_box:
            new_duped_check_box = TaskCheckBox(self.master, task=self.selected_task_check_box.task)
            new_duped_check_box.pack(fill='both', expand=True, pady=(0, 10))
            self.task_manager.add_task(new_duped_check_box.task)

    def delete_task(self):
        if self.selected_task_check_box:
            if tkinter.messagebox.askyesno("Delete Task", f"Are you sure you want to delete '{self.selected_task_check_box.task.name}'?"):
                self.task_manager.delete_task(self.selected_task_check_box.task)
                self.selected_task_check_box.destroy()
