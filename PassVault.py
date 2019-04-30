"""Password vault app"""
import tkinter as tk
import gui_3_0 as g3
import gui_2_3 as g2
import gui_god as gg


class MainApp(tk.Tk):
    """Password vault app main frame"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.app_data = {"account": tk.StringVar(), "key": tk.StringVar()}
        for app_fram in (g3.Login, g2.Main, gg.God):
            page_name = app_fram.__name__
            frame = app_fram(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")
        self.title("Password Vault")
        self.geometry("820x550")
        self.resizable(False, False)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        # print(self.frames, "here")
        frame = self.frames[page_name]

        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")


APP = MainApp()
APP.mainloop()
