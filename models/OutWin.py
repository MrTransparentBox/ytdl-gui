import threading
from tkinter.constants import *
from tkinter import ttk, messagebox, Text, StringVar, font, Toplevel
# from DownloaderGUI import Application 
from .Redirects import StdoutRedirect, StderrRedirect
class OutWin(Toplevel):
    def __init__(self, master, mode: str, title="New window", geometry: str = "1080x600", block=True, setGrab=True, deleteOnClose=1):
        Toplevel.__init__(self, master)
        self.config(bg=master.backgrounds[master.appConfig['prefs']['theme']])
        self.master = master
        self.block=block
        self.setGrab = setGrab
        self.delClose=deleteOnClose
        self.title(title)
        self.mode=mode
        self.clsCount=0
        self.geometry(geometry)
        self.textFrm = ttk.Frame(self)
        self.yScroll = ttk.Scrollbar(self.textFrm)
        self.outText = Text(self.textFrm, font=self.master.curr_font, yscrollcommand=self.yScroll.set, relief=FLAT, state=DISABLED)
        self.yScroll.config(command=self.outText.yview)
        if self.master.appConfig['prefs']['print_log']: 
            self.outRedir = StdoutRedirect(self.outText, interactive=False)
            self.errRedir = StderrRedirect(self.outText, interactive=False, master=self)
        if self.mode == "yt":
            # self.btnStart = ttk.Button(self, text="Start Download", command=self.task)
            self.yt_frm = ttk.Frame(self)
            self.progress = ttk.Progressbar(self.yt_frm, length=600, mode='determinate', maximum=1, value=0)
            self.progress.grid(column=0, row=0, padx=3, sticky=W)
            self.stat=StringVar(self.yt_frm, value="0MiB/0MiB @ 0MiB/s")
            ttk.Label(self.yt_frm, textvariable=self.stat, font=font.Font(size=14)).grid(column=1, row=0, padx=3)
            self.percent=StringVar(self.yt_frm, value=f"{self.progress['value']*100}%")
            ttk.Label(self.yt_frm, font=font.Font(size=10), textvariable=self.percent).grid(column=0, row=0)
            self.yt_frm.pack(side=TOP, pady=7.5)
        elif self.mode == "time":
            # self.btnStart = ttk.Button(self, text="Start Duration Scan", command=self.task)
            pass
        else:
            print(f"mode '{self.mode}' incorrect")
        
        self.task()
        # self.btnStart.pack(side=BOTTOM)
        self.textFrm.pack(side=TOP, expand=True, fill=BOTH)
        self.yScroll.pack(fill=Y, side=RIGHT)
        self.outText.pack(expand=True, fill=BOTH)
        self.iconbitmap(self.master.relative_path("Resources\\YTDLv2_256.ico"))
        self.protocol("WM_DELETE_WINDOW", self.outWin_close)
        self.focus_set()
        if self.setGrab: self.grab_set()
    def outWin_close(self, event=None):
        self.master = self.master
        if self.master.running and self.block:
            messagebox.showerror("Cannot close", "Unable to close window while download is in progress.", parent=self)
            return
        elif self.master.running and self.delClose == 1:
            messagebox.showwarning("Download not stopped...", "Download logs continue in the console.", parent=self)
        self.grab_release()
        if self.delClose == 1: # Do delete
            self.destroy()
            self.outRedir.close()
            self.errRedir.close()
            if self.mode == "yt" and hasattr(self.master, "yt_download_win"): 
                self.master.yt_download_win.destroy()
                del self.master.yt_download_win
                self.master.log_debug("Deleted yt win")
            elif self.mode == "time" and hasattr(self.master, "time_window"):
                self.master.time_window.destroy()
                del self.master.time_window
                self.master.log_debug("Deleted time win")
        elif self.delClose == 0: # Don't delete
            self.withdraw()
            self.master.log_debug("Withdrawn")
        self.master.focus_set()
    def task(self):
        if self.mode == "yt" and self.master.appConfig['prefs']['rerun']:
            self.t = threading.Thread(target=self.master.yt_download, args=[2])
        elif self.mode == "yt":
            self.t = threading.Thread(target=self.master.yt_download)
        elif self.mode == "time":
            self.t = threading.Thread(target=self.master.start_time)
        else:
            print(f"mode '{self.mode}' incorrect")
            return
        self.t.start()