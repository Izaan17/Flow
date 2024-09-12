from functools import partial
import customtkinter
from utils.settings import settings
from widgets.dropdown import DefaultDropDown
from widgets.switch import DefaultSwitch
from widgets.page import Page


def create_dropdown(frame, label_text, values, command, setting_key, default_value):
    dropdown = DefaultDropDown(frame, label_text=label_text, values=values, command=command)
    dropdown.pack(anchor='w')
    dropdown.set(settings.get_setting(setting_key, default_value))
    return dropdown


def create_switch(frame, label_text, setting_key, backup_default="False"):
    current_value = settings.get_setting(setting_key, backup_default)  # Get current setting value
    switch_var = customtkinter.StringVar(value=current_value)

    def on_switch_toggle():
        settings.add_setting(setting_key, switch_var.get())
        # Auto change the text
        ctk_switch.configure(text=switch_var.get())

    ctk_switch = DefaultSwitch(frame, label_text=label_text, command=on_switch_toggle,
                               variable=switch_var, onvalue="True", offvalue="False", text=current_value)
    ctk_switch.pack(anchor='w')
    return ctk_switch


def on_setting_change(setting_key, choice):
    settings.add_setting(setting_key, choice)


def on_icon_size_change(choice):
    width, height = choice.split("x")
    settings.add_setting("icon_width", width)
    settings.add_setting("icon_height", height)


class SettingsPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, page_title="Settings",
                         subheading="Edit all your settings here.")

        self.all_icon_sizes = ["24x24", "50x50", "100x100", "100x125", "125x100", "125x125", "200x200"]

        self.drop_downs_frame = customtkinter.CTkFrame(self, fg_color='white')
        self.drop_downs_frame.pack(fill='both', expand=True)

        self.show_image_preview = create_switch(self.drop_downs_frame, "Show Image Preview", "show_img_preview",
                                                backup_default="True")

        self.allow_full_directory_deletion = create_switch(self.drop_downs_frame, "Allow Full Directory Deletion",
                                                           "allow_full_dir_deletion")

        # Create dropdowns with a generic handler
        self.max_items_per_row = create_dropdown(
            self.drop_downs_frame, "Max Items Per Row", [str(i) for i in range(5, 11)],
            partial(on_setting_change, "max_items_per_row"), "max_items_per_row", 5
        )

        self.max_text_length = create_dropdown(
            self.drop_downs_frame, "Max Text Length", [str(i) for i in range(10, 50)],
            partial(on_setting_change, "max_text_length"), "max_text_length", 30
        )

        self.icon_size_drop_down = DefaultDropDown(
            self.drop_downs_frame, label_text="Icon Size", values=self.all_icon_sizes,
            command=on_icon_size_change)
        self.icon_size_drop_down.pack(anchor='w')
        self.icon_size_drop_down.set(
            f"{settings.get_setting('icon_width', 50)}x{settings.get_setting('icon_height', 50)}")


if __name__ == '__main__':
    app = customtkinter.CTk()

    page = SettingsPage(app)
    page.pack(expand=True, fill='both')

    app.mainloop()
