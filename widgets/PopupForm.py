from typing import Any

import customtkinter

from widgets.Buttons import DefaultButton


class PopupForm(customtkinter.CTkToplevel):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)
        self.entries: list[customtkinter.CTkEntry] = []
        self.submit_button = DefaultButton(self, text='Submit', command=self.on_submit)
        self.submit_button.pack(side='bottom', pady=10)
        self.data = None

    def add_field(self, text_box: customtkinter.CTkEntry):
        self.entries.append(text_box)
        self.pack_fields()

    def pack_fields(self):
        for child in self.entries:
            child.pack()

    def on_submit(self):
        self.get_data_from_fields()
        self.destroy()

    def get_data_from_fields(self):
        self.data = [entry.get() for entry in self.entries]


if __name__ == '__main__':
    root = customtkinter.CTk()
    p = PopupForm(root)
    tasks_name_text_box = customtkinter.CTkEntry(p, placeholder_text="Task Name")
    tasks_name_text_box.pack(pady=10)
    tasks_name_text_box2 = customtkinter.CTkEntry(p, placeholder_text="Task Name 2")
    p.add_field(tasks_name_text_box)
    p.add_field(tasks_name_text_box2)
    print(p)
    root.wait_window(p)
    print(p.data)
    root.mainloop()
