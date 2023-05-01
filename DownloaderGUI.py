#!/usr/bin/env D:\alexj\VSCode\Python\YTDL\.venv
"""This is a script to generate an easy to use GUI for the youtube-dl package.

This is usually bundled into an executable with pyinstaller (or similar) for ease of use to non-python users.  
This also implements some additional features on top of what youtube-dl provides, such as, total length calculation of videos in a folder, spotify support (eventually) and more...
"""
print("Loading Modules...")
import os, json, sys, threading, argparse, spotipy, re, validators
from ttkthemes import ThemedTk # pylint: disable=import-error
from tkinter import messagebox, filedialog, ttk, font
from tkinter import * #For development use... pylint: disable=unused-wildcard-import
from typing import Any
from yt_dlp import YoutubeDL # pylint: disable=import-error
from models import GetStats, Font_wm
class Application(ThemedTk):
    """Base application window and functions for the Youtube-dl GUI

    Attributes
    ------
        title: The title of the window
        size: Form of "``x_size``x``y_size``"
        debug: Whether to put the app in debug mode. Prints additional info.
        path: Path-like string determining the path of the `.ytdl` or other file to open. Leave as ```None``` for default `ToDownload.ytdl` file
        version: Version info if applicable.
    """
    def __init__(self, size, debug=False, path=None, version_info=None):
        print("Loading preferences and settings...")
        self.appConfig = {}
        self.running=False
        self.debug=debug
        self.path=path
        self.dataPath=os.path.abspath(os.path.expandvars("%appdata%\\Youtube-dl_GUI"))
        self.appVersion=version_info
        self.exe = bool(getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"))
        if not os.path.exists(self.dataPath): 
            self.log_debug("Creating '%appdata/Youtube-dl_GUI' folder")
            os.mkdir(self.dataPath)
        if not os.path.exists(os.path.join(self.dataPath, "appConfig.json")): 
            open(os.path.join(self.dataPath,"appConfig.json"), "x").close()
            self.log_debug("Creating 'appConfig.json'")
        with open(os.path.join(self.dataPath, "appConfig.json"), "r") as f:
            try:
                self.appConfig = json.load(f)
            except json.decoder.JSONDecodeError:
                print("Error in config. Setting default config...")
                self.appConfig={}
            f.close()

        self.defaultConfig={"dir": "", "spotify_enabled": False, "prefs": {"font": ["Arial", 14, "normal", "roman", 0, 0], "parallel": False, "print_log": True, "theme": "vista", "verbosity": False, "remove_success": False, "rerun": False, "outwin_mode": 0, "update_launch": True, "disable_stats": False, "disable_percentage": False}, "opts": {"resolution": 1080, "subtitles": True, "metadata": True, "thumbnail": True, "description": False, "audio": False}}
        if self.appConfig == {}:
            self.appConfig=self.defaultConfig
            self.write_config()
        if self.path == None:
            self.path = os.path.abspath(os.path.join(self.dataPath, "ToDownload.ytdl"))
            self.log_debug("Loading default .ytdl", True)
            if not os.path.exists(self.path): 
                open(self.path, "x").close() # Create if it doesn't exist
                self.log_debug("Creating ToDownload.ytdl")
        elif not (os.path.exists(self.path) and os.path.isfile(self.path) and (str(self.path).endswith(".ytdl") or str(self.path).endswith(".vdl"))):
            raise OSError("File specified must be an existing file of type .ytdl (or .vdl for legacy files)")        
        self.backgrounds = {'adapta': '#FAFBFC', 'alt': '#D9D9D9', 'aquativo': '#FAFAFA', 'arc': '#F5F6F7', 'awarc': '#F5F6F7', 'awblack': '#424242', 'awbreeze': '#EFF0F1', 'awbreezedark': '#2F3336', 'awclearlooks': '#EFEBE7', 'awdark': '#33393B', 'awlight': '#E8E8E7', 'awtemplate': '#424242', 'awwinxpblue': '#ECE9D8', 'black': '#424242', 'blue': '#6699CC', 'breeze': '#EFF0F1', 'clam': '#DCDAD5', 'classic': '#D9D9D9', 'clearlooks': '#EFEBE7', 'default': '#D9D9D9', 'elegance': '#D8D8D8', 'equilux': '#464646', 'itft1': '#DAEFFD', 'keramik': '#CCCCCC', 'kroc': '#FCB64F', 'plastik': '#EFEFEF', 'radiance': '#EFEFEF', 'scidblue': '#D8D8D8', 'scidgreen': '#D8D8D8', 'scidgrey': '#D8D8D8', 'scidmint': '#D8D8D8', 'scidpink': '#D8D8D8', 'scidpurple': '#D8D8D8', 'scidsand': '#D8D8D8', 'smog': '#E7EAF0', 'ubuntu': '#F6F4F2', 'vista': '#F0F0F0', 'winnative': '#F0F0F0', 'winxpblue': '#ECE9D8', 'xpnative': '#F0F0F0', 'yaru': '#F0F0F0'}
        super().__init__(theme=self.appConfig['prefs']['theme'], toplevel=self.backgrounds[self.appConfig['prefs']['theme']], themebg=self.backgrounds[self.appConfig['prefs']['theme']])
        self.tk.call('lappend', 'auto_path', self.relative_path('awthemes-10.3.0'))
        self.tk.call('package', 'require', 'awthemes')
        self.tk.call('lappend', 'auto_path', self.relative_path('tksvg0.7'))
        self.tk.call('package', 'require', 'tksvg')
        self.availThemes = ['adapta', 'alt', 'aquativo', 'arc', 'awarc', 'awblack', 'awbreeze', 'awbreezedark', 'awclearlooks', 'awdark', 'awlight', 'awtemplate', 'awwinxpblue', 'black', 'blue', 'breeze', 'clam', 'classic', 'clearlooks', 'default', 'elegance', 'equilux', 'itft1', 'keramik', 'kroc', 'plastik', 'radiance', 'scidblue', 'scidgreen', 'scidgrey', 'scidmint', 'scidpink', 'scidpurple', 'scidsand', 'smog', 'ubuntu', 'vista', 'winnative', 'winxpblue', 'xpnative', 'yaru']
        ths = self.get_themes()
        ths.sort()
        self.log_debug(f"THEMES PRESENT: {ths == self.availThemes}"); print(f"EXE: {self.exe}")
        self.log_debug(", ".join(ths))
        if ths != self.availThemes:
            difference=list(set(ths) ^ set(self.availThemes))
            messagebox.showerror("Themes unavailable", f"The themes: {difference} aren't available\nThis may require a reinstall of the software to fix this issue.\nOtherwise, please report an issue.", parent=self)
            if self.appConfig['prefs']['theme'] in difference:
                sys.exit(f"Themes: {', '.join(difference)} \nare unavailable")
        del ths, self.availThemes
        if str(self.appConfig["dir"]).strip() == "":
            ans = filedialog.askdirectory(parent=self, title="Select Download Directory...")
            if ans.strip() == "":
                sys.exit("No Directory given...")
            else:
                self.appConfig["dir"] = os.path.abspath(ans)
        os.environ["SPOTIPY_CLIENT_ID"] = "fbeffc75e6a44a119e33e9061123fefc"
        os.environ['SPOTIPY_REDIRECT_URI'] = "http://localhost:8000/authorise"
        if self.appConfig['spotify_enabled'] == True:
            self.log_debug("Enabling spotify...")
            self.PKCE_Man = spotipy.SpotifyPKCE(scope="playlist-read-private,playlist-read-collaborative")
            self.spotify = spotipy.Spotify(auth_manager=self.PKCE_Man)
        self.title(f"Youtube-dl GUI - {str(self.appConfig['dir'])}")
        self.iconbitmap(self.relative_path("Resources\\YTDLv2_256.ico"))
        self.geometry(size)
        self.saved = True
        confont = self.appConfig['prefs']['font']
        self.curr_font = font.Font(family=confont[0], size=confont[1], weight=confont[2], slant=confont[3], underline=confont[4], overstrike=confont[5])
        self.write_config()
        self.btnFrm = ttk.Frame(self)
        self.btnFrm.pack(side=BOTTOM, fill=X, expand=True)
        ttk.Frame(self.btnFrm).grid(row=0, column=0)
        mid = ttk.Frame(self.btnFrm)
        mid.grid(row=0, column=1)
        self.ytButton=ttk.Button(mid, text="Start Download...", command=self.yt_win)
        self.timeButton=ttk.Button(mid, text="List Time...", command=self.time)
        self.ytButton.grid(row=0, column=0, padx=3, pady=5)
        self.timeButton.grid(row=0, column=1, padx=3, pady=5)
        ttk.Frame(self.btnFrm).grid(row=0, column=2)
        self.btnFrm.grid_columnconfigure(0, weight=1)
        self.btnFrm.grid_columnconfigure(1, weight=1)
        self.btnFrm.grid_columnconfigure(2, weight=1)
        self.textFrame = ttk.Frame(self)
        self.yScroll = ttk.Scrollbar(self.textFrame)
        self.xScroll = ttk.Scrollbar(self.textFrame, orient=HORIZONTAL)
        self.mainText = Text(self.textFrame, xscrollcommand=self.xScroll.set, yscrollcommand=self.yScroll.set, relief=FLAT, font=self.curr_font, undo=True, maxundo=-1)
        self.yScroll.config(command=self.mainText.yview)
        self.xScroll.config(command=self.mainText.xview)
        self.f = open(self.path, "r+")
        self.log_debug(f"Opened file {self.f.name}  ||  Encoding is {self.f.encoding}")
        try:
            self.f.seek(0)
            inStrL = self.f.readlines()
            self.log_debug(f"Read {inStrL} from {self.f.name}")
        except UnicodeDecodeError:
            inStrL=""
            messagebox.showerror("Bad encoding", "The encoding of the file isn't supported", parent=self)
        if len(inStrL) > 0:
            if type(inStrL[0]) == bytes: inStrL = [i.decode() for i in inStrL]
            if inStrL[-1][-1:] == "\n": inStrL[-1] = inStrL[-1][:-1]
            for i in inStrL:
                if i.strip() in ("", "\n"): inStrL.remove(i)
        self.mainText.insert("1.0", "".join(inStrL))
        self.mainText.edit_reset()
        self.textFrame.pack(side=TOP, expand=True, fill=BOTH, padx=5)
        self.yScroll.pack(side=RIGHT, fill=Y)
        self.xScroll.pack(side=BOTTOM, fill=X)
        self.mainText.pack(side=TOP, expand=True, fill=BOTH)
        self.menu = Menu(self, relief=FLAT)

        self.fileMenu=Menu(self.menu, tearoff=0)
        self.fileMenu.add_command(label="New (CTRL+N)", command=self.new)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Save (CTRL+S)", command=self.save)
        self.fileMenu.add_command(label="Save As (CTRL+SHIFT+S)...", command=self.save_as)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Open (CTRL+O)...", command=self.open)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Preferences...", command=self.prefs_win)

        self.editMenu=Menu(self.menu, tearoff=0)
        self.editMenu.add_command(label="Undo (CTRL+Z)", command=self.mainText.edit_undo)
        self.editMenu.add_command(label="Redo (CTRL+Y)", command=self.mainText.edit_redo)

        self.viewMenu = Menu(self.menu, tearoff=0)
        self.viewMenu.add_command(label="Font...", command=self.font)

        self.toolMenu=Menu(self.menu, tearoff=0)
        self.toolMenu.add_command(label="Current File", command=self.curr_file)
        self.toolMenu.add_command(label="Current Directory", command=self.curr_dir)
        self.toolMenu.add_command(label="Change Directory...", command=self.change_dir)
        self.toolMenu.add_separator()
        self.toolMenu.add_command(label="Download Options...", command=self.options_win)
        self.toolMenu.add_separator()
        self.toolMenu.add_command(label="Enable Spotify support..." if self.appConfig['spotify_enabled'] is False else "Spotify already enabled.", command=self.enable_sp, state=NORMAL if self.appConfig['spotify_enabled'] is False else DISABLED)
        self.stats=None

        self.helpMenu=Menu(self.menu, tearoff=0)
        self.helpMenu.add_command(label="About Youtube-dl GUI", command=self.about)
        self.helpMenu.add_command(label="Help & Instructions", command=self.openHelp)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label="Report Bug", command=self.bug)
        self.helpMenu.add_command(label="Check for updates...", command=self.check_update)

        self.menu.add_cascade(label="File", menu=self.fileMenu, underline=0)
        self.menu.add_cascade(label="Edit", menu=self.editMenu, underline=0)
        self.menu.add_cascade(label="View", menu=self.viewMenu, underline=0)
        self.menu.add_cascade(label="Tools", menu=self.toolMenu, underline=0)
        self.menu.add_cascade(label="Help", menu=self.helpMenu, underline=0)
        self.config(menu=self.menu)

        self.bind_all("<Control-n>", self.new)
        self.bind_all("<Control-s>", self.save)
        self.bind_all("<Control-Shift-S>", self.save_as)
        self.bind_all("<Control-o>", self.open)
        self.mainText.bind("<Control-Shift-Z>", self.mainText.edit_redo)
        self.mainText.bind("<<Modified>>", self.modified)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if self.appConfig['prefs']['update_launch']:
            if self.check_update(start_up=True) == False:
                self.log_debug("No updates")
        self.update_theme(self.appConfig['prefs']['theme'])

    def log_debug(self, value: object, default_stdout: bool=False):
        if self.debug: 
            if default_stdout:
                print(value)
            elif hasattr(self, "yt_download_win"):
                self.yt_download_win.outRedir.old_stdout.write(f"{str(value)}\n")
            elif hasattr(self, "time_window"):
                self.time_window.outRedir.old_stdout.write(f"{str(value)}\n")
            else:
                print(value)
    def new(self, event: Any=None) -> None:
        self.log_debug("New file")
        if self.ask_save() == None: return
        self.mainText.delete("1.0", END)
        self.f.close()
        self.f = None
    def ask_save(self):
        """Ask user if they want to save.
        
        Ask user if they want to save. Returns `True` and auto-saves if they do want to save, `False` if they don't and `None` if they cancel.
        
        Returns:
            True: if yes is selected
            False: if no is selected
            None: if cancel is selected"""
        if not self.saved:
            self.log_debug("Asking save")
            sv = messagebox.askyesnocancel("Save Changes?", "Do you want to save your changes?", parent=self)
            if sv == True:
                self.save()
                return True
            elif sv == False:
                return False
            elif sv == None:
                return None
        else:
            self.log_debug("Already saved.")
            return True
    def save(self, event=None):
        if self.f == None:
            self.save_as()
            self.log_debug("Save as from save")
            return
        self.saved=True
        self.title(self.title().replace("*", ""))
        self.log_debug("Save")
        s=self.mainText.get("1.0", END)[:-1]
        self.log_debug(s)
        self.f.truncate(0)
        self.log_debug(f"SEEKABLE: {self.f.seekable()}")
        self.f.seek(0)
        self.f.write(s)
        self.f.flush()
        os.fsync(self.f)
    def save_as(self, event=None):
        path = filedialog.asksaveasfilename(confirmoverwrite=True, defaultextension=".ytdl", initialfile="downloads.ytdl", filetypes=[("Youtube-dl File (*.ytdl)", "*.ytdl"), ("Legacy Downloader File (*.vdl)", "*.vdl")], title="Save As...", parent=self)
        if path:
            self.log_debug("Save as")
            if self.f != None: self.f.close()
            self.f=open(path, "r+")
            self.title(f"Youtube-dl GUI - {path}")
            self.save()
        else:
            self.log_debug("Save as cancelled")
    def open(self, event=None):
        path = filedialog.askopenfilename(defaultextension=".ytdl", filetypes=[("Youtube-dl File (*.ytdl)", "*.ytdl"), ("Legacy Downloader File (*.vdl)", "*.vdl")], parent=self, title="Open...")
        if path:
            self.log_debug("Open")
            if self.f != None: self.f.close()
            self.f=open(path, "r+")
            try:
                inStrL = self.f.readlines()
                self.mainText.delete("1.0", END)
                self.log_debug(f"Read {inStrL} from {self.f.name}")
            except UnicodeDecodeError:
                inStrL=""
                messagebox.showerror("Bad encoding", "The encoding of the file isn't supported", parent=self)
            if len(inStrL) > 0:
                if type(inStrL[0]) == bytes: inStrL = [i.decode() for i in inStrL]
                if inStrL[-1][-1:] == "\n": inStrL[-1] = inStrL[-1][:-1]
                for i in inStrL:
                    if i.strip() in ("", "\n"): inStrL.remove(i)
            self.title(f"Youtube-dl GUI - {path}")
            self.mainText.insert("1.0", "".join(inStrL))
            self.mainText.edit_reset()
            self.saved=False
            self.title(f"*{self.title()}*")
    @staticmethod
    def version_compare(ver1: str, ver2: str):
        sp1=ver1.split(".")
        sp2=ver2.split(".")
        if len(sp1) != len(sp2): raise ValueError(f"Version formats of {ver1} and {ver2} aren't the same.")
        for i in range(len(sp1)):
            if sp1[i] > sp2[i]:
                return ">"
            elif sp1[i] < sp2[i]:
                return "<"
            elif sp1[i] == sp2[i] and i == ver1.count("."):
                return "="
        raise Exception("Something went wrong and the comparisons didn't match.")
    def check_update(self, start_up: bool=False):
        def update_Win():
            self.uWin = Toplevel(self, background=self.backgrounds[self.appConfig['prefs']['theme']])
            self.uWin.iconbitmap(self.relative_path("Resources\\YTDLv2_256.ico"))
            self.uWin.title("Youtube-dl GUI - Update")
            ttk.Label(self.uWin, text=f"A new version of Youtube-dl GUI is available!\nAn update is recommended.", justify=LEFT).pack(padx=5, pady=5)
            ttk.Label(self.uWin, text=f"\tNew version: {tag}\n\tYour Version: v{self.appVersion}", justify=LEFT).pack(pady=10)
            ttk.Label(self.uWin, text="Click update to download the new version.", justify=LEFT).pack()
            updateBtn=ttk.Button(self.uWin, text="Update", command=threading.Thread(target=st_update).start)
            updateBtn.pack(side=BOTTOM, pady=15)
            self.uWin.focus_set()

        def st_update():
            if self.ask_save() == None: return
            def func():
                fname = ""
                progress = ttk.Progressbar(self.uWin, maximum=1, mode="determinate", length=200)
                progress.pack(side=BOTTOM, fill=X, expand=True)
                progress_text=StringVar(progress, value="Downloaded: 0%")
                ttk.Label(self.uWin, textvariable=progress_text, justify=CENTER).pack(side=BOTTOM)
                with requests.Session() as s:
                    # try:
                    #     auth=requests.auth.HTTPBasicAuth("MrTransparentBox", os.environ['github_token'])
                    # except KeyError:
                    #     auth=None
                    # self.log_debug(f"AUTH required: {auth.password if auth != None else auth}")
                    res = s.get(latest['assets'][0]['url'], headers={"Accept": "application/octet-stream", "Authorization": "Bearer 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"}, auth=None, stream=True)
                    res.raise_for_status()
                    cd=res.headers.get("content-disposition")
                    try:
                        fname=os.path.join(os.environ['temp'], cd[cd.index("filename=")+9:])
                    except KeyError:
                        fname=os.path.join(os.path.expandvars("%tmp%"), cd[cd.index("filename=")+9:])
                    length=int(res.headers.get("content-length"))
                    dl=0
                    with open(fname, "wb") as f:
                        for data in res.iter_content(chunk_size=524288):
                            dl+=len(data)
                            f.write(data)
                            progress['value']=dl/length
                            progress_text.set(f"Downloaded: {round(dl/length*100, 1)}%")
                        f.close()
                return fname
            fname = func()
            print(fname)
            # if th.is_alive():
            #     messagebox.showerror("Timeout error", "The download thread timed out. Please try again.\nIf this issue persists please report it on https://github.com/MrTransparentBox/ytdl-gui.", parent=self.uWin)
            os.execv(fname, 
                     ["""/NOCANCEL /RESTARTAPPLICATIONS /SP- /SILENT /NOICONS "/DIR=expand:{autopf}\\Youtube-dl GUI" /deleteinstaller='true'"""])
            os._exit(0)
        try:
            import requests, requests.auth
            # try:
            #     g_auth=requests.auth.HTTPBasicAuth("MrTransparentBox:", os.environ['github_token'])
            # except KeyError:
            g_auth=None
            latest=requests.get("https://api.github.com/repos/MrTransparentBox/ytdl-gui/releases/latest", headers={"accept": "application/vnd.github.v3+json"}, auth=g_auth)
            if latest.status_code == 404:
                messagebox.showinfo("No releases found", "There are no releases for this program.\nIf you think this is an error please report it on", parent=self)
                return None
            latest.raise_for_status()
            latest=latest.json()
            tag=latest['tag_name']
        except Exception as ex:
            messagebox.showerror("Unable to check for update", f"{ex}\n\nTry checking your internet connection, and try again.", parent=self)
            return None
        comp=self.version_compare(tag, f"v{self.appVersion}")
        if comp == "=":
            if not start_up: messagebox.showinfo("Up-to-date", "No updates found", parent=self)
            return False
        elif comp == ">":
            messagebox.showinfo("Update available!", f"New version found: {tag}", parent=self)
            update_Win()
            return True
        elif comp == "<" and not start_up:
            ans=messagebox.askyesno("Preview", f"Looks like you have a special preview or pre-release version! Do you want to install the last full release?")
            if ans: update_Win()
    
    def enable_sp(self):
        if not messagebox.askokcancel("Proceed?", "This will open the authorisation in your default browser when download starts.\nProceed?", parent=self): return
        self.PKCE_Man = spotipy.SpotifyPKCE(redirect_uri="http://localhost:8000/authorise", scope="playlist-read-private,playlist-read-collaborative")
        self.spotify = spotipy.Spotify(auth_manager=self.PKCE_Man)
        self.toolMenu.entryconfigure(7, label="Spotify already enabled.", state=DISABLED)
        self.appConfig['spotify_enabled'] = True
        self.write_config()
    def curr_dir(self):
        messagebox.showinfo("Current Directory", f"Current directory is: {self.appConfig['dir']}", parent=self)
    def curr_file(self):
        messagebox.showinfo("Current File", f"Current file is: {self.f.name if self.f != None else None}", parent=self)
    def change_dir(self):
        ans = filedialog.askdirectory(parent=self, title="Select Download Directory...")
        if ans.strip() != "":
            self.appConfig['dir'] = os.path.abspath(ans)
        self.write_config()
        self.title(f"Youtube-dl GUI - {str(self.appConfig['dir'])}")
    def about(self):
        def link(url):
            os.startfile(url)
        
        self.aWin=Toplevel(self, background=self.backgrounds[self.appConfig['prefs']['theme']])
        self.aWin.title("Youtube-dl GUI - About")
        # self.aWin.geometry("300x175")
        self.aWin.iconbitmap(self.relative_path("Resources\\YTDLv2_256.ico"))
        aboutNote = ttk.Notebook(self.aWin)
        aboutNote.pack(side=TOP, expand=True, fill=BOTH)
        mainFrm=ttk.Frame(self.aWin)
        verLbl=ttk.Label(mainFrm, text=f"Youtube-dl GUI v{self.appVersion}", justify=LEFT, anchor=NW)
        verLbl.grid(column=0,row=0,sticky=NW,padx=10,pady=2, columnspan=2)
        undFnt = font.Font(verLbl, font=verLbl.cget("font"), underline=True, size=9)

        ttk.Label(mainFrm, text="Author: ", justify=LEFT).grid(column=0,row=1,sticky=NW,padx=10,pady=2)
        ttk.Label(mainFrm, text="Alex Johnson", justify=LEFT).grid(column=1,row=1,sticky=NW,padx=10,pady=2)
        ttk.Label(mainFrm, text="Contact: ", justify=LEFT).grid(column=0,row=2,sticky=NW,padx=10,pady=2)
        con2Lbl=ttk.Label(mainFrm, text="16JohnA28@gmail.com", foreground="#00A7FF", font=undFnt, cursor="hand2", justify=LEFT)
        con2Lbl.bind("<Button-1>", lambda e: link("mailto:16JohnA28@gmail.com"))
        con2Lbl.grid(column=1,row=2,sticky=NW,padx=10,pady=2)
        ttk.Label(mainFrm, text="Github: ", justify=LEFT).grid(column=0,row=3,sticky=NW,padx=10,pady=2)
        git2Lbl=ttk.Label(mainFrm, text="https://github.com/MrTransparentBox/ytdl-gui", foreground="#00A7FF", font=undFnt, cursor="hand2", justify=LEFT)
        git2Lbl.bind("<Button-1>", lambda e: link("https://github.com/MrTransparentBox/ytdl-gui"))
        git2Lbl.grid(column=1,row=3,sticky=NW,padx=10,pady=2)
        ttk.Label(mainFrm, text="Copyright © 2021 Alexander Johnson", justify=LEFT).grid(column=0, row=4, columnspan=3, pady=5)
        ttk.Label(mainFrm, text='THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,\nEXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF\nMERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.\nIN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR\nOTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,\nARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR\nOTHER DEALINGS IN THE SOFTWARE.\n', 
        justify=LEFT, relief=GROOVE).grid(column=0, row=5, columnspan=3)
        ttk.Label(mainFrm, text="Refer to ").grid(column=0, row=6, sticky=W)
        locLbl=ttk.Label(mainFrm, text="LICENSE", foreground="#00A7FF", font=undFnt, cursor="hand2", justify=LEFT)
        locLbl.bind("<Button-1>", lambda e: link(self.relative_path("info\\LICENSE")))
        locLbl.grid(column=1, row=6, sticky=W)
        ttk.Label(mainFrm, text=" for information regarding distribution, modification and use", justify=LEFT).grid(column=2, row=6, sticky=W)
        aboutNote.add(mainFrm, text="About Youtube-dl GUI")

        ffmpegFrm = ttk.Frame(self.aWin)
        ffLicTxt = Text(ffmpegFrm)
        with open(self.relative_path("ffmpeg-20200115-0dc0837-win64-static\\LICENSE.txt"), "r") as f: 
            ffLicTxt.insert(INSERT, "".join(f.readlines()))
            f.close()
        ffLicTxt.config(state=DISABLED)
        ffLicY = ttk.Scrollbar(ffmpegFrm, command=ffLicTxt.yview)
        ffLicY.pack(side=RIGHT, fill=Y,expand=True)
        ffLicTxt.config(yscrollcommand=ffLicY.set)
        ffLicTxt.pack(side=LEFT, fill=BOTH, expand=True)
        aboutNote.add(ffmpegFrm, text="FFMPEG License")

        atomicFrm = ttk.Frame(self.aWin)
        atLicTxt = Text(atomicFrm)
        with open(self.relative_path("AtomicParsley-win32-0.9.0\\COPYING"), "r") as f: 
            atLicTxt.insert(INSERT, "".join(f.readlines()))
            f.close()
        atLicTxt.config(state=DISABLED)
        atLicY = ttk.Scrollbar(atomicFrm, command=atLicTxt.yview)
        atLicY.pack(side=RIGHT, fill=Y,expand=True)
        atLicTxt.config(yscrollcommand=atLicY.set)
        atLicTxt.pack(side=LEFT, fill=BOTH, expand=True)
        aboutNote.add(atomicFrm, text="Atomic Parsley License")

        awthemeFrm = ttk.Frame(self.aWin)
        awLicTxt = Text(awthemeFrm)
        with open(self.relative_path("awthemes-10.3.0\\LICENSE"), "r") as f: 
            awLicTxt.insert(INSERT, "".join(f.readlines()))
            f.close()
        awLicTxt.config(state=DISABLED)
        awLicY = ttk.Scrollbar(awthemeFrm, command=awLicTxt.yview)
        awLicY.pack(side=RIGHT, fill=Y,expand=True)
        awLicTxt.config(yscrollcommand=atLicY.set)
        awLicTxt.pack(side=LEFT, fill=BOTH, expand=True)
        aboutNote.add(awthemeFrm, text="Awthemes License")

    def openHelp(self):
        self.helpWin = Toplevel(self, background=self.backgrounds[self.appConfig['prefs']['theme']])
        self.helpWin.title("Youtube-dl GUI - Help")

        helpFrm = ttk.Frame(self.helpWin)
        helpTxt = Text(helpFrm)
        helpTxt.insert(INSERT, "No U, get good.")
        helpTxt.config(state=DISABLED)
        helpFrm.pack()
        helpTxt.pack(side=LEFT, fill=BOTH, expand=True)

    def time(self):
        if hasattr(self, "time_window"):
            self.time_window.deiconify()
            if self.time_window.setGrab: self.time_window.grab_set()
            self.log_debug("Unwithdrawn time win")
        else:
            self.time_window = OutWin(self, "time", f"List Time Output - {self.appConfig['dir']}", block=False, deleteOnClose=1)
            self.stats = GetStats(self.appConfig['dir'])
            self.log_debug("Created time win")
    def yt_win(self):
        if self.ask_save() == None: return

        # if self.f == None: messagebox.showerror("No open file", "Must have an open .ytdl file before download", parent=self)
        if hasattr(self, "yt_download_win"):
            self.yt_download_win.deiconify()
            self.log_debug("Unwithdrawn yt win")
            if self.yt_download_win.setGrab: self.yt_download_win.grab_set()
        else:
            self.yt_download_win = OutWin(self, "yt", f"Download Output - {self.appConfig['dir']}", block=False, setGrab=True, deleteOnClose=self.appConfig['prefs']['outwin_mode'])
            self.log_debug("Created yt win")
    def yt_download(self, toDisable: ttk.Button, run=1):
        toDisable.config(state=DISABLED)
        def progress_hook(d: dict):
            def inner_hook(d: dict):
                if d['status'] == 'downloading':
                    if not self.appConfig['prefs']['disable_percentage']:

                        try:
                            if d['total_bytes'] != None:
                                self.yt_download_win.progress['value'] = d['downloaded_bytes'] / d['total_bytes']
                        except Exception as e:
                            self.yt_download_win.errRedir.old_stderr.write(f"WARNING: Progess bar unavailable; {e}\n")
                        else:
                            self.yt_download_win.percent.set(f"{round(self.yt_download_win.progress['value']*100, 1)}%")
                    if not self.appConfig['prefs']['disable_stats']:
                        MiB_done=d['downloaded_bytes']/1048576
                        self.log_debug(MiB_done)
                        if d['total_bytes'] != None:
                            self.log_debug(MiB_done/d['elapsed'])
                            self.log_debug(d['total_bytes']/1048576)
                            self.yt_download_win.stat.set(f"{round(MiB_done, 1)}MiB/{round(d['total_bytes']/1048576, 1)}MiB @ {round(MiB_done/d['elapsed'], 1)}MiB/s")
                elif d['status'] == 'finished':
                    try:
                        print(f"Finished downloading {d['total_bytes']} bytes in {d['elapsed']} seconds")
                    except:
                        print("Download finished")
                    finally:
                        self.yt_download_win.progress['value'] = 0
                        self.yt_download_win.percent.set("Download Complete! - Finishing up")
                        tot=round(d['total_bytes']/1048576, 1)
                        self.yt_download_win.stat.set(f"{tot}MiB/{tot}MiB @ 0MiB/s")
            t = threading.Thread(target=inner_hook, args=[d]).start()
        if not os.path.exists(os.path.join(self.dataPath, "archive.txt")):
            open(os.path.join(self.dataPath, "archive.txt"), "w").close() # Create archive if it doesn't exist
        opts = {"default_search": "auto", 
        "outtmpl": f"{self.appConfig['dir']}\\%(upload_date)s-%(uploader)s-%(title)s.%(ext)s",
        "format": f"bestvideo[height<=?{self.appConfig['opts']['resolution']}][ext=mp4]+bestaudio[ext=m4a]/best[height<=?{self.appConfig['opts']['resolution']}][ext=mp4]/best[ext=mp4]/best", 
        "ffmpeg_location": self.relative_path("ffmpeg-20200115-0dc0837-win64-static\\bin"),
        "cookiefile": self.relative_path("Logs\\cookies.txt"),
        "writethumbnail": self.appConfig['opts']['thumbnail'], 
        "writesubtitles": self.appConfig['opts']['subtitles'], 
        "writeautomaticsub": self.appConfig['opts']['subtitles'], 
        'writedescription': self.appConfig['opts']['description'],
        "retries": 2, 
        "ignoreerrors": True,
        "download_archive": os.path.join(self.dataPath, "archive.txt"), 
        "progress_hooks": [], 
        "postprocessors": [],
        "verbose": self.appConfig['prefs']['verbosity']} or self.debug
        if self.appConfig['opts']['audio']: opts['postprocessors'].append({'key': 'FFmpegExtractAudio'})
        if self.appConfig['opts']['metadata']: opts['postprocessors'].append({'key': 'FFmpegMetadata'})
        # if self.appConfig['opts']['thumbnail']: opts['postprocessors'].append({'key': 'EmbedThumbnail', 'already_have_thumbnail': False, "atomic_path": self.relative_path("AtomicParsley-win32-0.9.0/AtomicParsley.exe")})#"./AtomicParsley-win32-0.9.0/AtomicParsley.exe"})
        if self.appConfig['opts']['thumbnail']: opts['postprocessors'].append({'key': 'EmbedThumbnail', 'already_have_thumbnail': False})
        if self.appConfig['opts']['subtitles']: opts['postprocessors'].append({'key': 'FFmpegEmbedSubtitle'})
        if self.appConfig['prefs']['disable_stats'] == False or self.appConfig['prefs']['disable_percentage'] == False: 
            self.log_debug("Added progress hook")
            opts['progress_hooks'].append(progress_hook)
        ytdl = YoutubeDL(opts)
        self.log_debug(f"Parallel: {str(self.appConfig['prefs']['parallel'])}")
        lines=[]
        if self.f == None:
            lines = self.mainText.get("1.0", END).split("\n")
        else:
            self.f.seek(0)
            lines = [i.replace("\n", "") for i in self.f.readlines()]
        warn_sp=False
        items=[]
        for i in lines:
            if (validators.url(i) == True and "open.spotify.com" in i) or bool(re.fullmatch(r"spotify:((track)|(playlist)|(album)|(artist)|(show)|(episode)):([0-9]|[A-Z]|[a-z]){22}", i)):
                # ^ If the line is a valid spotify url, uri or id
                if not warn_sp and not self.appConfig['spotify_enabled']:
                    ans=messagebox.askyesnocancel("Spotify not enabled", "Spotify support is an optional extra.\nTo enable it either go to Tools > Enable Spotify support...\nOr click 'Yes' to enable it now.\nIf it is not enabled all spotify lines will be removed", parent=self.yt_download_win)
                    if ans == None: 
                        return
                    elif ans == True: 
                        self.enable_sp()
                if self.appConfig['spotify_enabled']:
                    items.extend(self.get_items(i))
            elif not i.strip() == "" and not i.strip().startswith("#"): 
                items.append(i)
        if items[-1].strip() == "": items = items[:-1]
        messagebox.showwarning("Starting Download", "This may take some time...", parent=self.yt_download_win)
        self.running = True
        if not self.appConfig['prefs']['print_log']: self.disable_insert(self.yt_download_win.outText, END, "Check console window if you want to see output")
        for a in range(run):
            if self.appConfig['prefs']['parallel'] == False:
                ytdl.download(items)
            else:
                for i in items:
                    th = threading.Thread(target=ytdl.download, args=[[i]])
                    th.start()
                th.join()
            
            if self.appConfig['prefs']['remove_success'] or self.debug:
                ltext: list = self.mainText.get("1.0", END).split("\n")
                copy=ltext.copy()
                with open(os.path.join(self.dataPath, "archive.txt"), "r") as f: 
                    success = f.readlines()
                    f.close()
                success=[i[i.index(" ")+1:-1] for i in success]
                self.log_debug(success)
                for i in ltext:
                    for x in success:
                        if x in i and not self.debug:
                            copy.remove(i)
                        elif x in i and self.debug:
                            copy.remove(i)
                            self.log_debug(f"Removing {i} from mainTxt")

                
                self.mainText.delete("1.0", END)
                self.mainText.insert("1.0", "\n".join(copy))

            with open(os.path.join(self.dataPath, "archive.txt"), "w") as f: 
                f.truncate(0)
                f.close()
            self.yt_download_win.outRedir.old_stdout.write(f"Finished run {a+1}\n")
            if a < run - 1: print("------------\n------------")
        self.running=False
        try:
            toDisable.config(state=NORMAL)
        except:
            print("Process unfinished... Window closed early")
        else:
            self.yt_download_win.percent.set("All videos downloaded successfully (window may be closed)")
            print("Process finished successfully\nWindow may be closed...", end="")
            messagebox.showinfo("Download finished", "Download finished successfully", parent=self.yt_download_win)
        
    def get_items(self, urn):
        """This gathers items to be downloaded based on the specified search query or url (youtube and spotify only)
        <search> May be a search query for youtube e.g. 'Smash mouth All star' or a youtube/spotify url e.g. 'https://open.spotify.com/track/3cfOd4CMv2snFaKAnMdnvK?si=Ig6gRcMRS_aK7qMasRM0AQ' or 'https://open.spotify.com/playlist/4O9mmcH1OQ9azGfJPe4lMn?si=CwFHUVWxTXO8nkE9swBl0A'
        Accepts: [youtube or spotify urls, youtube searches]
        URL types: [spotify track, playlist, artist, album, podcast episode or podcast show urls]
        Returns: False for errors or the list of search queries"""
        if "spotify.com" in urn:
            self.log_debug("Is spotify url")
            self.log_debug(urn)
            if "track" in urn:
                try:
                    results = self.spotify.track(urn, market="from_token")
                except:
                    print(f"Couldn't find the requested track (Invalid track url/uri - {urn})")
                    return
                return [f"{results['name']} {results['artists'][0]['name']}"]
            elif "playlist" in urn:
                try:
                    results = self.spotify.playlist_items(urn, fields="items(track)", market="from_token")
                except:
                    print(f"Couldn't find the requested playlist (Invalid playlist url/uri - {urn})")
                    return
                return [f"{track['track']['name']} {track['track']['artists'][0]['name']}" for track in results['tracks']['items']]
            elif "artist" in urn:
                try:
                    results = self.spotify.artist_top_tracks(urn, country="from_token")
                except:
                    print(f"Couldn't find the requested artist (Invalid artist url/uri - {urn})")
                    return
                return [f"{track['name']} {track['artists'][0]['name']}" for track in results['tracks']]
            elif "album" in urn:
                try:
                    results = self.spotify.album_tracks(urn, market="from_token")
                except:
                    print(f"Couldn't find the requested album (Invalid album url/uri - {urn})")
                    return
                return [f"{track['name']} {track['artists'][0]['name']}" for track in results['items']]
            elif "episode" in urn:
                try:
                    results = self.spotify.episode(urn)
                except:
                    print(f"Couldn't find the requested episode (Invalid episode url/uri - {urn})\nOr Episode wasn't available in your market.")
                    return
                return [f"{results['name']} {results['show']['name']}"]
            elif "show" in urn:
                try:
                    results = self.spotify.show(urn)
                except:
                    print(f"Couldn't find the requested show (Invalid show url/uri - {urn})")
                    return
                return [f"{episode['name']} {results['name']}" for episode in results['episodes']['items']]
        else:
            print("Invalid url")
            return

    def start_time(self):
        self.time_window.outText.delete("1.0", END)
        messagebox.showwarning("Starting Duration Scan", "Please don't close until scan is finished.", parent=self.time_window)
        print("Please be patient while the scan runs...")
        l = self.stats.folder_length()
        self.disable_insert(self.time_window.outText, "1.0", f"Total folder duration for {self.appConfig['dir']}:\n{l['hours']}hrs, {l['minutes']}mins, {l['seconds']}secs\n\nLogs:\n")
        self.time_window.outText.see("1.0")
        messagebox.showinfo("Completed Duration Scan!", f"Total folder duration for {self.appConfig['dir']}:\n{l['hours']}hrs, {l['minutes']}mins, {l['seconds']}secs", parent=self.time_window)
    

    @staticmethod
    def add_to_queue(l: list, value: Any):
        l.pop(0)
        l.append(value)

    def options_win(self):
        self.oWin = Toplevel(self)
        self.oWin.title("Download Options")
        self.oWin.config(bg=self.backgrounds[self.appConfig['prefs']['theme']])
        self.oWin.iconbitmap(self.relative_path("Resources\\YTDLv2_256.ico"))
        def update_opts(arg=None):
            self.appConfig['opts']['description'] = descr.get()
            self.appConfig['opts']['subtitles'] = subti.get()
            self.appConfig['opts']['metadata'] = metad.get()
            self.appConfig['opts']['thumbnail'] = thumb.get()
            self.appConfig['opts']['audio'] = audio.get()
            self.appConfig['opts']['resolution'] = int(resolBox.get())
            self.write_config()
        descr = BooleanVar(self.oWin, value=self.appConfig['opts']['description'])
        descrBox = ttk.Checkbutton(self.oWin, variable=descr, command=update_opts, text=" - Download .description file")
        subti = BooleanVar(self.oWin, value=self.appConfig['opts']['subtitles'])
        subtiBox = ttk.Checkbutton(self.oWin, variable=subti, command=update_opts, text=" - Embed subtitles")
        thumb = BooleanVar(self.oWin, value=self.appConfig['opts']['thumbnail'])
        thumbBox = ttk.Checkbutton(self.oWin, variable=thumb, command=update_opts, text=" - Embed Thumbnail")
        metad = BooleanVar(self.oWin, value=self.appConfig['opts']['metadata'])
        metadBox = ttk.Checkbutton(self.oWin, variable=metad, command=update_opts, text=" - Add metadata")
        audio = BooleanVar(self.oWin, value=self.appConfig['opts']['audio'])
        audioBox = ttk.Checkbutton(self.oWin, variable=audio, command=update_opts, text=" - Extract audio")
        resolFrm = ttk.Frame(self.oWin)
        resolLbl = ttk.Label(resolFrm, text=" - Max resolution")
        resolBox = ttk.Spinbox(resolFrm, values=[480, 720, 1080, 2160], command=update_opts)
        resolBox.set(self.appConfig['opts']['resolution'])
        descrBox.grid(column=0, row=0, sticky=NW)
        subtiBox.grid(column=0, row=1, sticky=NW)
        thumbBox.grid(column=0, row=2, sticky=NW)
        metadBox.grid(column=0, row=3, sticky=NW)
        audioBox.grid(column=0, row=4, sticky=NW)
        resolFrm.grid(column=0, row=5, sticky=NW)
        resolBox.grid(column=0, row=0)
        resolLbl.grid(column=1, row=0)
        ttk.Label(self.oWin, text="NOTE: Some options may cause undesirable behaviours on platforms other than YT.\nE.g. twitch's description is the stream JSON.").grid(column=0, row=5)
    def update_theme(self, theme):
        ttk.Style().theme_use(theme)
        self.set_theme(theme, self.backgrounds[theme], self.backgrounds[theme])
        self.config(bg=self.backgrounds[self.appConfig['prefs']['theme']])
        try:
            self.mainText.config(bg=self.backgrounds[theme])
        except:
            pass
        try: 
            self.yt_download_win.config(bg=self.backgrounds[theme])
            self.yt_download_win.outText.config(bg=self.backgrounds[theme])
        except:
            pass
        try: 
            self.oWin.config(bg=self.backgrounds[theme])
        except:
            pass
        try: 
            self.time_window.config(bg=self.backgrounds[theme])
        except:
            pass
        try:
            self.pWin.config(bg=self.backgrounds[theme])
        except:
            pass
    def prefs_win(self):
        self.pWin = Toplevel(self)
        self.pWin.title("Preferences")
        self.pWin.config(bg=self.backgrounds[self.appConfig['prefs']['theme']])
        self.pWin.iconbitmap(self.relative_path("Resources\\YTDLv2_256.ico"))
        def warn_para(arg=None):
            update_prefs()
            if para.get(): messagebox.showwarning("Parallel Download Warning", "Downloading in parallel may affect output readability", parent=self.pWin)
        def update_prefs(arg=None):
            self.appConfig['prefs']['parallel'] = para.get()
            self.appConfig['prefs']['print_log'] = log.get()
            self.appConfig['prefs']['theme'] = theme.get()
            self.appConfig['prefs']['verbosity'] = verb.get()
            self.appConfig['prefs']['rerun'] = rerun.get()
            self.appConfig['prefs']['update_launch'] = checkUp.get()
            self.appConfig['prefs']['remove_success'] = rem.get()
            self.appConfig['prefs']['disable_stats'] = disStat.get()
            self.appConfig['prefs']['disable_percentage'] = disPerc.get()
            self.update_theme(theme.get())
            self.write_config()
        def reset_prefs(arg=None):
            self.appConfig['prefs'] = {"font": self.appConfig['prefs']['font'], "parallel": False, "print_log": True, "theme": "vista", "verbosity": False, "remove_success": False, "rerun": False, "outwin_mode": 0, "update_launch": True, "disable_stats": False, "disable_percentage": False}
            para.set(self.appConfig['prefs']['parallel'])
            theme.set(self.appConfig['prefs']['theme'])
            log.set(self.appConfig['prefs']['print_log'])
            verb.set(self.appConfig['prefs']['verbosity'])
            rerun.set(self.appConfig['prefs']['rerun'])
            checkUp.set(self.appConfig['prefs']['update_launch'])
            rem.set(self.appConfig['prefs']['remove_success'])
            disStat.set(self.appConfig['prefs']['disable_stats'])
            disPerc.set(self.appConfig['prefs']['disable_percentage'])
            self.update_theme(theme.get())
            self.write_config()
        resetBtn = ttk.Button(self.pWin, text="Reset Prefs", command=reset_prefs)
        resetBtn.pack(side=BOTTOM)
        prefBook = ttk.Notebook(self.pWin)
        prefBook.enable_traversal()
        prefBook.pack(side=TOP, expand=True, fill=BOTH)
        pFrm = ttk.Frame(prefBook)
        pFrm.pack(expand=True, fill=BOTH, side=TOP)
        para = BooleanVar(self.pWin, value=self.appConfig['prefs']['parallel'])
        paraBox = ttk.Checkbutton(pFrm, variable=para, command=warn_para, text=" - Download in parallel (Much Faster, lower readability)")
        log = BooleanVar(self.pWin, value=self.appConfig['prefs']['print_log'])
        logBox = ttk.Checkbutton(pFrm, variable=log, command=update_prefs, text=" - Print download log to output (defaults to console window)")
        checkUp = BooleanVar(self.pWin, value=self.appConfig['prefs']['verbosity'])
        checkUpBox=ttk.Checkbutton(pFrm, variable=checkUp, command=update_prefs, text=" - Check for updates on app launch")

        themeFrm = ttk.Frame(pFrm)
        theme = StringVar(self.pWin, value=self.appConfig['prefs']['theme'])
        themeBox = ttk.OptionMenu(themeFrm, theme, theme.get(), 'adapta', 'alt', 'aquativo', 'arc', 'awarc', 'awblack', 'awbreeze', 'awbreezedark', 'awclearlooks', 'awdark', 'awlight', 'awtemplate', 'awwinxpblue', 'black', 'blue', 'breeze', 'clam', 'classic', 'clearlooks', 'default', 'elegance', 'equilux', 'itft1', 'keramik', 'kroc', 'plastik', 'radiance', 'scidblue', 'scidgreen', 'scidgrey', 'scidmint', 'scidpink', 'scidpurple', 'scidsand', 'smog', 'ubuntu', 'vista', 'winnative', 'winxpblue', 'xpnative', 'yaru', command=update_prefs)
        paraBox.grid(column=0, row=0, sticky=NW)
        logBox.grid(column=0, row=1, sticky=NW)
        checkUpBox.grid(column=0, row=2, sticky=NW)
        themeFrm.grid(column=0, row=3, sticky=NW)
        themeBox.grid(column=0, row=0, sticky=NW)
        ttk.Label(themeFrm, text=" - Theme").grid(column=1, row=0, sticky=NW)
        prefBook.add(pFrm, text="General", underline=0)

        advFrm = ttk.Frame(prefBook, relief=FLAT)
        advFrm.pack(expand=True, fill=BOTH, side=TOP, padx=2.5)
        verb = BooleanVar(self.pWin, value=self.appConfig['prefs']['verbosity'])
        verbBox = ttk.Checkbutton(advFrm, variable=verb, command=update_prefs, text=" - Add download verbosity (Shows extra info in output window)")
        rerun = BooleanVar(self.pWin, value=self.appConfig['prefs']['rerun'])
        rerunBox = ttk.Checkbutton(advFrm, variable=rerun, command=update_prefs, text=" - Runs downloader twice as sometimes errors can occur in post processing")
        rem = BooleanVar(self.pWin, value=self.appConfig['prefs']['remove_success'])
        remBox = ttk.Checkbutton(advFrm, variable=rem, command=update_prefs, text=" - Remove successful downloads from list")
        disStat=BooleanVar(self.pWin, self.appConfig['prefs']['disable_stats'])
        disStatBox=ttk.Checkbutton(advFrm, variable=disStat, command=update_prefs, text=" - Disable download statistics (improves download speed)")
        disPerc=BooleanVar(self.pWin, value=self.appConfig['prefs']['disable_percentage'])
        disPercBox=ttk.Checkbutton(advFrm, variable=disPerc, command=update_prefs, text=" - Disable download percentage bar (still available in output, improves download speed)")
        verbBox.grid(column=0, row=0, sticky=NW)
        rerunBox.grid(column=0, row=1, sticky=NW)
        remBox.grid(column=0, row=2, sticky=NW)
        disStatBox.grid(column=0, row=3, sticky=NW)
        disPercBox.grid(column=0, row=4, sticky=NW)
        prefBook.add(advFrm, text="Advanced", underline=0)
    def bug(self):
        ans=messagebox.askyesnocancel("Report via email?", "Would you like to report a bug by email.\nYes: report by email\nNo: report on github", parent=self)
        if ans==True:
            os.startfile("mailto:16JohnA28@gmail.com")
            self.log_debug("Email report.")
        elif ans==False:
            os.startfile("https://github.com/MrTransparentBox/ytdl-gui/issues/new")
            self.log_debug("Github report.")
        else:
            self.log_debug("Cancelled report.")
    def font(self):
        Font_wm(Font=self.curr_font)
        self.font_to_list()
    def write_config(self):
        self.log_debug("Written config", True)
        with open(os.path.expandvars("%appdata%\\Youtube-dl_GUI\\appConfig.json"), "w") as f: 
            json.dump(self.appConfig, f)
            f.close()
    
    def relative_path(self, path: str):
        try:
            base = sys._MEIPASS
            res = os.path.abspath(os.path.join(base, path))
            if not os.path.exists(res): raise FileNotFoundError(f"File {res} isn't an existing runtime file.")
        except (AttributeError, FileNotFoundError):
            base = os.path.abspath(".")
            res = os.path.abspath(os.path.join(base, path))
            if not os.path.exists(res): raise FileNotFoundError(f"File {res} isn't an existing local file.")
        self.log_debug(f"GATHERED PATH: {str(res)}")
        return res
    @staticmethod
    def disable_insert(text: Text, index, chars, *args):
        text.config(state=NORMAL)
        text.insert(index, chars, args)
        text.config(state=DISABLED)

    def on_closing(self, event=None):
        try:
            self.font_to_list()
        except Exception as ex:
            self.log_debug(ex)
        if not self.saved:
            sv = messagebox.askyesnocancel("Save Changes?", "Do you want to save your changes?", parent=self)
            if sv == True:
                self.save()
                self.destroy()
                sys.exit(0)
            elif sv == False:
                self.destroy()
                sys.exit(0)
            elif sv == None:
                return
        else:
            self.destroy()
            sys.exit(0)
    def modified(self, event=None):
        if self.saved:
            self.saved=False
            self.title(f"*{self.title()}*")
        self.mainText.edit_modified(False)
    def font_to_list(self):
        self.appConfig['prefs']['font'] = [self.curr_font.actual("family"), self.curr_font.actual("size"), self.curr_font.actual("weight"), self.curr_font.actual("slant"), self.curr_font.actual("underline"), self.curr_font.actual("overstrike")]
        self.write_config()
