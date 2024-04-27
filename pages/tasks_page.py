import datetime
import os
import tkinter

import customtkinter
import requests
from PIL import Image
from utils.online_icalendar import OnlineICalendar
from tkcalendar import Calendar as tkCalendar

from utils.directory_manager import get_icon_dir, get_app_dir
from utils.settings import settings
from widgets import CheckBox
from widgets.Buttons import DefaultButton
from widgets.CheckBox import TaskCheckBox
from widgets.CheckBoxManager import CheckBoxManager
from widgets.HyperLink import HyperLink
from widgets.Page import Page
from widgets.PopupForm import PopupForm
from widgets.Popups import SuccessPopup, ErrorPopup
from tkinter import messagebox

ALL_TASK_SOURCES = ["MyOpenMath", "BlackBoard", "Achieve"]


class TasksPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color='white')
        tasks_label = customtkinter.CTkLabel(self, text="My Tasks", font=('Roboto', 36))
        tasks_label.pack(padx=10, pady=(50, 10), side='top', anchor='nw')

        top_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        top_buttons_frame.pack(padx=10, pady=(0, 5), side='top', anchor='nw')

        import_tasks_button = DefaultButton(top_buttons_frame, text="Import Tasks",
                                            image=customtkinter.CTkImage(Image.open(f'{get_icon_dir()}'
                                                                                    f'{os.sep}download.png')))
        import_tasks_button.pack(padx=(0, 10), side='left', anchor='nw')

        add_task_button = DefaultButton(top_buttons_frame, text="Add Task",
                                        image=customtkinter.CTkImage(Image.open(f'{get_icon_dir()}'
                                                                                f'{os.sep}plus-square.png')))
        add_task_button.pack(padx=(0, 10), side='left', anchor='nw')

        clear_all_tasks_button = DefaultButton(top_buttons_frame, text="Clear All",
                                               image=customtkinter.CTkImage(Image.open(f'{get_icon_dir()}'
                                                                                       f'{os.sep}trash.png')))
        clear_all_tasks_button.pack(padx=(0, 10))

        tasks_list_and_info_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        tasks_list_and_info_frame.pack(fill='both', expand=True)

        tasks_scrollable_frame = customtkinter.CTkScrollableFrame(master=tasks_list_and_info_frame,
                                                                  fg_color='transparent')
        tasks_scrollable_frame.pack(fill='both', expand=True, padx=(5, 10), pady=(5, 5), side='left')

        task_info_frame = customtkinter.CTkFrame(tasks_list_and_info_frame, fg_color='white', width=10)
        task_info_frame.pack(side='right', fill='both', expand=True)

        check_box_manager = CheckBoxManager(f'{get_app_dir()}{os.sep}tasks.json')

        def clear_info_frame():
            # Clear details frame
            for child in task_info_frame.winfo_children():
                child.destroy()

        def init_checkbox(new_check_box: TaskCheckBox):

            def display_details(event):
                # Set selected checkbox to current
                check_box_manager.set_active(new_check_box.get_checkbox_data())
                clear_info_frame()
                task_header_font = ('Roboto', 12)
                task_header_color = 'grey'
                display_task_name = customtkinter.CTkLabel(task_info_frame,
                                                           text=new_check_box.get_task_name(), font=('Roboto', 26))
                display_task_name.pack()

                about_label = customtkinter.CTkLabel(task_info_frame, text="About",
                                                     font=('Roboto bold', 14, 'bold'))
                about_label.pack()

                source_header_label = customtkinter.CTkLabel(task_info_frame, text="Source",
                                                             font=task_header_font,
                                                             text_color=task_header_color)
                source_header_label.pack(anchor='w')

                source_label = customtkinter.CTkLabel(task_info_frame, text=new_check_box.get_task_source())
                source_label.pack(anchor='w')

                link_header_label = customtkinter.CTkLabel(task_info_frame, text="Link", font=task_header_font,
                                                           text_color=task_header_color)
                link_header_label.pack(anchor='w')

                link_hyperlink = HyperLink(task_info_frame, url=new_check_box.get_task_link())
                link_hyperlink.pack(anchor='w')

                due_date_header = customtkinter.CTkLabel(task_info_frame, text="Due Date", font=task_header_font,
                                                         text_color=task_header_color)
                due_date_header.pack(anchor='w')

                task_due_date = customtkinter.CTkLabel(
                    task_info_frame,
                    text=f"{CheckBox.get_day_of_week_string(new_check_box.get_task_due_date())}, "
                         f"{CheckBox.get_month_abbreviation(new_check_box.get_task_due_date())} "
                         f"{CheckBox.get_day(new_check_box.get_task_due_date())}, "
                         f"{CheckBox.get_time_suffix(new_check_box.get_task_due_date())}")
                task_due_date.pack(anchor='w')

            def delete():
                if tkinter.messagebox.askyesno("Delete Task",
                                               f"Are you sure you want to delete "
                                               f"'{new_check_box.cget("text")}'?"):
                    # Check if the current selected checkbox id matches with our checkbox id
                    active_checkbox = check_box_manager.get_active()
                    if active_checkbox == new_check_box.get_checkbox_data():
                        # Destroy all items in details frame
                        clear_info_frame()
                        # Unset active checkbox
                        check_box_manager.remove_active()

                    new_check_box.task_item_frame.destroy()
                    check_box_manager.remove_checkbox_data_by_id(new_check_box.get_task_id())
                    new_check_box.destroy()

            # Right Click menu
            right_click_menu = tkinter.Menu()
            right_click_menu.add_command(label="Delete", command=delete)

            def action_menu(event):
                right_click_menu.tk_popup(event.x_root, event.y_root)

            def toggle_state():
                old_data = check_box_manager.check_boxes_data.pop(new_check_box.get_task_id())
                new_data = new_check_box.get_checkbox_data()
                new_data.completion_status = 1 if old_data.completion_status == 0 else 0
                check_box_manager.check_boxes_data[new_check_box.task_id] = new_data
                check_box_manager.save_to_file()

            new_check_box.configure(command=toggle_state)

            new_check_box.bind("<Button-2>", action_menu)
            new_check_box.task_item_frame.bind("<Button-2>", action_menu)
            new_check_box.task_info_frame.bind("<Button-2>", action_menu)

            new_check_box.task_item_frame.bind("<Button-1>", display_details)
            new_check_box.bind("<Button-1>", display_details)

        load_popup = SuccessPopup(self, "Loading saved tasks...", 100000)

        def load_saved_checkboxes():
            for checkbox_data in check_box_manager.load_from_file().values():
                check_box = TaskCheckBox(tasks_scrollable_frame, task_id=checkbox_data.task_id,
                                         text=checkbox_data.task_name, source=checkbox_data.task_source,
                                         link=checkbox_data.task_link, due_date=checkbox_data.task_due_date)
                init_checkbox(check_box)
                if checkbox_data.completion_status == 1:
                    check_box.select()
                check_box.pack(fill='both', expand=True, pady=(0, 10))
            load_popup.slide_up()

        self.after(0, load_saved_checkboxes)

        # Command call backs
        def add_task_callback():
            task_popup_form = PopupForm(self)
            task_popup_form.wm_title("Add Task")

            task_name_entry = customtkinter.CTkEntry(task_popup_form, placeholder_text='Task Name')
            task_source_entry = customtkinter.CTkComboBox(task_popup_form,
                                                          values=ALL_TASK_SOURCES)
            task_link_entry = customtkinter.CTkEntry(task_popup_form, placeholder_text='Task Link')
            hour_drop_down = customtkinter.CTkOptionMenu(task_popup_form,
                                                         values=[str(i) for i in range(1, 24)])
            minute_drop_down = customtkinter.CTkOptionMenu(task_popup_form,
                                                           values=[str(i) for i in range(60)])

            due_date_calendar = tkCalendar(task_popup_form)
            due_date_calendar.pack(padx=10)

            task_name_entry.pack(pady=10)
            task_source_entry.pack(pady=10)
            task_link_entry.pack(pady=10)
            hour_drop_down.pack(padx=5, pady=10)
            minute_drop_down.pack(padx=5, pady=10)

            task_popup_form.add_widget(task_name_entry)
            task_popup_form.add_widget(task_source_entry)
            task_popup_form.add_widget(task_link_entry)
            task_popup_form.add_widget(hour_drop_down)
            task_popup_form.add_widget(minute_drop_down)

            # Wait for window to be destroyed or submitted
            self.wait_window(task_popup_form)

            # Check if the user pressed the submit button if yes get the data else do nothing
            if task_popup_form.data_ready:
                task_name = task_popup_form.get_data(task_name_entry)
                task_source = task_popup_form.get_data(task_source_entry)
                task_link = task_popup_form.get_data(task_link_entry)
                original_format_string = '%m/%d/%y %H:%M'
                desired_format_string = '%m-%d-%Y-%H-%M'
                parsed_date = datetime.datetime.strptime(
                    f"{due_date_calendar.get_date()} "
                    f"{task_popup_form.get_data(hour_drop_down)}:{task_popup_form.get_data(minute_drop_down)}",
                    original_format_string)
                formatted_date = parsed_date.strftime(desired_format_string)
                new_task_id = check_box_manager.load_last_id()
                new_check_box = TaskCheckBox(tasks_scrollable_frame, task_id=new_task_id,
                                             text=task_name, source=task_source,
                                             link=task_link, due_date=formatted_date)

                init_checkbox(new_check_box)
                check_box_manager.add_checkbox(new_task_id, new_check_box.get_checkbox_data())
                new_check_box.pack(fill='both', expand=True, pady=(0, 10))

        def clear_tasks_callback():
            if messagebox.askyesno("Delete all tasks", "Are you sure you want to delete all of your tasks?"):
                for child in tasks_scrollable_frame.winfo_children():
                    # Delete from the checkbox manager
                    # TODO: FIND A NEW WAY TO DELETE THE TASK CHECKBOX
                    task_check_box = child.winfo_children()[1]
                    if isinstance(task_check_box, TaskCheckBox):
                        check_box_manager.remove_checkbox_data_by_id(task_check_box.task_id)
                        child.destroy()
                    else:
                        ErrorPopup(self, f"Could not delete task {task_check_box}")
                # Reset uid file
                check_box_manager.reset_ids()
                # Reset the checkbox active
                check_box_manager.remove_active()
                # Delete all children in tasks information
                clear_info_frame()

        def import_tasks_callback():
            # Create a new toplevel
            new_top_level = customtkinter.CTkToplevel(self, fg_color='white')
            new_top_level.wm_title("Import Tasks")

            # Only capture events for this window
            new_top_level.grab_set()

            # Source Sections Frame
            # ==BB==
            bb_header_label = customtkinter.CTkLabel(new_top_level, text='BlackBoard', font=('Roboto', 18, 'bold'))
            bb_header_label.pack(anchor='w', padx=10)

            bb_section = customtkinter.CTkFrame(new_top_level, fg_color='transparent', corner_radius=0)
            bb_section.pack(fill='both')

            bb_calendar_url_label = customtkinter.CTkLabel(bb_section, text="iCalendar URL",
                                                           font=('Roboto', 14))
            bb_calendar_url_label.pack(anchor='w', padx=12)

            bb_calendar_url_entry = customtkinter.CTkEntry(bb_section, width=550,
                                                           placeholder_text='iCalendar URL')
            bb_calendar_url_entry.pack(anchor='w', padx=10, pady=(5, 10))
            # Set the url from the settings
            bb_calendar_url_entry.insert(0, settings.get_setting("bb_url", ""))

            bb_button_layout = customtkinter.CTkFrame(bb_section, fg_color='transparent')
            bb_button_layout.pack(anchor='w', padx=10, expand=True)

            bb_calendar_url_save_button = DefaultButton(bb_button_layout, text="Save URL")
            bb_calendar_url_save_button.pack(side='left', padx=(0, 5))

            def bb_save_url():
                settings.add_setting("bb_url", bb_calendar_url_entry.get())
                # Show success popup
                SuccessPopup(new_top_level, "Successfully saved url")

            bb_calendar_url_save_button.configure(command=bb_save_url)

            bb_load_button = DefaultButton(bb_button_layout, text="Load Tasks")
            bb_load_button.pack(side='left', padx=10)

            bb_scrollable_frame = customtkinter.CTkScrollableFrame(master=bb_section,
                                                                   fg_color='transparent')
            bb_scrollable_frame.pack(fill='both', expand=True, padx=(5, 10), pady=(5, 5), side='left')

            bb_select_all_button = DefaultButton(bb_button_layout, text="Select All")
            bb_select_all_button.pack(anchor='e', padx=10)

            self.loaded_tasks = []

            def bb_load_tasks():
                # Set loaded to none
                self.loaded_tasks = []
                # Clear the task frame
                for child in bb_scrollable_frame.winfo_children():
                    child.destroy()
                SuccessPopup(new_top_level, "Loading BlackBoard Tasks...")
                try:
                    online_icalendar = OnlineICalendar(bb_calendar_url_entry.get())
                    for event in online_icalendar.get_events():
                        task_name = event.get("SUMMARY")
                        task_due_date: datetime.datetime = event.get("DTEND").dt
                        task_due_date_str = task_due_date.strftime("%m-%d-%Y-%H-%M")
                        # Convert the date to usable format
                        new_bb_task = TaskCheckBox(bb_scrollable_frame, text=task_name, source="BlackBoard",
                                                   link=None, task_id=0, due_date=task_due_date_str)
                        new_bb_task.pack(anchor='w')
                        # Add to list
                        self.loaded_tasks.append(new_bb_task)
                except requests.HTTPError as request_error:
                    ErrorPopup(new_top_level, f"{request_error}")
                except Exception as error:
                    ErrorPopup(new_top_level, f"Error => {error}")

            bb_load_button.configure(command=bb_load_tasks)

            def bb_select_all():
                for child in bb_scrollable_frame.winfo_children():
                    task_check_box = child.winfo_children()[1]
                    if isinstance(task_check_box, TaskCheckBox):
                        if not task_check_box.get():
                            task_check_box.select()
                        else:
                            task_check_box.deselect()

            bb_select_all_button.configure(command=bb_select_all)

            # ==BB==

            # Add all button
            add_all_tasks_button = DefaultButton(new_top_level, text="Add Selected Tasks")
            add_all_tasks_button.pack(pady=10)

            def add_all_tasks():
                while self.loaded_tasks:
                    task_box: TaskCheckBox = self.loaded_tasks.pop()
                    # If selected
                    if task_box.get():
                        # Unselect the checkbox
                        task_box.deselect()
                        task_box_data = task_box.get_checkbox_data()
                        # Generate new id and set id
                        task_box_data.task_id = check_box_manager.load_last_id()
                        # Add to checkbox manager
                        check_box_manager.add_checkbox(task_box_data.task_id, task_box_data)
                        # Pack the checkbox
                        new_task_box = TaskCheckBox(tasks_scrollable_frame, task_box_data.task_id,
                                                    task_box_data.task_source, task_box_data.task_link,
                                                    task_box_data.task_due_date, text=task_box_data.task_name)
                        init_checkbox(new_task_box)
                        new_task_box.pack(fill='both', expand=True, pady=(0, 10))

                # Close all
                new_top_level.destroy()
                SuccessPopup(self, "Successfully Loaded Tasks")

            add_all_tasks_button.configure(command=add_all_tasks)

        add_task_button.configure(command=add_task_callback)
        clear_all_tasks_button.configure(command=clear_tasks_callback)
        import_tasks_button.configure(command=import_tasks_callback)
