import tkinter as tk

import customtkinter


class Popup:
    def __init__(self, master, message, delay=5000, fg_color='transparent'):
        self.root = master
        self.delay = delay

        self.popup_frame = customtkinter.CTkFrame(self.root, fg_color=fg_color, corner_radius=10)
        self.popup_frame.place(relx=0.5, rely=-1, anchor=tk.N)

        self.message_label = customtkinter.CTkLabel(self.popup_frame, text=message, text_color='white')
        self.message_label.pack(padx=10, pady=5)

        self.slide_down()

    def slide_down(self):
        self.popup_frame.place_configure(rely=0)
        self.popup_frame.after(self.delay, self.slide_up)

    def slide_up(self):
        self.popup_frame.destroy()


class ErrorPopup(Popup):
    def __init__(self, master, message, delay=5000):
        super().__init__(master, message, delay=delay, fg_color='red')


class SuccessPopup(Popup):
    def __init__(self, master, message, delay=5000):
        super().__init__(master, message, delay=delay, fg_color='green')


if __name__ == '__main__':
    # Example usage:
    root = tk.Tk()
    root.geometry("400x300")
    root.title("Error Popup Example")
    ErrorPopup(root, "This is an error message.")
    root.mainloop()
