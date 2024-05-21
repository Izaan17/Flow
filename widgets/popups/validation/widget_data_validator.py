import customtkinter


class Validators:
    def __init__(self):
        pass


class BaseValidator:
    def __init__(self):
        self.original_color = None
        self.error_label = None
        self.error_label_id = None  # Store the id of the scheduled error label deletion

    def validate(self, widget) -> bool:
        """Override this method in specific validators."""
        raise NotImplementedError("Subclasses should implement this method")

    def indicate_error(self, widget, error_message, duration=3000):
        """Indicate an error visually on the widget."""
        if widget.cget("fg_color") != "red":
            self.original_color = widget.cget("fg_color")
            widget.configure(fg_color="red")
            widget.focus_set()

            if self.error_label:
                self.error_label.configure(text=error_message)
            else:
                self.error_label = customtkinter.CTkLabel(widget.master, text=error_message)
                self.error_label.place(in_=widget, anchor="nw")

            # Schedule deletion of the error label after duration milliseconds
            self.error_label_id = self.error_label.after(duration, self.clear_error, widget)

    def clear_error(self, widget):
        """Clear the error indication on the widget."""
        if self.original_color is not None:
            widget.configure(fg_color=self.original_color)
        self.original_color = None

        if self.error_label:
            self.error_label.destroy()
            self.error_label = None
            # Cancel scheduled deletion if it exists
            if self.error_label_id:
                widget.after_cancel(self.error_label_id)
                self.error_label_id = None


class NonEmptyValidator(BaseValidator):
    error_message = "This field cannot be empty."

    def validate(self, widget) -> bool:
        widget_value = widget.get()
        if not widget_value.strip():
            self.indicate_error(widget, self.error_message)
            return False
        self.clear_error(widget)
        return True


class NumericValidator(BaseValidator):

    def __init__(self, min_value=None, max_value=None):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, widget) -> bool:
        widget_value = widget.get()
        if not widget_value.isdigit():
            self.indicate_error(widget, f"Value must be an integer.")
            return False

        num_value = int(widget_value)
        if (self.min_value is not None and num_value < self.min_value) or (self.max_value is not None and num_value >
                                                                           self.max_value):
            self.indicate_error(widget, f"Value must be between {self.min_value} - {self.max_value}.")
            return False

        self.clear_error(widget)
        return True
