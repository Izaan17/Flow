import customtkinter

from utils.settings import settings
from widgets.Dropdown import DefaultDropDown
from widgets.Page import Page


class SettingsPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, fg_color='white')

        self.all_icon_sizes = ["24x24", "50x50", "100x100", "100x125", "125x100", "125x125", "200x200"]

        self.settings_label = customtkinter.CTkLabel(self, text="Settings", font=('Roboto', 36))
        self.settings_label.pack(padx=10, pady=(50, 10), side='top', anchor='nw')

        self.drop_downs_frame = customtkinter.CTkFrame(self, fg_color='white')
        self.drop_downs_frame.pack(fill='both', expand=True)

        self.max_items_per_row = DefaultDropDown(self.drop_downs_frame,
                                                 label_text="Max Items Per Row",
                                                 values=[str(i) for i in range(5, 11)], command=self.on_max_row_change)
        self.max_items_per_row.pack(anchor='w')
        self.max_items_per_row.set(settings.get_setting("max_items_per_row", 5))

        self.max_text_length = DefaultDropDown(self.drop_downs_frame,
                                               label_text="Max Text Length",
                                               values=[str(i) for i in range(10, 50)],
                                               command=self.on_text_length_change)
        self.max_text_length.pack(anchor='w')
        self.max_text_length.set(settings.get_setting("max_text_length", 30))

        self.show_image_preview = DefaultDropDown(self.drop_downs_frame,
                                                  label_text="Show Image Preview",
                                                  values=["True", "False"], command=self.on_img_preview_change)
        self.show_image_preview.pack(anchor='w')
        self.show_image_preview.set(settings.get_setting("show_img_preview", "True"))

        self.icon_size_drop_down = DefaultDropDown(self.drop_downs_frame, label_text="Icon Size",
                                                   values=self.all_icon_sizes, command=self.on_icon_change)
        self.icon_size_drop_down.pack(anchor='w')
        # Set saved icon size or default
        self.icon_size_drop_down.set(f"{settings.get_setting('icon_width', 50)}x"
                                     f"{settings.get_setting('icon_height', 50)}")

        self.allow_full_directory_deletion = DefaultDropDown(self.drop_downs_frame,
                                                             label_text="Full Directory Deletion",
                                                             values=["True", "False"], command=self.on_dir_delete)
        self.allow_full_directory_deletion.pack(anchor='w')
        self.allow_full_directory_deletion.set(settings.get_setting("allow_full_dir_deletion", "False"))

    @staticmethod
    def on_icon_change(choice):
        icon_size = choice.split("x")
        settings.add_setting("icon_width", icon_size[0])
        settings.add_setting("icon_height", icon_size[1])

    @staticmethod
    def on_dir_delete(choice):
        settings.add_setting("allow_full_dir_deletion", choice)

    @staticmethod
    def on_img_preview_change(choice):
        settings.add_setting("show_img_preview", choice)

    @staticmethod
    def on_max_row_change(choice):
        settings.add_setting("max_items_per_row", choice)

    @staticmethod
    def on_text_length_change(choice):
        settings.add_setting("max_text_length", choice)