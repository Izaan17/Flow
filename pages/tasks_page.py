import datetime
import os
from tkinter import messagebox

import customtkinter
import requests
from tkcalendar import dateentry

import utils.date
import utils.system
import utils.widget_utils
from constants import ALL_TASK_SOURCES
from database.task_manager import TaskManager
from models import Task
from utils.directory_manager import get_app_dir
from utils.icon import load_icon
from utils.online_icalendar import OnlineICalendar
from utils.settings import settings
from widgets.buttons import DefaultButton
from widgets.entry import DefaultEntry
from widgets.page import Page
from widgets.popups.PopupForm import PopupForm
from widgets.popups.Popups import SuccessPopup, ErrorPopup
from widgets.popups.validation.widget_data_validator import NonEmptyValidator, NumericValidator
from widgets.task_check_box import TaskCheckBox
from widgets.task_check_box_context_menu import TaskContextMenu
from widgets.task_check_box_details_displayer import TaskCheckBoxDisplayer


class TasksPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, page_title="My Tasks")

        # Initialize DB
        self.task_manager = TaskManager(f'{get_app_dir()}{os.sep}tasks.db')

        self.current_date = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M")
        # Change subheading
        self.subheading.configure(text=f"{utils.date.get_day_of_week_string(self.current_date)}, "
                                       f"{utils.date.get_month_string(self.current_date)} "
                                       f"{utils.date.get_day_string(self.current_date)}")

        # Setup page buttons
        self.top_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.top_buttons_frame.pack(padx=10, pady=(0, 5), side='top', anchor='nw')

        self.import_tasks_button = DefaultButton(self.top_buttons_frame, text="Import Tasks",
                                                 command=self.import_tasks_callback,
                                                 image=load_icon("download.png"))
        self.import_tasks_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.add_task_button = DefaultButton(self.top_buttons_frame, text="Add Task", command=self.add_task_callback,
                                             image=load_icon("plus-square.png"))
        self.add_task_button.pack(padx=(0, 10), side='left', anchor='nw')

        self.clear_all_tasks_button = DefaultButton(self.top_buttons_frame, text="Clear All",
                                                    command=self.clear_tasks_callback,
                                                    image=load_icon("trash.png"))
        self.clear_all_tasks_button.pack(side='left', padx=(0, 10))

        self.task_count_label = customtkinter.CTkLabel(self.top_buttons_frame, text=f"Count: N/A",
                                                       height=50)
        self.task_count_label.pack(anchor='e')

        self.tasks_list_and_info_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.tasks_list_and_info_frame.pack(fill='both', expand=True)

        self.tasks_scrollable_frame = customtkinter.CTkScrollableFrame(master=self.tasks_list_and_info_frame,
                                                                       fg_color='transparent', width=800,
                                                                       scrollbar_button_color='white')
        self.tasks_scrollable_frame.pack(fill='both', expand=True, padx=(5, 10), pady=(5, 5), side='left')

        self.task_info_frame = customtkinter.CTkFrame(self.tasks_list_and_info_frame, fg_color='white')

        # Init task context menu
        self.task_context_menu = TaskContextMenu(self.tasks_scrollable_frame, self.task_manager)

        # Initialize task displayer
        self.task_check_box_displayer = TaskCheckBoxDisplayer(self.tasks_scrollable_frame, self.task_info_frame)

        # Load checkboxes threaded
        self.after(5, self.load_saved_tasks)
        self.update_count_label()

    def add_task_callback(self):
        task_popup_form = PopupForm(self, fg_color='white')
        task_popup_form.wm_title("Add Task")

        task_entries_frame = customtkinter.CTkFrame(task_popup_form)
        task_entries_frame.pack(fill='both', expand=True, padx=10, pady=10)

        task_name_entry = DefaultEntry(task_entries_frame, placeholder_text='Task Name')
        task_source_entry = customtkinter.CTkComboBox(task_entries_frame,
                                                      values=ALL_TASK_SOURCES)
        task_link_entry = DefaultEntry(task_entries_frame, placeholder_text='Task Link')
        hour_entry = DefaultEntry(task_entries_frame, placeholder_text='Hour')
        minute_entry = DefaultEntry(task_entries_frame, placeholder_text='Minutes')

        due_date_calendar = dateentry.Calendar(task_entries_frame)
        due_date_calendar.pack(padx=10, pady=15)

        task_name_entry.pack(padx=20, pady=15)
        task_source_entry.pack(padx=20, pady=10)
        task_link_entry.pack(padx=20, pady=10)
        hour_entry.pack(padx=20, pady=15)
        minute_entry.pack(padx=20, pady=15)

        task_popup_form.add_widget(task_name_entry, [NonEmptyValidator()])
        task_popup_form.add_widget(task_source_entry)
        task_popup_form.add_widget(task_link_entry)
        task_popup_form.add_widget(hour_entry, [NonEmptyValidator(), NumericValidator(1, 23)])
        task_popup_form.add_widget(minute_entry, [NonEmptyValidator(), NumericValidator(0, 59)])

        # Wait for window to be destroyed or submitted
        self.wait_window(task_popup_form)

        # Check if the user pressed the submit button if yes get the data else do nothing
        if task_popup_form.data_ready:
            task_name = task_popup_form.get_data(task_name_entry)
            task_source = task_popup_form.get_data(task_source_entry)
            task_link = task_popup_form.get_data(task_link_entry)

            # Get date from calendar and time from entries
            due_date_str = due_date_calendar.get_date()  # e.g., '9/11/24'
            hour_str = task_popup_form.get_data(hour_entry).zfill(2)  # Ensure two digits
            minute_str = task_popup_form.get_data(minute_entry).zfill(2)  # Ensure two digits

            # Combine date and time into one string
            combined_date_time_str = f"{due_date_str} {hour_str}:{minute_str}"

            # Define format strings
            original_format_string = '%m/%d/%y %H:%M'  # Format used by dateentry.Calendar
            desired_format_string = '%m-%d-%Y-%H-%M'

            # Parse and format the date
            try:
                parsed_date = datetime.datetime.strptime(combined_date_time_str, original_format_string)
                formatted_date = parsed_date.strftime(desired_format_string)
            except ValueError as e:
                print(f"Date parsing error: {e}")
                return

            # Create the task
            created_task = Task(0, task_name, task_source, task_link, formatted_date)
            task_id = self.task_manager.add_task(created_task)

            # Create and pack the new checkbox
            new_check_box = TaskCheckBox(self.tasks_scrollable_frame, created_task)
            new_check_box.pack(fill='both', expand=True, pady=(0, 10))

    def import_tasks_callback(self):
        # Create a new toplevel
        new_top_level = customtkinter.CTkToplevel(self, fg_color='white')
        new_top_level.wm_title("Import Tasks")

        # Only capture events for this window
        new_top_level.grab_set()

        # Source Sections Frame
        # --ICAL--
        ical_header_label = customtkinter.CTkLabel(new_top_level, text='iCalendar Import',
                                                   font=('Roboto', 18, 'bold'))
        ical_header_label.pack(anchor='w', padx=10)

        ical_section = customtkinter.CTkFrame(new_top_level, fg_color='transparent', corner_radius=0)
        ical_section.pack(fill='both')

        icalendar_url_label = customtkinter.CTkLabel(ical_section, text="iCalendar URL",
                                                     font=('Roboto', 14))
        icalendar_url_label.pack(anchor='w', padx=12)

        icalendar_url_entry = DefaultEntry(ical_section, width=550,
                                           placeholder_text='iCalendar URL')
        icalendar_url_entry.pack(anchor='w', padx=10, pady=(5, 10))
        # Set the url from the settings
        icalendar_url_entry.insert(0, settings.get_setting("ical_url", ""))

        ical_button_layout = customtkinter.CTkFrame(ical_section, fg_color='transparent')
        ical_button_layout.pack(anchor='w', padx=10, expand=True)

        icalendar_url_save_button = DefaultButton(ical_button_layout, text="Save URL")
        icalendar_url_save_button.pack(side='left', padx=(0, 5))

        def ical_save_url():
            settings.add_setting("ical_url", icalendar_url_entry.get())
            # Show success popup
            SuccessPopup(new_top_level, "Successfully saved url")

        icalendar_url_save_button.configure(command=ical_save_url)

        ical_load_button = DefaultButton(ical_button_layout, text="Load From URL")
        ical_load_button.pack(side='left', padx=10)

        ical_scrollable_frame = customtkinter.CTkScrollableFrame(master=ical_section,
                                                                 fg_color='transparent')
        ical_scrollable_frame.pack(fill='both', expand=True, padx=(5, 10), pady=(5, 5), side='left')

        ical_select_all_button = DefaultButton(ical_button_layout, text="Select All")
        ical_select_all_button.pack(anchor='e', padx=10)

        loaded_tasks = []

        def ical_load_tasks():
            # Clear the task frame
            for child in ical_scrollable_frame.winfo_children():
                child.destroy()
            try:
                online_icalendar = OnlineICalendar(icalendar_url_entry.get())
                done = 0
                events = online_icalendar.get_events()
                length = len(events)
                for event in events:
                    task_name = event.get("SUMMARY")
                    task_due_date: datetime.datetime = event.get("DTEND").dt
                    task_due_date_str = task_due_date.strftime("%m-%d-%Y-%H-%M")
                    # Convert the date to usable format
                    new_task = Task(0, task_name, 'iCalendar', link=None, due_date=task_due_date_str)
                    new_ical_task = TaskCheckBox(ical_scrollable_frame, new_task)
                    new_ical_task.pack(anchor='w')
                    # Add to list
                    loaded_tasks.append(new_ical_task)
                    done += 1
                    SuccessPopup(new_top_level, f"{done}/{length}")
            except requests.HTTPError as request_error:
                ErrorPopup(new_top_level, f"{request_error}")
            except Exception as error:
                ErrorPopup(new_top_level, f"Error => {error}")

        ical_load_button.configure(command=ical_load_tasks)

        def ical_select_all():
            for child in ical_scrollable_frame.winfo_children():
                child: TaskCheckBox = child
                task_check_box: customtkinter.CTkCheckBox = child.get_checkbox()
                if not task_check_box.get():
                    task_check_box.select()
                else:
                    task_check_box.deselect()

        ical_select_all_button.configure(command=ical_select_all)

        # --ICAL--

        # Add all button
        add_all_tasks_button = DefaultButton(new_top_level, text='Add Selected Tasks')
        add_all_tasks_button.pack(pady=10)

        def add_all_tasks():
            while loaded_tasks:
                task_box: TaskCheckBox = loaded_tasks.pop()
                # If selected
                if task_box.checkbox.get():
                    # Unselect the checkbox
                    task_box.checkbox.deselect()
                    # Add to checkbox manager
                    self.task_manager.add_task(task_box.task)
                    # Pack the checkbox
                    new_task_box = TaskCheckBox(self.tasks_scrollable_frame, task=task_box.task)
                    new_task_box.pack(fill='x', expand=True, pady=(0, 10))

            # Close all
            new_top_level.destroy()
            SuccessPopup(self, 'Successfully Loaded Tasks')

        add_all_tasks_button.configure(command=add_all_tasks)

    def clear_tasks_callback(self):
        if messagebox.askyesno("Delete all tasks", "Are you sure you want to delete all of your tasks?"):
            for child in self.tasks_scrollable_frame.winfo_children():
                # Destroy the child
                if isinstance(child, TaskCheckBox):
                    child.destroy()
            # Delete table
            self.task_manager.clear_table()
            # Delete all children in tasks information
            self.task_check_box_displayer.clear_info_frame()

    def load_saved_tasks(self):
        for task in self.task_manager.get_all_tasks():
            check_box = TaskCheckBox(self.tasks_scrollable_frame, task)
            check_box.pack(fill='both', expand=True, pady=(0, 10))

    def update_count_label(self):
        self.task_count_label.configure(text=f"Count: {len(self.tasks_scrollable_frame.winfo_children()) - 1}")
        self.after(100, self.update_count_label)


if __name__ == '__main__':
    app = customtkinter.CTk()
    page = TasksPage(app)
    page.pack(expand=True, fill='both')
    app.mainloop()
