import customtkinter


class UtilitySection(customtkinter.CTkFrame):
    def __init__(self, master, section_title, section_subtitle="", icon=None, **kwargs):
        super().__init__(master, **kwargs)
        self.section_title = customtkinter.CTkLabel(self, text=section_title,
                                                    font=('Roboto', 24, 'bold'), image=icon,
                                                    compound='left')
        self.section_title.pack()
        self.section_subtitle = customtkinter.CTkLabel(self, text=section_subtitle,
                                                       font=('Roboto', 16))
        self.section_subtitle.pack()
