"""Third time lucky"""
import tkinter as tk
import database3
# from gui_3_0 import Login

class God(tk.Frame):
    """God app screen"""
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
        if not cls.left_accentry.get():
            cls.message_label['text'] = "Please complete the Account field!"
            cls.left_frame['highlightthickness'] = 1
            cls.left_frame.after(1500, God.leftframeborderoff)
            cls.message_label.after(2500, God.messagecleanner)
            return
        else:
            lhost_2 = cls.left_accentry.get()


        if not cls.left_passentry.get():
            cls.message_label['text'] = "Please complete the Password field!"
            cls.left_frame['highlightthickness'] = 1
            cls.left_frame.after(1500, God.leftframeborderoff)
            cls.message_label.after(2500, God.messagecleanner)
            return
        else:
            lpass_2 = cls.left_passentry.get()

        # cls.acc = format(cls.controller.print_it())
        user = database3.Db03(lhost_2, lpass_2)
        cls.message_label['text'] = user.adduser()
        if cls.message_label['text'] == "User created!":
            cls.message_label.after(2500, God.messagecleanner)
            # cls.message_label.after(1500, Login.swittch)
        else:
            cls.message_label['text'] = "User already exists!"
            cls.message_label.after(2500, God.messagecleanner)
        cls.message_label.after(1500, God.messagecleanner)

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
    def changedacc(cls, *args):
        """Host selection event."""
        # MESSAGELABEL['text'] = VAR1.get()
        God.timeclean()
        new_host = cls.var_1.get()


    @classmethod
    def updateacc(cls):
        """Updates the lists after adding new account"""
        cls.var_1.set('')
        cls.right_accentry['menu'].delete(0, 'end')

        # Insert list of new options (tk._setit hooks them up to var)
        temp = database3.Db03("", "")
        new_choices = temp.accounts()
        for choice in new_choices:
            cls.right_accentry['menu'].add_command(label=choice, \
            command=tk._setit(cls.var_1, choice, God.changedacc))
        try:
            cls.var_1.set(new_choices[0])
        except IndexError:
            cls.var_1.set('None')
        God.changedacc()

    @classmethod
    def lout(cls):
        """Go to Login"""
        God.controller.show_frame("Login")
    @classmethod
    def updaterr(cls, event):
        """Update label"""
        print(event)

        cls.user_label["text"] = "user: " +\
         cls.controller.app_data["account"].get()

        # cls.list_1 = temp.hosts()
        # cls.var_1.set(cls.list_1[0])
        cls.left_accentry.delete(0, 'end')

        cls.left_passentry.delete(0, 'end')
        cls.entry_text.set("")
        God.updateacc()
    @classmethod
    def gettime(cls, acc, pss):
        """Get account timespan"""
        temp = database3.Db03(acc, pss)
        cls.right_timelabel["text"] = "Active sice: " + temp.datefind()
        cls.right_timeactive["text"] = format(int(temp.datediff())) + " days"

    @classmethod
    def print_it(cls):
        return Login.controller.app_data["account"].get()

    @classmethod
    def remove(cls):
        """Remove from vault"""
        acc = cls.var_1.get()
        temp = database3.Db03(acc, "")
        if temp.deleterow():
            cls.message_label['fg'] = "green"
            cls.message_label['text'] = "Password removed!"
            God.updateacc()
        else:
            cls.message_label['fg'] = "red"
            cls.message_label['text'] = "Something went wrong, dont's ask why!!!"
            cls.right_frame['highlightthickness'] = 1
            cls.right_frame.after(1500, God.rightframeborderoff)
        God.updateacc()
        cls.entry_text.set("")
        cls.message_label.after(1500, God.messagecleanner)


    @classmethod
    def hidepassword(cls):
        """Hide password after 5 seconds"""
        cls.right_passentry["show"] = "*"
        cls.message_label['fg'] = "green"
        cls.message_label['text'] = "Password hidded!"
        cls.message_label.after(2000, God.messagecleanner)

    @classmethod
    def timeclean(cls, *args):
        """Time stamps"""
        cls.right_timelabel["text"] = ""
        cls.right_timeactive["text"] = ""
        cls.entry_text.set("")

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
          borderwidth=0, text="logout", command=God.lout\
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

        left_subtitle = tk.Label(cls.left_frame, text="Add Account", fg="white",\
        font=("Helvetica", 18), bg="#000c18")
        left_acclabel = tk.Label(cls.left_frame, text="Account", fg="white",\
        font=("Helvetica", 14), bg="#000c18")
        left_passlabel = tk.Label(cls.left_frame, text="Password", fg="white",\
        font=("Helvetica", 14), bg="#000c18")
        cls.left_accentry = tk.Entry(cls.left_frame, bg="grey",\
        font=("Helvetica", 10, "bold"), fg="#000c18", width=30)
        cls.left_passentry = tk.Entry(cls.left_frame, show="*", bg="grey",\
        font=("Helvetica", 10, "bold"), fg="#000c18", width=30)

        left_image = tk.PhotoImage(file=".\\imgs\\button_create.png")

        left_button = tk.Button(cls.left_frame, activebackground="#000c18",\
         bg="#000c18", font=("Helvetica", 16, "bold"), fg="#000c18",\
          image=left_image, borderwidth=0, command=God.create)
        left_button.image = left_image
        # Layout left Widgets
        left_subtitle.grid(row=0, column=0, columnspan=2, sticky="n", pady=(10, 100))
        left_acclabel.grid(row=1, column=0, sticky="e", padx=(25, 5), pady=5)
        cls.left_accentry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        left_passlabel.grid(row=2, column=0, sticky="e", padx=(25, 5), pady=5)
        cls.left_passentry.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        left_button.grid(row=3, column=0, columnspan=2, sticky="n", pady=(70, 0))

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
        user_config = database3.Db03("1", "2")
        if not user_config.accounts():
            cls.list_1 = ["None"]
        else:
            cls.list_1 = user_config.accounts()
        cls.var_1 = tk.StringVar()
        cls.var_1.set(cls.list_1[0])
        cls.right_accentry = tk.OptionMenu(cls.right_frame, cls.var_1, *cls.list_1)
        cls.right_accentry["menu"].config(bg="grey",\
        font=("Helvetica", 10, "bold"), fg="#000c18", activebackground="black")
        cls.right_accentry.config(bg="grey",\
        font=("Helvetica", 10, "bold"), fg="#000c18", width=25, borderwidth=0,\
        highlightbackground="#000c18", highlightthickness=0)
        right_subtitle = tk.Label(cls.right_frame, text="Admin Accounts", fg="white",\
        font=("Helvetica", 18), bg="#000c18")
        right_acclabel = tk.Label(cls.right_frame, text="Acounts", fg="white",\
        font=("Helvetica", 14), bg="#000c18")


        right_removeimg = tk.PhotoImage(file=".\\imgs\\button_remove.png")
        right_removebutton = tk.Button(cls.right_frame, text="Remove", activebackground="#000c18",\
         bg="#000c18", command=God.remove, \
        font=("Helvetica", 16, "bold"), fg="#000c18", image=right_removeimg, borderwidth=0)
        right_removebutton.image = right_removeimg
        # Layout Right Widgets
        right_subtitle.grid(row=0, column=0, columnspan=2, sticky="n", pady=(10, 100), padx=(90))
        right_acclabel.grid(row=1, column=0, sticky="e", padx=(25, 5), pady=5)
        cls.right_accentry.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        right_removebutton.grid(row=3, columnspan=2, sticky="we", pady=(110, 0))
        cls.right_timelabel.grid(row=4, column=0, sticky="w", pady=(30, 0), padx=10)
        cls.right_timeactive.grid(row=4, column=1, sticky="e", pady=(30, 0))

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
        cls.message_label.after(2500, God.messagecleanner)
