import tkinter
from typing import Any
import utils
from widgets.popups.validation.widget_data_validator import BaseValidator

import customtkinter


class DefaultEntry(customtkinter.CTkEntry):
    def __init__(self, master: Any, validators: None | list[BaseValidator] = None, **kwargs):
        super().__init__(master, **kwargs)
        self.validators = validators
        self.right_click_menu = tkinter.Menu(self, tearoff=0)
        self.right_click_menu.add_command(label="Cut", command=self._cut_text)
        self.right_click_menu.add_command(label="Copy", command=self._copy_text)
        self.right_click_menu.add_command(label="Paste", command=self._paste_text)
        self.right_click_menu.add_command(label="Select All", command=self._select_all)

        self.bind(utils.system.right_click_binding_key_code,
                  lambda event: self.right_click_menu.tk_popup(event.x_root, event.y_root))
        self._update_context_menu()
        self.bind("<KeyRelease>", self._update_context_menu)
        self.bind("<ButtonRelease>", self._update_context_menu)
        self.bind(utils.system.undo_button_sequence, self.undo)
        self.bind(utils.system.redo_button_sequence, self.redo)
        self.bind("<Key>", self.on_key_press)

        self.undo_stack = []
        self.redo_stack = []

    def undo(self, event=None):
        if self.undo_stack:
            text = self.undo_stack.pop()
            self.redo_stack.append(self.get())
            self.delete(0, tkinter.END)
            self.insert(0, text)

    def redo(self, event=None):
        if self.redo_stack:
            text = self.redo_stack.pop()
            self.undo_stack.append(self.get())
            self.delete(0, tkinter.END)
            self.insert(0, text)

    def on_key_press(self, event):
        if event.keysym not in [utils.system.undo_button_name, utils.system.redo_button_name, "z", "y"]:
            self.undo_stack.append(self.get())
            self.redo_stack.clear()

    def _cut_text(self):
        if self.select_present():
            self._copy_text()
            self.delete("sel.first", "sel.last")

    def _copy_text(self):
        if self.select_present():
            selection = self.selection_get()
        else:
            selection = self.get()
        self.clipboard_clear()
        self.clipboard_append(selection)

    def _paste_text(self):
        self.delete(0, tkinter.END)
        self.insert(0, self.clipboard_get())

    def _select_all(self):
        self.focus_set()
        self.select_range(0, tkinter.END)

    def _update_context_menu(self, event=None):
        try:
            if self.select_present():
                self.right_click_menu.entryconfig(0, state="normal")
                self.right_click_menu.entryconfig(1, state="normal")
            else:
                self.right_click_menu.entryconfig(0, state="disabled")
                self.right_click_menu.entryconfig(1, state="disabled")
        except tkinter.TclError:
            # Catch any errors in case the menu item labels are not found
            pass

    def validated_get(self):
        if not self.validators:
            return self.get()

        for validator in self.validators:
            if not validator.validate(self):
                return False
        return self.get()
