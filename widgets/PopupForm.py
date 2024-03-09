from typing import Any

import customtkinter

from widgets.Buttons import DefaultButton


class PopupForm(customtkinter.CTkToplevel):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)
        self.widgets: list[customtkinter.CTkBaseClass] = []
        self.submit_button = DefaultButton(self, text='Submit', command=self.on_submit)
        self.submit_button.pack(side='bottom', pady=10)
        self.data_ready = False
        self.data = {}

    def add_widget(self, widget: customtkinter.CTkBaseClass):
        self.widgets.append(widget)
        self.data[id(widget)] = None

    def on_submit(self):
        for widget in self.widgets:
            if (isinstance(widget, customtkinter.CTkEntry) or isinstance(widget, customtkinter.CTkComboBox) or
                    isinstance(widget, customtkinter.CTkOptionMenu)):
                self.data[id(widget)] = widget.get()
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
    p.add_widget(tasks_name_text_box)
    p.add_widget(tasks_name_text_box2)
    root.wait_window(p)
    # If we got data
    if p.data_ready:
        print(f'Task Name Data: {p.get_data(tasks_name_text_box)}')
        print(f'Task Name 2 Data: {p.get_data(tasks_name_text_box2)}')
    # User clicked the exit button
    else:
        print('User cancelled action')
    root.mainloop()
