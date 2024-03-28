import customtkinter


class MenuButton(customtkinter.CTkButton):
    def __init__(self, master, icon_image, text, button_width=25, *args, **kwargs):
        super().__init__(master, image=icon_image, text=text, width=button_width, fg_color='transparent',
                         hover_color=None, corner_radius=0, compound=customtkinter.TOP, *args, **kwargs)
