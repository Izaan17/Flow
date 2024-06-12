import tkinter
from typing import Any
import utils
import customtkinter


class DefaultEntry(customtkinter.CTkEntry):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)
        self.right_click_menu = tkinter.Menu(self, tearoff=0)
        self.right_click_menu.add_command(label="Copy", command=self._copy_text)
        self.right_click_menu.add_command(label="Paste", command=self._paste_text)
        self.right_click_menu.add_command(label="Select All", command=self._select_all)

        self.bind(utils.system.right_click_binding_key_code,
                  lambda event: self.right_click_menu.tk_popup(event.x_root, event.y_root))

    def _copy_text(self):
        try:
            selection = self.selection_get()
        except tkinter.TclError:
            selection = self.get()
        self.master.clipboard_clear()
        self.master.clipboard_append(selection)

    def _paste_text(self):
        self.delete(0, tkinter.END)
        self.insert(0, self.master.clipboard_get())

    def _select_all(self):
        self.focus_set()
        self.select_range(0, tkinter.END)