class StderrRedirect(object):
    """A Class that redirects `sys.stderr` to itself and allows writing to a Tkinter `Text` widget.  

    Parametres:
    ----------
    `t` - The `Text` box to redirect to

    ----------
    !! ENSURE YOU USE `close()` TO RESET STDERR TO ITS ORIGINAL STATE !!"""
    def __init__(self, t: Text, interactive: bool = True, msgbox: bool = False, master=None):
        self.old_stderr = sys.stderr
        self.text_box = t
        self.interactive = interactive
        self.open=True
        self.master=master
        sys.stderr = self
        self.msgbox=msgbox
    def write(self, s: str):
        if self.msgbox and "warning" in s.lower():
            messagebox.showwarning("Warning", s, parent=self.master)
        elif self.msgbox and "error" in s.lower():
            messagebox.showerror("Error", s, parent=self.master)
        elif self.msgbox:
            messagebox.showinfo("Issue", s, parent=self.master)
        else:
            try:
                self.text_box.config(state=NORMAL)
                if s.startswith("\r"):
                    self.text_box.delete("end-1c linestart", "end")
                    self.text_box.insert(END, f"\n{s}")
                    self.text_box.see(END)
                else:
                    self.text_box.insert(END, s)
                    self.text_box.see(END)
                self.text_box.config(state=DISABLED)
            except (TclError, RuntimeError) as e:
                if "main thread is not in main loop" in str(e):
                    sys.exit(e)
                self.old_stderr.write(f"OLD: '{s}'\n")
                if self.open: self.close()
    def flush(self):
        pass
    def writelines(self, lines):
        self.text_box.config(state=NORMAL)
        self.text_box.insert(END, "\n".join(lines))
        self.text_box.see(END)
        self.text_box.config(state=DISABLED)
    def close(self):
        sys.stderr = self.old_stderr
        self.open=False
        del self
    def isatty(self):
        return self.interactive
