"""provides FontWm class"""
from tkinter import IntVar, Listbox, StringVar, Toplevel, font, ttk
from tkinter.constants import END


class FontWm(Toplevel):
    """Font window"""

    def __init__(self, my_font=None):
        Toplevel.__init__(self)
        self.mainfont = my_font
        self.title("Font ...")

        self.result = None
        self.var = StringVar()  # For Font Face
        self.var.set(self.mainfont.actual("family"))
        self.var1 = IntVar()  # for Font Size
        self.var1.set(self.mainfont.actual("size"))
        self.var2 = StringVar()  # For Bold
        self.var2.set(self.mainfont.actual("weight"))
        self.var3 = StringVar()  # For Italic
        self.var3.set(self.mainfont.actual("slant"))
        self.var4 = IntVar()  # For Underline
        self.var4.set(self.mainfont.actual("underline"))
        self.var5 = IntVar()  # For Overstrike
        self.var5.set(self.mainfont.actual("overstrike"))
        self.font_1 = font.Font()
        for i in ["family", "weight", "slant", "overstrike", "underline", "size"]:
            self.font_1[i] = self.mainfont.actual(i)

        self.main_window = ttk.Frame(self)
        self.main_window.pack(padx=10, pady=10)

        self.main_frame = ttk.Frame(self.main_window)
        self.main_frame.pack(side="top", ipady=30, ipadx=30, expand="no", fill="both")
        self.main_frame_0 = ttk.Frame(self.main_window)
        self.main_frame_0.pack(side="top", expand="yes", fill="x", padx=10, pady=10)
        self.main_frame_1 = ttk.Frame(self.main_window)
        self.main_frame_1.pack(side="top", expand="no", fill="both")
        self.main_frame_2 = ttk.Frame(self.main_window)
        self.main_frame_2.pack(side="top", expand="yes", fill="x", padx=10, pady=10)
        # Frame in [  main frame]
        self.frame = ttk.LabelFrame(self.main_frame, text="Select Font Face")
        self.frame.pack(side="left", padx=10, pady=10, ipadx=20, ipady=20, expand="yes", fill="both")
        self.frame_1 = ttk.LabelFrame(self.main_frame, text="Select Font size")
        self.frame_1.pack(side="left", padx=10, pady=10, ipadx=20, ipady=20, expand="yes", fill="both")
        self.fam_ent = ttk.Entry(self.frame, textvariable=self.var)
        self.fam_ent.pack(side="top", padx=5, pady=5, expand="yes", fill="x")
        self.listbox = Listbox(self.frame, bg="gray70")
        self.listbox.pack(side="top", padx=5, pady=5, expand="yes", fill="both")
        fams = list(font.families())
        fams.sort()
        for i in fams:
            self.listbox.insert(END, i)

        # Frame in [ 0. mainframe]
        self.bold = ttk.Checkbutton(
            self.main_frame_0,
            text="Bold",
            onvalue="bold",
            offvalue="normal",
            variable=self.var2,
            command=self.checkstyle,
        )
        self.bold.pack(side="left", expand="yes", fill="x")
        self.italic = ttk.Checkbutton(
            self.main_frame_0,
            text="Italic",
            onvalue="italic",
            offvalue="roman",
            variable=self.var3,
            command=self.checkstyle,
        )
        self.italic.pack(side="left", expand="yes", fill="x")
        self.underline = ttk.Checkbutton(
            self.main_frame_0, text="Underline", onvalue=1, offvalue=0, variable=self.var4, command=self.checkstyle
        )
        self.underline.pack(side="left", expand="yes", fill="x")
        self.overstrike = ttk.Checkbutton(
            self.main_frame_0, text="Overstrike", onvalue=1, offvalue=0, variable=self.var5, command=self.checkstyle
        )
        self.overstrike.pack(side="left", expand="yes", fill="x")

        # Frame in [ 1. main frame]
        self.size_ent = ttk.Entry(self.frame_1, textvariable=self.var1)
        self.size_ent.pack(side="top", padx=5, pady=5, expand="yes", fill="x")
        self.size = Listbox(self.frame_1, bg="gray70")
        self.size.pack(side="top", padx=5, pady=5, expand="yes", fill="both")
        for i in range(30):
            self.size.insert(END, i)

        ttk.Label(self.main_frame_1, text="""\nABCDEabcde12345\n""", font=self.font_1).pack(
            expand="no", padx=10, pady=10
        )
        # Frame in [ 2. mainframe]
        ttk.Button(self.main_frame_2, text="   OK   ", command=self.out).pack(
            side="left", expand="yes", fill="x", padx=5, pady=5
        )
        ttk.Button(self.main_frame_2, text=" Cancel ", command=self.end).pack(
            side="left", expand="yes", fill="x", padx=5, pady=5
        )
        ttk.Button(self.main_frame_2, text=" Apply  ", command=self.applied).pack(
            side="left", expand="yes", fill="x", padx=5, pady=5
        )

        self.listbox.bind("<<ListboxSelect>>", self.checkface)
        self.size.bind("<<ListboxSelect>>", self.checksize)

    def checkface(self, event=None):
        try:
            self.var.set(str(self.listbox.get(self.listbox.curselection())))
            self.font_1.config(
                family=self.var.get(),
                size=self.var1.get(),
                weight=self.var2.get(),
                slant=self.var3.get(),
                underline=self.var4.get(),
                overstrike=self.var5.get(),
            )
        except IndexError:
            pass

    def checksize(self, event=None):
        try:
            self.var1.set(int(self.size.get(self.size.curselection())))
            self.font_1.config(
                family=self.var.get(),
                size=self.var1.get(),
                weight=self.var2.get(),
                slant=self.var3.get(),
                underline=self.var4.get(),
                overstrike=self.var5.get(),
            )
        except IndexError:
            pass

    def checkstyle(self, event=None):
        try:
            self.font_1.config(
                family=self.var.get(),
                size=self.var1.get(),
                weight=self.var2.get(),
                slant=self.var3.get(),
                underline=self.var4.get(),
                overstrike=self.var5.get(),
            )
        except IndexError:
            pass

    def applied(self):
        self.result = (
            self.var.get(),
            self.var1.get(),
            self.var2.get(),
            self.var3.get(),
            self.var4.get(),
            self.var5.get(),
        )
        self.mainfont["family"] = self.var.get()
        self.mainfont["size"] = self.var1.get()
        self.mainfont["weight"] = self.var2.get()
        self.mainfont["slant"] = self.var3.get()
        self.mainfont["underline"] = self.var4.get()
        self.mainfont["overstrike"] = self.var5.get()

    def out(self):
        self.result = (
            self.var.get(),
            self.var1.get(),
            self.var2.get(),
            self.var3.get(),
            self.var4.get(),
            self.var5.get(),
        )
        self.mainfont["family"] = self.var.get()
        self.mainfont["size"] = self.var1.get()
        self.mainfont["weight"] = self.var2.get()
        self.mainfont["slant"] = self.var3.get()
        self.mainfont["underline"] = self.var4.get()
        self.mainfont["overstrike"] = self.var5.get()
        # applied()
        self.destroy()

    def end(self):
        self.result = None
        self.destroy()
