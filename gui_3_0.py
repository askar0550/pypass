"""Stopped counting at 3 :)))"""
import tkinter as tk
import database


class Login(tk.Frame):
    """Main app screen"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=805, height=550, bg="#000c18", padx=10)
        self.controller = controller
        container = tk.Frame(self)
        #container.grid_rowconfigure(0, weight=1)
        #container.grid_columnconfigure(0, weight=1)
        self.lid_2 = ""
        container.grid()
        self.top_widgets(container)
        self.centre1_widgets(container)
        self.centre2_widgets(container, controller)
        self.bottom_widgets(container)
        self.bind("<<ShowFrame>>", self.updaterr)
        Login.connecction()

    @classmethod
    def updaterr(cls, event):
        """Update label"""
        cls.message_label['fg'] = "green"
        cls.account_entry.delete(0, 'end')
        cls.key_entry.delete(0, 'end')
        cls.user_label["text"] = ""
        print(event)

    @classmethod
    def opend(cls):
        """Checks and squares"""

        cls.message_label['fg'] = "red"
        cls.centre_frame2['highlightbackground'] = 'red'
        cls.centre_frame2['highlightcolor'] = 'red'
        cls.centre_frame2['highlightthickness'] = 0
        if not cls.account_entry.get():
            cls.message_label['text'] = "No account! Hey mister, leave the chest alone!."
            cls.centre_frame2['highlightthickness'] = 1
            cls.centre_frame2.after(1500, Login.frameborderoff)
            cls.message_label.after(2500, Login.messagecleanner)
            return
        else:
            cls.lid_2 = cls.account_entry.get()

        if not cls.key_entry.get():
            cls.message_label['text'] = "Haven't you forgot something?"
            cls.centre_frame2['highlightthickness'] = 1
            cls.centre_frame2.after(1500, Login.frameborderoff)
            cls.message_label.after(2500, Login.messagecleanner)
            return
        else:
            lkey_2 = cls.key_entry.get()
            cls.message_label['fg'] = "green"


        cls.connect = database.Db01(cls.lid_2, lkey_2)
        cls.message_label['text'] = cls.connect.checkuser()
        if cls.message_label['text'] == "Success!":
            cls.message_label.after(2500, Login.messagecleanner)
            cls.user_label["text"] = "user: " + format(cls.controller.app_data["account"].get())
            cls.message_label.after(1500, Login.swittch)
        else:
            cls.centre_frame2['highlightthickness'] = 1
            cls.centre_frame2.after(1500, Login.frameborderoff)

    @classmethod
    def opend2(cls):
        """Checks and create"""
        Login.connecction()
        cls.message_label['fg'] = "red"
        cls.centre_frame2['highlightbackground'] = 'red'
        cls.centre_frame2['highlightcolor'] = 'red'
        cls.centre_frame2['highlightthickness'] = 0
        if not cls.account_entry.get():
            cls.message_label['text'] = "No account! Hey mister, leave the chest alone!."
            cls.centre_frame2['highlightthickness'] = 1
            cls.centre_frame2.after(1500, Login.frameborderoff)
            cls.message_label.after(2500, Login.messagecleanner)
            return
        else:
            cls.lid_3 = cls.account_entry.get()

        if not cls.key_entry.get():
            cls.message_label['text'] = "Haven't you forgot something?"
            cls.centre_frame2['highlightthickness'] = 1
            cls.centre_frame2.after(1500, Login.frameborderoff)
            cls.message_label.after(2500, Login.messagecleanner)
            return
        else:
            lkey_2 = cls.key_entry.get()

        cls.connect = database.Db01(cls.lid_3, lkey_2)
        cls.message_label['text'] = cls.connect.adduser()
        if cls.message_label['text'] == "User created!":
            cls.message_label.after(2500, Login.messagecleanner)
            # cls.message_label.after(1500, Login.swittch)
        else:
            cls.message_label['text'] = "User already exists - Just Log in"
            cls.message_label.after(2500, Login.messagecleanner)


    @classmethod
    def frameborderoff(cls):
        """Cleans left frame error format"""
        cls.centre_frame2['highlightthickness'] = 0

    @classmethod
    def connecction(cls):
        """Database existance"""
        cls.connect = database.Db01("1", "2")
        if cls.connect.checker():
            cls.message_label["text"] = "Vault created!"
        else:
            cls.message_label["text"] = "Vault exists!"
        cls.message_label.after(1500, Login.messagecleanner)
        # cls.message_label.after(1500, Login.swittch)

    @classmethod
    def messagecleanner(cls):
        """Cleans bottom message label"""
        cls.message_label['text'] = " "
        cls.message_label['fg'] = "green"
    @classmethod
    def swittch(cls):
        """Go to Main"""
        if cls.connect.lvl == 0:
            Login.controller.show_frame("Main")
        elif cls.connect.lvl == 1:
            Login.controller.show_frame("God")
        else:
            cls.message_label["text"] = "Too wrong for this world!"
        # Login.controller.print_it()


    @classmethod
    def top_widgets(cls, parent):
        """Top stuff"""
        top_frame = tk.Frame(parent, width=800, height=90, bg="#000c18")
        top_frame.grid(row=0, columnspan=3, sticky="news")
        top_frame.grid_propagate(0)
        top_frame.grid_rowconfigure(0, weight=1)
        top_frame.grid_columnconfigure(0, weight=1)
        cls.title_label = tk.Label(top_frame, text="Password Vault", fg="white",\
        font=("Helvetica", 24), bg="#000c18")
        cls.title_label.grid()

        cls.user_label = tk.Label(top_frame, fg="grey",\
        font=("Helvetica", 8), bg="#000c18")
        cls.user_label["text"] = "" # + format(cls.app_data["account"].get())
        cls.user_label.grid(row=0, sticky='nw', pady=(5, 0))

    @classmethod
    def centre1_widgets(cls, parent):
        """Icon"""
        centre_frame1 = tk.Frame(parent, width=800, height=170, bg="#000c18")
        centre_frame1.grid(row=1)
        centre_frame1.grid_propagate(0)
        centre_frame1.grid_rowconfigure(0, weight=1)
        centre_frame1.grid_columnconfigure(0, weight=1)
        chest_img = tk.PhotoImage(file=".\\imgs\\chest.png")
        chest_img = chest_img.subsample(4)
        cls.img_label = tk.Label(centre_frame1, image=chest_img, bg="#000c18")
        cls.img_label.image = chest_img
        cls.img_label.grid()

    @classmethod
    def centre2_widgets(cls, parent, controller):
        """Credentials"""
        cls.controller = controller
        cls.centre_frame2 = tk.Frame(parent, width=800, height=230, bg="#000c18")
        cls.centre_frame2.grid(row=2, sticky="ew")
        cls.centre_frame2.grid_propagate(0)
        cls.account_label = tk.Label(cls.centre_frame2, text="Account", fg="white",\
        font=("Helvetica", 18), bg="#000c18")
        cls.key_label = tk.Label(cls.centre_frame2, text="Authorisation key", fg="white",\
        font=("Helvetica", 18), bg="#000c18")

        cls.account_entry = tk.Entry(cls.centre_frame2, bg="grey",\
        font=("Helvetica", 10, "bold"), fg="#000c18", width=30,\
         textvariable=cls.controller.app_data["account"])

        cls.key_entry = tk.Entry(cls.centre_frame2, bg="grey",\
        font=("Helvetica", 10, "bold"), fg="#000c18", width=30, show="*", \
        textvariable=cls.controller.app_data["key"])
        log_image = tk.PhotoImage(file=".\\imgs\\button_log.png")
        cls.log_button = tk.Button(cls.centre_frame2, text="Open", activebackground="#000c18",\
         bg="#000c18", command=Login.opend, \
        font=("Helvetica", 16, "bold"), fg="#000c18", image=log_image, borderwidth=0)

        sign_image = tk.PhotoImage(file=".\\imgs\\button_sign.png")
        cls.sign_button = tk.Button(cls.centre_frame2, text="Open", activebackground="#000c18",\
         bg="#000c18", command=Login.opend2, \
        font=("Helvetica", 16, "bold"), fg="#000c18", image=sign_image, borderwidth=0)

        cls.log_button.image = log_image
        cls.sign_button.image = sign_image

        cls.account_label.grid(row=1, column=0, sticky='e', pady=(20, 0), padx=(200, 10))
        cls.key_label.grid(row=2, column=0, sticky='e', pady=(0, 10), padx=(200, 10))
        cls.account_entry.grid(row=1, column=1, sticky='w', pady=(20, 0))
        cls.key_entry.grid(row=2, column=1, sticky='w', pady=(0, 10))
        cls.log_button.grid(row=3, column=0, sticky='e', pady=(50, 20), padx=(200, 10))
        cls.sign_button.grid(row=3, column=1, sticky='w', pady=(50, 20), padx=(0, 10))


    @classmethod
    def bottom_widgets(cls, parent):
        """Messages"""
        bottom_frame = tk.Frame(parent, width=800, height=60, bg="#000c18")
        bottom_frame.grid(row=3, columnspan=3, sticky="ew")
        bottom_frame.grid_propagate(0)
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=1)
        cls.message_label = tk.Label(bottom_frame, text="", fg="green",\
        font=("Helvetica", 20), bg="#000c18")
        cls.message_label.grid(sticky='news')
        cls.message_label['fg'] = "green"
        cls.message_label['text'] = "Ola!"
        cls.message_label.after(1500, Login.messagecleanner)