class StdoutRedirect(object):
    """A Class that redirects `sys.stdout` to itself and allows writing to a Tkinter `Text` widget.  

    Parametres:
    ----------
    `t` - The `Text` box to redirect to
    
    ----------
    !! ENSURE YOU USE `close()` TO RESET STDOUT TO ITS ORIGINAL STATE !!"""
    def __init__(self, t: Text, interactive: bool = True):
        self.old_stdout = sys.stdout
        self.text_box = t
        self.interactive = interactive
        self.open=True
        sys.stdout = self
    def write(self, s: str):
        try:
            self.text_box.config(state=NORMAL)
            if s.startswith("\r"):
                self.text_box.delete("end-1c linestart", "end")
                self.text_box.insert(END, f"\n{s}")
                self.text_box.see(END)
            else:
                self.text_box.insert(END, s)
                self.text_box.see(END)
            self.text_box.config(state=DISABLED)
        except TclError:
            self.old_stdout.write(f"OLD: '{s}'\n")
            if self.open: self.close()
    def flush(self):
        pass
    def writelines(self, lines):
        self.text_box.config(state=NORMAL)
        self.text_box.insert(END, "\n".join(lines))
        self.text_box.see(END)
        self.text_box.config(state=DISABLED)
    def close(self):
        sys.stdout = self.old_stdout
        self.open=False
        del self
    def isatty(self):
        return self.interactive
