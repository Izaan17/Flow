import tkinter as tk

import customtkinter


class ErrorPopup:
    def __init__(self, master, message, delay=5000):
        self.root = master
        self.delay = delay

        self.popup_frame = customtkinter.CTkFrame(self.root, fg_color='red', corner_radius=10)
        self.popup_frame.place(relx=0.5, rely=-1, anchor=tk.N)

        self.message_label = customtkinter.CTkLabel(self.popup_frame, text=message)
        self.message_label.pack(padx=10, pady=5)

        self.slide_down()

    def slide_down(self):
        self.popup_frame.place_configure(rely=0)
        self.popup_frame.after(self.delay, self.slide_up)

    def slide_up(self):
        self.popup_frame.destroy()


if __name__ == '__main__':
    # Example usage:
    root = tk.Tk()
    root.geometry("400x300")
    root.title("Error Popup Example")
    ErrorPopup(root, "This is an error message.")
    root.mainloop()
