import datetime
import os

import customtkinter
from PIL import Image

from CheckBoxData import CheckBoxData
from directory_manager import get_icon_dir
from widgets.Buttons import DefaultButton
from widgets.CheckBox import TaskCheckBox
from widgets.CheckBoxManager import CheckBoxManager
from widgets.Page import Page
from widgets.PopupForm import PopupForm
from tkcalendar import Calendar

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

        check_box_manager = CheckBoxManager('saved-checkboxes')

        # Load checkboxes
        for checkbox_data in check_box_manager.load_from_file().values():
            check_box = TaskCheckBox(tasks_scrollable_frame, text=checkbox_data.task_name,
                                     source=checkbox_data.task_source,
                                     link=checkbox_data.task_link,
                                     details_frame=task_info_frame, checkbox_manager=check_box_manager,
                                     due_date=checkbox_data.task_due_date,
                                     uid=checkbox_data.id)
            if checkbox_data.completion_status == 1:
                check_box.select()
            check_box.pack(fill='both', expand=True, pady=(0, 10))

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

            due_date_calendar = Calendar(task_popup_form)
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
                new_check_box_id = check_box_manager.load_last_id()
                new_check_box = TaskCheckBox(tasks_scrollable_frame, text=task_name, source=task_source,
                                             link=task_link,
                                             details_frame=task_info_frame, checkbox_manager=check_box_manager,
                                             due_date=formatted_date,
                                             uid=new_check_box_id)
                check_box_manager.add_checkbox(CheckBoxData.from_checkbox(new_check_box,
                                                                          new_check_box_id))
                new_check_box.pack(fill='both', expand=True, pady=(0, 10))

        def clear_tasks_callback():
            for child in tasks_scrollable_frame.winfo_children():
                # Delete from the checkbox manager
                # TODO: FIND A NEW WAY TO DELETE THE TASK CHECKBOX
                check_box_manager.remove_checkbox_data(child.winfo_children()[1].id)
                child.destroy()
            # Reset uid file
            check_box_manager.reset_ids()
            # Reset the checkbox active
            check_box_manager.remove_active()
            # Delete all children in tasks information
            for child in task_info_frame.winfo_children():
                child.destroy()

        add_task_button.configure(command=add_task_callback)
        clear_all_tasks_button.configure(command=clear_tasks_callback)