class OutWin(Toplevel):
    def __init__(self, master: Application, mode: str, title="New window", geometry: str = "900x550", block=True, setGrab=True, deleteOnClose=1):
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
            self.outRedir = StdoutRedirect(self.outText)
            self.errRedir = StderrRedirect(self.outText, master=self)
        if self.mode == "yt":
            self.btnStart = ttk.Button(self, text="Start Download", command=self.task)
            self.yt_frm = ttk.Frame(self)
            self.progress = ttk.Progressbar(self.yt_frm, length=600, mode='determinate', maximum=1, value=0)
            self.progress.grid(column=0, row=0, padx=3)
            self.stat=StringVar(self.yt_frm, value="0MiB/0MiB @ 0MiB/s")
            ttk.Label(self.yt_frm, textvariable=self.stat, font=font.Font(size=14)).grid(column=1, row=0, padx=3)
            self.percent=StringVar(self.yt_frm, value=f"{self.progress['value']*100}%")
            ttk.Label(self.yt_frm, font=font.Font(size=10), textvariable=self.percent).grid(column=0, row=0)
            self.yt_frm.pack(side=TOP, pady=7.5)
        elif self.mode == "time":
            self.btnStart = ttk.Button(self, text="Start Duration Scan", command=self.task)
        else:
            print(f"mode '{self.mode}' incorrect")
        self.btnStart.pack(side=BOTTOM)
        self.textFrm.pack(side=TOP, expand=True, fill=BOTH)
        self.yScroll.pack(fill=Y, side=RIGHT)
        self.outText.pack(expand=True, fill=BOTH)
        self.iconbitmap(self.master.relative_path("Resources\\YTDLv2_256.ico"))
        self.protocol("WM_DELETE_WINDOW", self.outWin_close)
        self.focus_set()
        if self.setGrab: self.grab_set()
    def outWin_close(self, event=None):
        self.master: Application=self.master
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
            self.t = threading.Thread(target=self.master.yt_download, args=[self.btnStart, 2])
        elif self.mode == "yt":
            self.t = threading.Thread(target=self.master.yt_download, args=[self.btnStart])
        elif self.mode == "time":
            self.t = threading.Thread(target=self.master.start_time)
        else:
            print(f"mode '{self.mode}' incorrect")
            return
        self.t.start()
appVersion = "2023.05.01.f2"
notes = f"""Youtube-dl GUI v{appVersion}
- Removed missing themes
- Upgraded from youtube-dl to yt-dlp due to some issues
- Removed need to restart for theme application
- Improved theme handling to properly set background after restart
- Optimised progress hook for download speed
- Option to remove successful downloads now works
- Moved other classes into separate files
- Added instruction button in help"""
def main(args: argparse.Namespace):
    if args.notes:
        print(notes)
        sys.exit(0)
    if args.path == None:
        p = None
    elif not os.path.exists(os.path.abspath(args.path)):
        sys.exit(f"File {args.path} doesn't exist")
    else:
        p = os.path.abspath(args.path)
    if args.debug: print(sys.argv)
    app = Application("1080x600", args.debug, p, appVersion)
    try:
        app.mainloop()
    except RuntimeError as e:
        sys.exit(str(e))
