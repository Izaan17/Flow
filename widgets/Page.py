import customtkinter


class Page(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        customtkinter.CTkFrame.__init__(self, *args, **kwargs, corner_radius=0)

    def show(self):
        self.lift()
