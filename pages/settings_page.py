from functools import partial
import customtkinter
from utils.settings import settings
from widgets.Dropdown import DefaultDropDown
from widgets.Page import Page


def create_dropdown(frame, label_text, values, command, setting_key, default_value):
    dropdown = DefaultDropDown(frame, label_text=label_text, values=values, command=command)
    dropdown.pack(anchor='w')
    dropdown.set(settings.get_setting(setting_key, default_value))
    return dropdown


def on_setting_change(setting_key, choice):
    settings.add_setting(setting_key, choice)


def on_icon_size_change(choice):
    width, height = choice.split("x")
    settings.add_setting("icon_width", width)
    settings.add_setting("icon_height", height)


class SettingsPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color='white')

        self.all_icon_sizes = ["24x24", "50x50", "100x100", "100x125", "125x100", "125x125", "200x200"]

        self.settings_label = customtkinter.CTkLabel(self, text="Settings", font=('Roboto', 36))
        self.settings_label.pack(padx=10, pady=(50, 10), side='top', anchor='nw')

        self.drop_downs_frame = customtkinter.CTkFrame(self, fg_color='white')
        self.drop_downs_frame.pack(fill='both', expand=True)

        # Create dropdowns with a generic handler
        self.max_items_per_row = create_dropdown(
            self.drop_downs_frame, "Max Items Per Row", [str(i) for i in range(5, 11)],
            partial(on_setting_change, "max_items_per_row"), "max_items_per_row", 5
        )

        self.max_text_length = create_dropdown(
            self.drop_downs_frame, "Max Text Length", [str(i) for i in range(10, 50)],
            partial(on_setting_change, "max_text_length"), "max_text_length", 30
        )

        self.show_image_preview = create_dropdown(
            self.drop_downs_frame, "Show Image Preview", ["True", "False"],
            partial(on_setting_change, "show_img_preview"), "show_img_preview", "True"
        )

        self.icon_size_drop_down = DefaultDropDown(
            self.drop_downs_frame, label_text="Icon Size", values=self.all_icon_sizes,
            command=on_icon_size_change)
        self.icon_size_drop_down.pack(anchor='w')
        self.icon_size_drop_down.set(
            f"{settings.get_setting('icon_width', 50)}x{settings.get_setting('icon_height', 50)}")

        self.allow_full_directory_deletion = create_dropdown(
            self.drop_downs_frame, "Full Directory Deletion", ["True", "False"],
            partial(on_setting_change, "allow_full_dir_deletion"), "allow_full_dir_deletion", "False"
        )
