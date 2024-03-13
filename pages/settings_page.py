import customtkinter

from utils.settings import settings
from widgets.Dropdown import DefaultDropDown
from widgets.Page import Page


class SettingsPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color='white')

        self.all_icon_sizes = ["24x24", "50x50", "100x100", "125x125", "200x200"]

        self.settings_label = customtkinter.CTkLabel(self, text="Settings", font=('Roboto', 36))
        self.settings_label.pack(padx=10, pady=(50, 10), side='top', anchor='nw')

        self.drop_downs_frame = customtkinter.CTkFrame(self, fg_color='white')
        self.drop_downs_frame.pack(fill='both', expand=True)

        self.icon_size_drop_down = DefaultDropDown(self.drop_downs_frame, label_text="Image Preview Size",
                                                   values=self.all_icon_sizes, command=self.on_icon_change)
        self.icon_size_drop_down.pack(anchor='w')
        # Set saved icon size or default
        self.icon_size_drop_down.set(f"{settings.get_setting('icon_width', 50)}x"
                                     f"{settings.get_setting('icon_height', 50)}")

    @staticmethod
    def on_icon_change(choice):
        icon_size = choice.split("x")
        settings.add_setting("icon_width", icon_size[0])
        settings.add_setting("icon_height", icon_size[1])
