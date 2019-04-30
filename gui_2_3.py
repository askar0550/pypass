"""Third time lucky"""
import tkinter as tk
import database2
# from gui_3_0 import Login

class Main(tk.Frame):
    """Main app screen"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=805, height=550, bg="#000c18", padx=10)
        self.controller = controller
        container = tk.Frame(self)
        #container.grid_rowconfigure(0, weight=1)
        #container.grid_columnconfigure(0, weight=1)
        container.grid()
        self.top_widgets(container, controller)
        self.left_widgets(container)
        self.centre_widgets(container)
        self.right_widgets(container)
        self.bottom_widgets(container)
        self.bind("<<ShowFrame>>", self.updaterr)



    @classmethod
    def create(cls):
        """On Create button click."""
        cls.message_label['fg'] = "red"
        cls.left_frame['highlightbackground'] = 'red'
        cls.left_frame['highlightcolor'] = 'red'
        cls.left_frame['highlightthickness'] = 0
        if not cls.left_hostentry.get():
            cls.message_label['text'] = "Please complete the Host field!"
            cls.left_frame['highlightthickness'] = 1
            cls.left_frame.after(1500, Main.leftframeborderoff)
            cls.message_label.after(2500, Main.messagecleanner)
            return
        else:
            lhost_2 = cls.left_hostentry.get()
        if not cls.left_identry.get():
            cls.message_label['text'] = "Please complete the ID field!"
            cls.left_frame['highlightthickness'] = 1
            cls.left_frame.after(1500, Main.leftframeborderoff)
            cls.message_label.after(2500, Main.messagecleanner)
            return
        else:
            lid_2 = cls.left_identry.get()

        if not cls.left_passentry.get():
            cls.message_label['text'] = "Please complete the Password field!"
            cls.left_frame['highlightthickness'] = 1
            cls.left_frame.after(1500, Main.leftframeborderoff)
            cls.message_label.after(2500, Main.messagecleanner)
            return
        else:
            lpass_2 = cls.left_passentry.get()

        cls.acc = format(cls.controller.app_data["account"].get())
        user = database2.Db02(cls.acc, lhost_2, lid_2, lpass_2, cls.pss)
        if user.usercheck() == 0:
            cls.message_label['fg'] = "green"
            cls.message_label['text'] = "Password saved! " + user.write()
            Main.updatehost()
        else:
            cls.message_label['fg'] = "green"
            cls.message_label['text'] = "Already saved, proceed to the dark side!"
        cls.message_label.after(1500, Main.messagecleanner)

    @classmethod
    def leftframeborderoff(cls):
        """Cleans left frame error format"""
        cls.left_frame['highlightthickness'] = 0
    @classmethod
    def rightframeborderoff(cls):
        """Cleans left frame error format"""
        cls.right_frame['highlightthickness'] = 0


    @classmethod
    def messagecleanner(cls):
        """Cleans bottom message label"""
        cls.message_label['text'] = " "
        cls.message_label['fg'] = "green"
    @classmethod
    def changedhost(cls, *args):
        """Host selection event."""
        # MESSAGELABEL['text'] = VAR1.get()
        Main.timeclean()
        new_host = cls.var_1.get()
        Main.accountlistupdate(new_host)

    @classmethod
    def updatehost(cls):
        """Updates the lists after adding new account"""
        cls.var_1.set('')
        cls.right_hostentry['menu'].delete(0, 'end')

        # Insert list of new options (tk._setit hooks them up to var)
        new_choices = cls.temp.hosts()
        for choice in new_choices:
            cls.right_hostentry['menu'].add_command(label=choice, \
            command=tk._setit(cls.var_1, choice, Main.changedhost))
        try:
            cls.var_1.set(new_choices[0])
        except IndexError:
            cls.var_1.set('None')
        Main.changedhost()
    @classmethod
    def accountlistupdate(cls, neww_hhost):
        """Update the user id dropdown on any event"""
        try:
            cls.var_2.set('')
            cls.right_identry['menu'].delete(0, 'end')
            new_choices = cls.temp.accounts(neww_hhost)
            for choice in new_choices:
                cls.right_identry['menu'].add_command(label=choice, \
                command=tk._setit(cls.var_2, choice, Main.timeclean))
            cls.var_2.set(new_choices[0])
            # Main.timeclean()
        except IndexError:
            cls.var_2.set('None')
        # Main.timeclean()
    @classmethod
    def lout(cls):
        """Go to Login"""
        Main.controller.show_frame("Login")
    @classmethod
    def updaterr(cls, event):
        """Update label"""
        # print(event)

        cls.user_label["text"] = "user: " + cls.controller.app_data["account"].get()
        cls.acc = format(cls.controller.app_data["account"].get())
        # print(cls.controller.app_data)
        cls.pss = format(cls.controller.app_data["key"].get())

        cls.temp = database2.Db02(cls.acc, "2", "3", "4", cls.pss)
        # cls.list_1 = temp.hosts()
        # cls.var_1.set(cls.list_1[0])
        cls.left_hostentry.delete(0, 'end')
        cls.left_identry.delete(0, 'end')
        cls.left_passentry.delete(0, 'end')
        cls.entry_text.set("")
        Main.updatehost()
    @classmethod
    def get(cls):
        """GET"""
        host = cls.var_1.get()
        usid = cls.var_2.get()
        temp = database2.Db02(cls.acc, host, usid, "", cls.pss)
        cls.entry_text.set(temp.readd())
        cls.right_passentry["show"] = ""
        cls.message_label.after(3500, Main.hidepassword)
        cls.right_timelabel["text"] = "Active sice: " + temp.datefind()
        cls.right_timeactive["text"] = format(int(temp.datediff())) + " days"

    @classmethod
    def remove(cls):
        """Remove from vault"""
        host = cls.var_1.get()
        usid = cls.var_2.get()
        temp = database2.Db02(cls.acc, host, usid, "", cls.pss)

        if temp.deleterow():
            cls.message_label['fg'] = "green"
            cls.message_label['text'] = "Password removed!"
            Main.updatehost()
        else:
            cls.message_label['fg'] = "red"
            cls.message_label['text'] = "Something went wrong, dont's ask why!!!"
            cls.right_frame['highlightthickness'] = 1
            cls.right_frame.after(1500, Main.rightframeborderoff)
        Main.updatehost()
        cls.entry_text.set("")
        cls.message_label.after(1500, Main.messagecleanner)

    @classmethod
    def update(cls):
        """Update from vault"""
        if not cls.entry_text.get():
            cls.message_label['text'] = "Insert the new password!"
            cls.right_frame['highlightthickness'] = 1
            cls.right_frame.after(1500, Main.rightframeborderoff)
            cls.message_label.after(2500, Main.messagecleanner)
            return
        else:
            rkey_3 = cls.entry_text.get()

        host = cls.var_1.get()
        usid = cls.var_2.get()
        temp = database2.Db02(cls.acc, host, usid, rkey_3, cls.pss)

        if temp.updatepss():
            cls.message_label['fg'] = "green"
            cls.message_label['text'] = "Password has been updated."

        else:
            cls.message_label['fg'] = "red"
            cls.message_label['text'] = "Gone fishing :)"
            cls.right_frame['highlightthickness'] = 1
            cls.right_frame.after(1500, Main.rightframeborderoff)
        Main.timeclean()
        cls.message_label.after(1500, Main.messagecleanner)

    @classmethod
    def hidepassword(cls):
        """Hide password after 5 seconds"""
        cls.right_passentry["show"] = "*"
        cls.message_label['fg'] = "green"
        cls.message_label['text'] = "Password hidded!"
        cls.message_label.after(2000, Main.messagecleanner)

    @classmethod
    def timeclean(cls, *args):
        """Time stamps"""
        cls.right_timelabel["text"] = ""
        cls.right_timeactive["text"] = ""
        cls.entry_text.set("")

    # @classmethod
    # def print_it(cls):
    #     return Login.controller.app_data["account"].get()

    @classmethod
    def top_widgets(cls, parent, controller):
        """Top things"""
        cls.controller = controller
        top_frame = tk.Frame(parent, width=800, height=90, bg="#000c18")
        top_frame.grid(row=0, columnspan=3, sticky="news")
        top_frame.grid_propagate(0)
        top_frame.grid_rowconfigure(0, weight=1)
        top_frame.grid_columnconfigure(0, weight=1)
        title_label = tk.Label(top_frame, text="Password Vault", fg="white",\
        font=("Helvetica", 24), bg="#000c18")
        title_label.grid(row=0)
        l_button = tk.Button(top_frame, activebackground="#000c18",\
         bg="#000c18", font=("Helvetica", 8, "bold"), fg="grey",\
          borderwidth=0, text="logout", command=Main.lout\
          , cursor="pirate")
        l_button.grid(row=0, sticky='ne', pady=(5, 0))
        cls.user_label = tk.Label(top_frame, fg="grey",\
        font=("Helvetica", 8), bg="#000c18")
        cls.user_label["text"] = ""
        cls.user_label.grid(row=0, sticky='nw', pady=(5, 0))

    @classmethod
    def left_widgets(cls, parent):
        """Left stuff"""
        cls.left_frame = tk.Frame(parent, width=399, height=400, bg="#000c18")
        cls.left_frame.grid(row=1, column=0, sticky="nsw")
        cls.left_frame.grid_propagate(0)
        left_subtitle = tk.Label(cls.left_frame, text="Add Password", fg="white",\
        font=("Helvetica", 18), bg="#000c18")
        left_hostlabel = tk.Label(cls.left_frame, text="Host", fg="white",\
        font=("Helvetica", 14), bg="#000c18")
        left_idlabel = tk.Label(cls.left_frame, text="User ID", fg="white",\
        font=("Helvetica", 14), bg="#000c18")
        left_passlabel = tk.Label(cls.left_frame, text="Password", fg="white",\
        font=("Helvetica", 14), bg="#000c18")
        cls.left_hostentry = tk.Entry(cls.left_frame, text="host2", bg="grey",\
        font=("Helvetica", 10, "bold"), fg="#000c18", width=30)
        cls.left_identry = tk.Entry(cls.left_frame, text="ID2", bg="grey",\
        font=("Helvetica", 10, "bold"), fg="#000c18", width=30)
        cls.left_passentry = tk.Entry(cls.left_frame, text="Password2", show="*", bg="grey",\
        font=("Helvetica", 10, "bold"), fg="#000c18", width=30)
        left_image = tk.PhotoImage(file=".\\imgs\\button_create.png")

        # LIMG = LIMG.subsample(10)
        left_button = tk.Button(cls.left_frame, activebackground="#000c18",\
         bg="#000c18", font=("Helvetica", 16, "bold"), fg="#000c18",\
          image=left_image, borderwidth=0, command=Main.create)
        left_button.image = left_image
        # Layout left Widgets
        left_subtitle.grid(row=0, column=0, columnspan=2, sticky="n", pady=(10, 50))
        left_hostlabel.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        cls.left_hostentry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        left_idlabel.grid(row=4, column=0, sticky="e", padx=5, pady=5)
        cls.left_identry.grid(row=4, column=1, sticky="w", padx=10, pady=5)
        left_passlabel.grid(row=5, column=0, sticky="e", padx=5, pady=5)
        cls.left_passentry.grid(row=5, column=1, sticky="w", padx=10, pady=5)
        left_button.grid(row=6, column=0, columnspan=2, sticky="n", pady=(70, 0))

    @classmethod
    def centre_widgets(cls, parent):
        """Centre bar"""
        centre_frame = tk.Frame(parent, width=2, height=400, bg="#36454F")
        centre_frame.grid(row=1, column=1, sticky="nsew")

    @classmethod
    def right_widgets(cls, parent):
        """Right stuf"""
        cls.right_frame = tk.Frame(parent, width=399, height=400, bg="#000c18")
        cls.right_frame.grid(row=1, column=2, sticky="news")
        cls.right_frame.grid_propagate(0)
        cls.right_timelabel = tk.Label(cls.right_frame, text="", fg="grey",\
        font=("Helvetica", 8), bg="#000c18", wraplength=100)
        cls.right_timeactive = tk.Label(cls.right_frame, text="", fg="green",\
        font=("Helvetica", 8), bg="#000c18")
        cls.entry_text = tk.StringVar()
        user_config = database2.Db02("1", "2", "3", "4", "5")
        if not user_config.hosts():
            cls.list_1 = ["None"]
        else:
            cls.list_1 = user_config.hosts()

        cls.var_1 = tk.StringVar()
        cls.var_1.set(cls.list_1[0])
        cls.right_hostentry = tk.OptionMenu(cls.right_frame, cls.var_1, *cls.list_1)
        cls.right_hostentry["menu"].config(bg="grey",\
        font=("Helvetica", 10, "bold"), fg="#000c18", activebackground="black")
        cls.right_hostentry.config(bg="grey",\
        font=("Helvetica", 10, "bold"), fg="#000c18", width=25, borderwidth=0,\
        highlightbackground="#000c18", highlightthickness=0)
        if not user_config.accounts(cls.list_1[0]):
            cls.list_2 = ["None"]
        else:
            cls.list_2 = user_config.accounts(cls.list_1[0])
        cls.var_2 = tk.StringVar()
        cls.var_2.set(cls.list_2[0])
        cls.right_identry = tk.OptionMenu(cls.right_frame, cls.var_2, *cls.list_2,\
         command=Main.timeclean())
        cls.right_identry["menu"].config(bg="grey",\
        font=("Helvetica", 10, "bold"), fg="#000c18", activebackground="black")
        cls.right_identry.config(bg="grey",\
        font=("Helvetica", 10, "bold"), fg="#000c18", width=25, borderwidth=0,\
        highlightbackground="#000c18", highlightthickness=0)
        right_subtitle = tk.Label(cls.right_frame, text="Retrieve Password", fg="white",\
        font=("Helvetica", 18), bg="#000c18")
        right_hostlabel = tk.Label(cls.right_frame, text="Host", fg="white",\
        font=("Helvetica", 14), bg="#000c18")
        right_idlabel = tk.Label(cls.right_frame, text="User ID", fg="white",\
        font=("Helvetica", 14), bg="#000c18")
        right_passlabel = tk.Label(cls.right_frame, text="Password", fg="white",\
        font=("Helvetica", 14), bg="#000c18")

        cls.right_passentry = tk.Entry(cls.right_frame, textvariable=cls.entry_text, bg="grey",\
        font=("Helvetica", 10, "bold"), show="*", fg="#000c18", width=30,\
        readonlybackground="grey")
        right_getimg = tk.PhotoImage(file=".\\imgs\\button_get.png")
        right_getbutton = tk.Button(cls.right_frame, text="Get", activebackground="#000c18",\
         bg="#000c18", command=Main.get, \
        font=("Helvetica", 16, "bold"), fg="#000c18", image=right_getimg, borderwidth=0)
        right_getbutton.image = right_getimg
        right_upimg = tk.PhotoImage(file=".\\imgs\\button_update.png")
        right_upbutton = tk.Button(cls.right_frame, text="Update", activebackground="#000c18",\
         bg="#000c18", command=Main.update, \
        font=("Helvetica", 16, "bold"), fg="#000c18", image=right_upimg, borderwidth=0)
        right_upbutton.image = right_upimg
        right_removeimg = tk.PhotoImage(file=".\\imgs\\button_remove.png")
        right_removebutton = tk.Button(cls.right_frame, text="Remove", activebackground="#000c18",\
         bg="#000c18", command=Main.remove, \
        font=("Helvetica", 16, "bold"), fg="#000c18", image=right_removeimg, borderwidth=0)
        right_removebutton.image = right_removeimg

        # Layout Right Widgets
        right_subtitle.grid(row=0, column=0, columnspan=2, sticky="n", pady=(10, 50), padx=(90))
        right_hostlabel.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        right_idlabel.grid(row=4, column=0, sticky="e", padx=5, pady=5)
        cls.right_hostentry.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        cls.right_identry.grid(row=4, column=1, sticky="w", padx=10, pady=5)
        right_passlabel.grid(row=5, column=0, sticky="e", padx=5, pady=5)
        cls.right_passentry.grid(row=5, column=1, sticky="w", padx=10, pady=5)
        right_getbutton.grid(row=6, column=0, sticky="n", pady=(70, 0))
        right_upbutton.grid(row=6, column=1, sticky="ne", pady=(70, 0))
        right_removebutton.grid(row=6, columnspan=2, sticky="n", pady=(70, 0))
        cls.right_timelabel.grid(row=7, column=0, sticky="w", pady=(30, 0), padx=10)
        cls.right_timeactive.grid(row=7, column=1, sticky="e", pady=(30, 0))

    @classmethod
    def bottom_widgets(cls, parent):
        """Bottom messages"""
        bottom_frame = tk.Frame(parent, width=800, height=60, bg="#000c18")
        bottom_frame.grid(row=2, columnspan=3, sticky="ew")
        bottom_frame.grid_propagate(0)
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)
        cls.message_label = tk.Label(bottom_frame, text="", fg="green",\
        font=("Helvetica", 20), bg="#000c18")
        cls.message_label.grid(sticky='news')
        cls.message_label['fg'] = "green"
        cls.message_label['text'] = "Welcome!"
        cls.message_label.after(2500, Main.messagecleanner)
