from typing import Any

import customtkinter

from widgets.buttons import DefaultButton
from widgets.popups.validation.widget_data_validator import BaseValidator, NonEmptyValidator, NumericValidator


class PopupForm(customtkinter.CTkToplevel):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)
        self.widgets: list[customtkinter.CTkBaseClass] = []
        self.submit_button = DefaultButton(self, text='Submit', command=self.on_submit)
        self.submit_button.pack(side='bottom', pady=10)
        self.data_ready = False
        self.data = {}
        self.validators: dict[int, list[BaseValidator]] = {}
        # Make the window always on top
        self.transient(master)
        # Only capture events for this popup
        self.grab_set()

    def add_widget(self, widget: customtkinter.CTkBaseClass, validators: list[BaseValidator] | None = None):
        self.widgets.append(widget)
        self.data[id(widget)] = None
        self.validators[id(widget)] = validators

    def on_submit(self):
        data_is_valid = True
        for widget in self.widgets:
            if (isinstance(widget, customtkinter.CTkEntry) or isinstance(widget, customtkinter.CTkComboBox) or
                    isinstance(widget, customtkinter.CTkOptionMenu)):
                widget_data = widget.get()
                widget_validators = self.validators.get(id(widget))
                if widget_validators:
                    for validator in widget_validators:
                        if not validator.validate(widget):
                            data_is_valid = False
                            break
                # Data is valid and can be placed
                self.data[id(widget)] = widget.get()
        if data_is_valid:
            self.data_ready = True
            self.destroy()

    def get_data(self, widget):
        if self.data_ready:
            return self.data[id(widget)]
        else:
            raise Exception(f"Data is not ready or submitted yet. Widget => {widget}")


if __name__ == '__main__':
    root = customtkinter.CTk()
    p = PopupForm(root)
    tasks_name_text_box = customtkinter.CTkEntry(p, placeholder_text="Task Name")
    tasks_name_text_box.pack(pady=10)

    tasks_name_text_box2 = customtkinter.CTkEntry(p, placeholder_text="Task Name 2")
    tasks_name_text_box2.pack()

    age_text_box = customtkinter.CTkEntry(p, placeholder_text="Age")
    age_text_box.pack(pady=10)

    p.add_widget(tasks_name_text_box, [NonEmptyValidator()])
    p.add_widget(tasks_name_text_box2)
    p.add_widget(age_text_box, [NumericValidator(0, 100)])
    root.wait_window(p)
    # If we got data
    if p.data_ready:
        print(f'Task Name Data: {p.get_data(tasks_name_text_box)}')
        print(f'Task Name 2 Data: {p.get_data(tasks_name_text_box2)}')
        print(f'Age Data: {p.get_data(age_text_box)}')
    # User clicked the exit button
    else:
        print('User cancelled action')
    root.mainloop()
