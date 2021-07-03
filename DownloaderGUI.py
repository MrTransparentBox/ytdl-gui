#!/usr/bin/env D:\propertyofalexjohnson\vscode\python\YTDL\.venv\Scripts\python.exe
import os, json, sys, threading, argparse, psutil
from youtube_dl import YoutubeDL
from ttkthemes import ThemedTk
from tkinter import messagebox, filedialog, ttk, font 
from tkinter import *
# TO-DO<---
#    ADD INNO COMPILE TO BUILD TASK (CTRL+SHIFT+B) THROUGH 'ISCC.exe' (INNO SETUP COMMAND COMPILER - C:\Program Files (x86)\Inno Setup 6) AND "..\..\Setup\YTDLGUI\VDLS-21.4.24.f3.iss"
#    UPLOAD TO GITHUB (https://github.com/MrTransparentBox/ytdl-gui) AND CREATE AN UPDATER FUNCTION.
#    ADD SPOTIFY SUPPORT FROM MY SOUNDDL PROGRAM
#    MAKE SMALLER BY JUST USING IMAGIO_FFMPEG/BINARIES RATHER THAN INDEPENTENT INSTALL.
#    ADD MORE DOWNLOAD OPTIONS, E.G. AUDIO-ONLY (INCLUDING ADVANCED OPTIONS TAB WITH TTK.NOTEBOOK)
#    CHECK FOR BUGS
class Font_wm(Toplevel):
    def __init__(self, Font=None):
        Toplevel.__init__(self)
        self.mainfont=Font
        self.title('Font ...')

        self.var=StringVar()# For Font Face
        self.var.set(self.mainfont.actual('family'))
        self.var1=IntVar()  # for Font Size
        self.var1.set(self.mainfont.actual('size'))
        self.var2=StringVar() # For Bold
        self.var2.set(self.mainfont.actual('weight'))
        self.var3=StringVar() # For Italic
        self.var3.set(self.mainfont.actual('slant'))
        self.var4=IntVar()# For Underline
        self.var4.set(self.mainfont.actual('underline'))
        self.var5=IntVar() # For Overstrike
        self.var5.set(self.mainfont.actual('overstrike'))

        self.font_1=font.Font()
        for i in ['family', 'weight', 'slant', 'overstrike', 'underline', 'size']:
            self.font_1[i]=self.mainfont.actual(i)

        # Function
        def checkface(event=None):
            try:
                self.var.set(str(self.listbox.get(self.listbox.curselection())))
                self.font_1.config(family=self.var.get(), size=self.var1.get(), weight=self.var2.get(), slant=self.var3.get(), underline=self.var4.get(), overstrike=self.var5.get())
            except Exception as ex:
               pass
        def checksize(event=None):
            try:
                self.var1.set(int(self.size.get(self.size.curselection())))
                self.font_1.config(family=self.var.get(), size=self.var1.get(), weight=self.var2.get(), slant=self.var3.get(), underline=self.var4.get(), overstrike=self.var5.get())
            except Exception as ex:
                pass
        def checkstyle(event=None):
            try:
                self.font_1.config(family=self.var.get(), size=self.var1.get(), weight=self.var2.get(), slant=self.var3.get(), underline=self.var4.get(), overstrike=self.var5.get())
            except Exception as ex:
                pass
        def applied():
            self.result=(self.var.get(), self.var1.get(), self.var2.get(), self.var3.get(), self.var4.get(), self.var5.get())
            self.mainfont['family']=self.var.get()
            self.mainfont['size']=self.var1.get()
            self.mainfont['weight']=self.var2.get()
            self.mainfont['slant']=self.var3.get()
            self.mainfont['underline']=self.var4.get()
            self.mainfont['overstrike']=self.var5.get()
        def out():
            self.result=(self.var.get(), self.var1.get(), self.var2.get(), self.var3.get(), self.var4.get(), self.var5.get())
            self.mainfont['family']=self.var.get()
            self.mainfont['size']=self.var1.get()
            self.mainfont['weight']=self.var2.get()
            self.mainfont['slant']=self.var3.get()
            self.mainfont['underline']=self.var4.get()
            self.mainfont['overstrike']=self.var5.get()
            # applied()
            self.destroy()
        def end():
            self.result=None
            self.destroy()
            
        self.mainwindow=ttk.Frame(self)
        self.mainwindow.pack(padx=10, pady=10)

        self.mainframe=ttk.Frame(self.mainwindow)
        self.mainframe.pack(side='top',ipady=30, ipadx=30,expand='no', fill='both')
        self.mainframe0=ttk.Frame(self.mainwindow)
        self.mainframe0.pack(side='top', expand='yes', fill='x', padx=10, pady=10)
        self.mainframe1=ttk.Frame(self.mainwindow)
        self.mainframe1.pack(side='top',expand='no', fill='both')
        self.mainframe2=ttk.Frame(self.mainwindow)
        self.mainframe2.pack(side='top',expand='yes', fill='x', padx=10, pady=10)
        # Frame in [  main frame]
        self.frame=ttk.LabelFrame(self.mainframe, text='Select Font Face')
        self.frame.pack(side='left', padx=10, pady=10, ipadx=20, ipady=20, expand='yes', fill='both')
        self.frame1=ttk.LabelFrame(self.mainframe, text='Select Font size')
        self.frame1.pack(side='left', padx=10, pady=10, ipadx=20, ipady=20, expand='yes', fill='both')
        self.famEnt=ttk.Entry(self.frame, textvariable=self.var)
        self.famEnt.pack(side='top', padx=5, pady=5, expand='yes', fill='x')
        self.listbox=Listbox(self.frame, bg='gray70')
        self.listbox.pack(side='top', padx=5, pady=5, expand='yes', fill='both')
        fams = list(font.families())
        fams.sort()
        for i in fams:
            self.listbox.insert(END, i)

        # Frame in [ 0. mainframe]
        self.bold=ttk.Checkbutton(self.mainframe0, text='Bold', onvalue='bold', offvalue='normal', variable=self.var2, command=checkstyle)
        self.bold.pack(side='left',expand='yes', fill='x')
        self.italic=ttk.Checkbutton(self.mainframe0, text='Italic', onvalue='italic', offvalue='roman',variable=self.var3, command=checkstyle)
        self.italic.pack(side='left', expand='yes', fill='x')
        self.underline=ttk.Checkbutton(self.mainframe0, text='Underline',onvalue=1, offvalue=0, variable=self.var4, command=checkstyle)
        self.underline.pack(side='left', expand='yes', fill='x')
        self.overstrike=ttk.Checkbutton(self.mainframe0, text='Overstrike',onvalue=1, offvalue=0, variable=self.var5, command=checkstyle)
        self.overstrike.pack(side='left', expand='yes', fill='x')
        
        # Frame in [ 1. main frame]
        self.sizeEnt=ttk.Entry(self.frame1, textvariable=self.var1)
        self.sizeEnt.pack(side='top', padx=5, pady=5, expand='yes', fill='x')
        self.size=Listbox(self.frame1, bg='gray70')
        self.size.pack(side='top', padx=5, pady=5, expand='yes', fill='both')
        for i in range(30):
            self.size.insert(END, i)

        ttk.Label(self.mainframe1, text='''\nABCDEabcde12345\n''', font=self.font_1).pack(expand='no', padx=10,pady=10)
        # Frame in [ 2. mainframe]
        ttk.Button(self.mainframe2, text='   OK   ', command=out).pack(side='left', expand='yes', fill='x', padx=5, pady=5)
        ttk.Button(self.mainframe2, text=' Cancel ', command=end).pack(side='left', expand='yes', fill='x', padx=5, pady=5)
        ttk.Button(self.mainframe2, text=' Apply  ', command=applied).pack(side='left', expand='yes', fill='x', padx=5, pady=5)
        
        self.listbox.bind('<<ListboxSelect>>', checkface)
        self.size.bind('<<ListboxSelect>>', checksize)
class GetStats():
    """Gets basic stats about a file or folder. Only folder video contents lenth currently.
    
    Parametres
    ------------
    pathname: str
      The folder path to get statistics for.
        Can include shell variables in form of '$var', '${var}' and '%var%'
    
    quiet: bool
      If True, suppresses non-vital messages
      
    silent: bool
      If True, supresses all messages"""
    def __init__(self, pathname, quiet=False, silent=False):
        self.pathname = os.path.realpath(os.path.expandvars(pathname))
        self.quiet = quiet
        self.silent = silent
        self.lis = []
        self.takeTime = False
        self.__dots__ = 0
    def write(self, text: str, long=0, importance=0):
        stages = ["|", "/", "-", "\\"]
        if not self.quiet or (importance == 1 and self.silent == False):
            print(text)
        elif self.silent and importance > 1:
            print(text)
        elif self.silent and importance <= 1:
            pass
        elif self.quiet and long == 1:
            self.__dots__ = 0
            print("Processing", end="")
        elif self.quiet and long == 2:
            self.__dots__ += 1
            print(f"\rProcessing  {stages[self.__dots__%4]}", end="")
                
    def get_length(self, filename):
        if not os.path.exists(filename): return None
        from moviepy.editor import VideoFileClip
        try:
            vid = VideoFileClip(filename)
            dur = vid.duration
        except Exception as ex:
            sys.exit(f"vv Error occurred getting video duration vv.\n\n{str(ex)}\n")
        return dur
    def folder_length(self) -> dict:
        sDir = self.pathname
        tlis = os.listdir(sDir)
        for i in tlis:
            if (i.endswith(".mp4") or i.endswith(".mov") or i.endswith(".mkv") or i.endswith(".webm") or i.endswith(".avi")) and i.count(".temp") == 0:
                self.lis.append(i)
        self.write("Gathered folder contents.")
        totTime=0
        self.write("<Video name>: <seconds.microseconds>\n\n--------------------", 1)
        for i in self.lis:
            t = self.get_length(os.path.join(self.pathname, i))
            if t == None: continue
            self.write(f"{i}: {t}s\n--------------------", 2)
            totTime += t
        seconds=totTime%60
        minutes=int((totTime/60)%60)
        hours=int(totTime/3600)
        self.write(f"Total video time: {hours}h:{minutes}m:{seconds}s\n\n", importance=1)
        return {"hours": hours, "minutes": minutes, "seconds": seconds}

class Application(ThemedTk):
    """Base application window and functions for the Youtube-dl GUI

    Parametres
    ------
        - `title`: str - The title of the window
        - `size`: str - Form of "``x_size``x``y_size``"
        - `debug`: bool - Whether to put the app in debug mode. Prints additional info.
        - `path`: str - `os.path` like string determining the path of the `.ytdl` or other file to open. Leave as ```None``` for default `ToDownload.ytdl` file
    """
    def __init__(self, title, size, debug=False, path=None):
        print("Loading preferences and settings...")
        self.appConfig = {}
        self.running=False
        self.debug=debug
        self.path=path

        self.exe = bool(getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"))
        if self.path == None:
            self.path = self.relative_path("ToDownload.ytdl")
        elif not (os.path.exists(self.path) and os.path.isfile(self.path) and (str(self.path).endswith(".ytdl") or str(self.path).endswith(".vdl"))):
            raise OSError("File specified must be an existing file of type .ytdl (or .vdl for legacy files)")

        with open(self.path, "r") as f:
            if self.debug: print(f"File is {self.path}  ||  Encoding is {f.encoding}")
            f.close()
        with open(self.relative_path("appConfig.json"), "r") as f:
            self.appConfig = json.load(f)
            f.close()
        if self.appConfig['prefs']['font'] == []:
            self.appConfig['prefs']['font'] = ["Arial", 14, "normal", "roman", 0, 0]
        self.backgrounds = {'adapta': '#FAFBFC', 'alt': '#D9D9D9', 'aquativo': '#FAFAFA', 'arc': '#F5F6F7', 'awarc': '#F5F6F7', 'awblack': '#424242', 'awbreeze': '#EFF0F1', 'awbreezedark': '#2F3336', 'awclearlooks': '#EFEBE7', 'awdark': '#33393B', 'awlight': '#E8E8E7', 'awtemplate': '#424242', 'awwinxpblue': '#ECE9D8', 'black': '#424242', 'blue': '#6699CC', 'breeze': '#EFF0F1', 'clam': '#DCDAD5', 'classic': '#D9D9D9', 'clearlooks': '#EFEBE7', 'default': '#D9D9D9', 'elegance': '#D8D8D8', 'equilux': '#464646', 'itft1': '#DAEFFD', 'keramik': '#CCCCCC', 'kroc': '#FCB64F', 'plastik': '#EFEFEF', 'radiance': '#EFEFEF', 'scidblue': '#D8D8D8', 'scidgreen': '#D8D8D8', 'scidgrey': '#D8D8D8', 'scidmint': '#D8D8D8', 'scidpink': '#D8D8D8', 'scidpurple': '#D8D8D8', 'scidsand': '#D8D8D8', 'smog': '#E7EAF0', 'ubuntu': '#F6F4F2', 'vista': '#F0F0F0', 'winnative': '#F0F0F0', 'winxpblue': '#ECE9D8', 'xpnative': '#F0F0F0', 'yaru': '#F0F0F0'}
        ThemedTk.__init__(self, theme=self.appConfig['prefs']['theme'], toplevel=self.backgrounds[self.appConfig['prefs']['theme']], themebg=self.backgrounds[self.appConfig['prefs']['theme']])
        self.tk.call('lappend', 'auto_path', self.relative_path('awthemes-10.3.0'))
        self.tk.call('package', 'require', 'awthemes')
        self.tk.call('lappend', 'auto_path', self.relative_path('tksvg0.7'))
        self.tk.call('package', 'require', 'tksvg')
        self.availThemes = ['adapta', 'alt', 'aquativo', 'arc', 'awarc', 'awblack', 'awbreeze', 'awbreezedark', 'awclearlooks', 'awdark', 'awlight', 'awtemplate', 'awwinxpblue', 'black', 'blue', 'breeze', 'clam', 'classic', 'clearlooks', 'default', 'elegance', 'equilux', 'itft1', 'keramik', 'kroc', 'plastik', 'radiance', 'scidblue', 'scidgreen', 'scidgrey', 'scidmint', 'scidpink', 'scidpurple', 'scidsand', 'smog', 'ubuntu', 'vista', 'winnative', 'winxpblue', 'xpnative', 'yaru']
        ths = self.get_themes()
        ths.sort()
        if self.debug: print(f"THEMES PRESENT: {ths == self.availThemes}"); print(f"EXE: {self.exe}")
        if ths != self.availThemes:
            difference=list(set(ths) ^ set(self.availThemes))
            messagebox.showerror("Themes unavailable", f"The themes: {difference} aren't available\nThis may require a reinstall of the software to fix this issue.\nOtherwise, please report an issue.", parent=self)
            sys.exit(f"Themes: {', '.join(difference)} \nare unavailable")
        del ths
        del self.availThemes
        self.update_theme(self.appConfig['prefs']['theme'])
        self.config(background=self.backgrounds[self.appConfig['prefs']['theme']])
        if str(self.appConfig["dir"]).strip() == "":
            ans = filedialog.askdirectory(parent=self, title="Select Download Directory...")
            if ans.strip() == "":
                sys.exit("No Directory given...")
            else:
                self.appConfig["dir"] = os.path.abspath(ans)
        self.title(f"{title} - {str(self.appConfig['dir'])}")
        self.iconbitmap(self.relative_path("Resources\\TransparentBox_1-1.ico"))
        self.geometry(size)
        self.saved = False
        confont = self.appConfig['prefs']['font']
        self.currFont = font.Font(family=confont[0], size=confont[1], weight=confont[2], slant=confont[3], underline=confont[4], overstrike=confont[5])
        self.writeConfig()
        self.btnFrm = ttk.Frame(self)
        self.btnFrm.pack(side=BOTTOM, fill=X, expand=True)
        ttk.Frame(self.btnFrm).grid(row=0, column=0)
        mid = ttk.Frame(self.btnFrm)
        mid.grid(row=0, column=1)
        self.ytButton=ttk.Button(mid, text="Start Download...", command=self.ytWin)
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
        self.mainText = Text(self.textFrame, xscrollcommand=self.xScroll.set, yscrollcommand=self.yScroll.set, relief=FLAT, font=self.currFont)
        self.yScroll.config(command=self.mainText.yview)
        self.xScroll.config(command=self.mainText.xview)
        insStr = []
        with open(self.path, "r", encoding="utf-8") as f:
            try:
                insStr = f.readlines()
            except UnicodeDecodeError as ex:
                messagebox.showerror("Bad encoding", "The encoding of the file couldn't isn't utf-8 or ansi", parent=self)
                sys.exit("The encoding of the file couldn't isn't utf-8 or ansi")
            f.close()
        if len(insStr) > 0:
            if type(insStr[0]) == bytes: insStr = [i.decode("utf-8") for i in insStr]
            if insStr[-1][-1:] == "\n": insStr[-1] = insStr[-1][:-1]
        self.mainText.insert("1.0", "".join(insStr))
        self.textFrame.pack(side=TOP, expand=True, fill=BOTH, padx=5)
        self.yScroll.pack(side=RIGHT, fill=Y)
        self.xScroll.pack(side=BOTTOM, fill=X)
        self.mainText.pack(side=TOP, expand=True, fill=BOTH)
        self.menu = Menu(self, relief=FLAT)

        self.fileMenu=Menu(self.menu, tearoff=0)
        self.fileMenu.add_command(label="New (CTRL+N)", command=self.new)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Save (CTRL+S)", command=self.save)
        self.fileMenu.add_command(label="Save As (CTRL+SHIFT+S)...", command=self.saveAs)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Preferences...", command=self.prefs_win)

        self.viewMenu = Menu(self.menu, tearoff=0)
        self.viewMenu.add_command(label="Font...", command=self.font)

        self.toolMenu=Menu(self.menu, tearoff=0)
        self.toolMenu.add_command(label="Current File", command=self.currFile)
        self.toolMenu.add_command(label="Current Directory", command=self.currDir)
        self.toolMenu.add_command(label="Change Directory...", command=self.cDir)
        self.toolMenu.add_separator()
        self.toolMenu.add_command(label="Duration Scan...", command=self.time)
        self.toolMenu.add_separator()
        self.toolMenu.add_command(label="Download Options...", command=self.options_win)
        self.stats=None

        self.helpMenu=Menu(self.menu, tearoff=0)
        self.helpMenu.add_command(label="About...", command=self.about)
        self.helpMenu.add_command(label="Report Bug", command=self.bug)

        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.menu.add_cascade(label="View", menu=self.viewMenu)
        self.menu.add_cascade(label="Tools", menu=self.toolMenu)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)
        self.config(menu=self.menu)

        self.bind_all("<Control-n>", self.new)
        self.bind_all("<Control-s>", self.save)
        self.mainText.bind("<<Modified>>", self.modified)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def relative_path(self, path: str):
        try:
            base = sys._MEIPASS
            res = os.path.abspath(os.path.join(base, path))
            if not os.path.exists(res): raise FileNotFoundError(f"File {res} isn't an existing runtime file.")
        except (AttributeError, FileNotFoundError) as ex:
            base = os.path.abspath(".")
            res = os.path.abspath(os.path.join(base, path))
            if not os.path.exists(res): raise FileNotFoundError(f"File {res} isn't an existing local file.")
        if self.debug: print(f"GATHERED PATH: {str(res)}")
        return res
    def disableInsert(self, text: Text, index, chars, *args):
        text.config(state=NORMAL)
        text.insert(index, chars, args)
        text.config(state=DISABLED)
    def new(self, event=None):
        if self.ask_save() == "cancel": return
        self.mainText.delete("1.0", END)
        self.path=None
        self.save()
    def ask_save(self):
        if not self.saved:
            sv = messagebox.askyesnocancel("Save Changes?", "Do you want to save your changes?", parent=self)
            if sv == True:
                self.save()
            elif sv == False:
                return "continue"
            elif sv == None:
                return "cancel"
    def save(self, event=None):
        if self.path == None:
            self.saveAs()
            return
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(self.mainText.get("1.0", END))
            f.close()
        self.saved=True
        self.title(self.title().replace("*", ""))
    def saveAs(self, event=None):
        ans = filedialog.asksaveasfilename(confirmoverwrite=True, defaultextension=".ytdl", initialfile="downloads.ytdl", filetypes=[("Youtube-dl File (*.ytdl)", "*.ytdl"), ("Legacy Downloader File (*.vdl)", "*.vdl")], title="Save As...", parent=self)
        if not ans: return
        self.path = os.path.abspath(ans)
        self.save()
    def currDir(self):
        messagebox.showinfo("Current Directory", f"Current directory is: {self.appConfig['dir']}", parent=self)
    def currFile(self):
        messagebox.showinfo("Current File", f"Current file is: {self.path}", parent=self)
    def cDir(self):
        ans = filedialog.askdirectory(parent=self)
        if ans.strip() != "":
            self.appConfig['dir'] = os.path.abspath(ans)
        self.writeConfig()
        self.title(f"Youtube-dl GUI - {str(self.appConfig['dir'])}")
    def time(self):
        if hasattr(self, "timeWindow"):
            self.timeWindow.deiconify()
            if self.timeWindow.setGrab: self.timeWindow.grab_set()
            if self.debug: print("Unwithdrawn time win")
        else:
            self.timeWindow = OutWin(self, "time", f"List Time Output - {self.appConfig['dir']}", block=False, deleteOnClose=self.appConfig['prefs']['outwin_mode'])
            if self.debug: print("Created time win")
        if not hasattr(self, "stats"):
            self.stats = GetStats(self.appConfig['dir'])
    def ytWin(self):
        if self.ask_save() == "cancel": return
        if self.path == None: messagebox.showerror("No open file", "Must have an open .ytdl file before download", parent=self)
        if hasattr(self, "ytDownloadWin"):
            self.ytDownloadWin.deiconify()
            if self.ytDownloadWin.setGrab: self.ytDownloadWin.grab_set()
            if self.debug: print("Unwithdrawn yt win")
        else:
            self.ytDownloadWin = OutWin(self, "yt", f"Download Output - {self.appConfig['dir']}", block=False, setGrab=True, deleteOnClose=self.appConfig['prefs']['outwin_mode'])
            if self.debug: print("Created yt win")
    def startTime(self):
        self.timeWindow.outText.delete("1.0", END)
        messagebox.showwarning("Starting Duration Scan", "Please don't close until scan is finished.", parent=self.timeWindow)
        print("Please be patient while the scan runs...")
        l = self.stats.folder_length()
        self.disableInsert(self.timeWindow.outText, "1.0", f"Total folder duration for {self.appConfig['dir']}:\n{l['hours']}hrs, {l['minutes']}mins, {l['seconds']}secs\n\nLogs:\n")
        self.timeWindow.outText.see("1.0")
        messagebox.showinfo("Completed Duration Scan!", f"Total folder duration for {self.appConfig['dir']}:\n{l['hours']}hrs, {l['minutes']}mins, {l['seconds']}secs", parent=self.timeWindow)
    def ytDownload(self, toDisable: ttk.Button, run=1):
        toDisable.config(state=DISABLED)
        def progress_hook(d):
            if d['status'] == 'finished':
                try:
                    print(f"Finished downloading {d['total_bytes']} bytes in {d['elapsed']} seconds")
                except:
                    print("Download finished")
                finally:
                    self.ytDownloadWin.progress['value'] = 0
            elif d['status'] == 'downloading':
                try:
                    self.ytDownloadWin.progress['value'] = d['downloaded_bytes'] / d['total_bytes']
                except Exception as e:
                    self.ytDownloadWin.errRedir.old_stderr.write(f"WARNING: Progess bar unavailable; {e}")
        opts = {"default_search": "auto", 
        "outtmpl": f"{self.appConfig['dir']}\\%(upload_date)s--%(title)s.%(ext)s",
        "format": f"bestvideo[height<=?{self.appConfig['opts']['resolution']}][ext=mp4]+bestaudio[ext=m4a]/best[height<=?{self.appConfig['opts']['resolution']}][ext=mp4]/best[ext=mp4]/best", 
        "ffmpeg_location": self.relative_path("ffmpeg-20200115-0dc0837-win64-static\\bin"),
        "cookiefile": self.relative_path("Logs\\cookies.txt"),
        "writethumbnail": self.appConfig['opts']['thumbnail'], 
        "embedthumbnail": self.appConfig['opts']['thumbnail'], 
        "writesubtitles": self.appConfig['opts']['subtitles'], 
        "writeautomaticsub": self.appConfig['opts']['subtitles'], 
        "embedsubtitles": self.appConfig['opts']['subtitles'], 
        'writedescription': self.appConfig['opts']['description'],
        "addmetadata": self.appConfig['opts']['metadata'], 
        "retries": 2, 
        "ignoreerrors": True,
        "download_archive": self.relative_path("Logs\\archive.txt"), 
        "progress_hooks": [progress_hook], 
        "postprocessors": [],
        "verbose": self.appConfig['prefs']['verbosity']}
        if self.appConfig['opts']['metadata']: opts['postprocessors'].append({'key': 'FFmpegMetadata'})
        if self.appConfig['opts']['thumbnail']: opts['postprocessors'].append({'key': 'EmbedThumbnail', 'already_have_thumbnail': False, "atomic_path": self.relative_path("AtomicParsley-win32-0.9.0/AtomicParsley.exe")})#"./AtomicParsley-win32-0.9.0/AtomicParsley.exe"})
        if self.appConfig['opts']['subtitles']: opts['postprocessors'].append({'key': 'FFmpegEmbedSubtitle'})
        ytdl = YoutubeDL(opts)
        if self.debug: print(f"Parallel: {str(self.appConfig['prefs']['parallel'])}")
        lines=[]
        if self.path == None:
            lines = self.mainText.get("1.0", END)
        else:
            with open(self.path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
        lines = [i.replace("\n", "") for i in lines]
        for i in lines:
            if i.strip() == "" or i.strip().startswith("#"): lines.remove(i)
        if lines[-1].strip() == "": lines = lines[:-1]
        messagebox.showwarning("Starting Download", "This may take some time...", parent=self.ytDownloadWin)
        self.running = True
        if not self.appConfig['prefs']['print_log']: self.ytDownloadWin.outText.insert(END, "Check console window if you want to see output")
        for a in range(run):
            if self.appConfig['prefs']['parallel'] == False:
                ytdl.download(lines)
            else:
                for i in lines:
                    th = threading.Thread(target=ytdl.download, args=[[i]])
                    th.start()
                th.join()
            if self.appConfig['prefs']['remove_success']:
                with open(self.relative_path("Logs\\archive.txt"), "r") as f:
                    success = f.readlines()
                    f.close()
                for i in range(len(success)): success[i] = success[i][success[i].index(" ")+1:]
                ltext: list = self.mainText.get("1.0", END).split("\n")
                difference=list(set(success) ^ set(ltext))
                if self.debug: print(f"SUCCESS: {success}\nLTEXT: {ltext}\nDIFFERENCE: {difference}")
                self.mainText.delete("1.0", END)
                if self.debug: print(f"Lines to keep: '{difference}'\nVideo IDs: {success}")
                self.mainText.insert("1.0", "\n".join(ltext))
                with open(self.relative_path("Logs\\archive.txt"), "w") as f:
                    f.write("")
                    f.close()
            self.ytDownloadWin.outRedir.old_stdout.write(f"Finished run {a+1}")
            if a < run - 1: print("------------\n------------")
        self.running=False
        try:
            toDisable.config(state=NORMAL)
        except:
            print("Process unfinished... Window closed early")
        else:
            print("Process finished successfully\nWindow may be closed...", end="")
            messagebox.showinfo("Download finished", "Download finished successfully", parent=self.ytDownloadWin)
        l = self.ytDownloadWin.outText.get("1.0", END).split("\n")
        for i in l:
            if i.strip() == "" or i.strip() == "\n": l.remove(i)
            self.ytDownloadWin.outText.delete("1.0", END)
            self.ytDownloadWin.outText.insert("".join(l))

    def options_win(self):
        self.oWin = Toplevel(self)
        self.oWin.title("Download Options")
        self.oWin.config(bg=self.backgrounds[self.appConfig['prefs']['theme']])
        self.oWin.iconbitmap(self.relative_path("Resources\\TransparentBox_1-1.ico"))
        def update_opts(arg=None):
            self.appConfig['opts']['description'] = desc.get()
            self.appConfig['opts']['subtitles'] = subt.get()
            self.appConfig['opts']['metadata'] = meta.get()
            self.appConfig['opts']['thumbnail'] = thumb.get()
            self.appConfig['opts']['resolution'] = int(resBox.get())
            self.writeConfig()
        desc = BooleanVar(self.oWin, value=self.appConfig['opts']['description'])
        desBox = ttk.Checkbutton(self.oWin, variable=desc, command=update_opts, text=" - Add description")
        subt = BooleanVar(self.oWin, value=self.appConfig['opts']['subtitles'])
        subtBox = ttk.Checkbutton(self.oWin, variable=subt, command=update_opts, text=" - Download subtitles")
        thumb = BooleanVar(self.oWin, value=self.appConfig['opts']['thumbnail'])
        thumbBox = ttk.Checkbutton(self.oWin, variable=thumb, command=update_opts, text=" - Embed Thumbnail")
        meta = BooleanVar(self.oWin, value=self.appConfig['opts']['metadata'])
        metaBox = ttk.Checkbutton(self.oWin, variable=meta, command=update_opts, text=" - Add metadata")
        resFrm = ttk.Frame(self.oWin)
        resLbl = ttk.Label(resFrm, text=" - Max resolution")
        resBox = ttk.Spinbox(resFrm, values=[480, 720, 1080, 2160], command=update_opts)
        resBox.set(self.appConfig['opts']['resolution'])
        desBox.grid(column=0, row=0, sticky=NW)
        subtBox.grid(column=0, row=1, sticky=NW)
        thumbBox.grid(column=0, row=2, sticky=NW)
        metaBox.grid(column=0, row=3, sticky=NW)
        resFrm.grid(column=0, row=4, sticky=NW)
        resBox.grid(column=0, row=0)
        resLbl.grid(column=1, row=0)
        ttk.Label(self.oWin, text="NOTE: Some options may cause undesirable behaviours on platforms other than YT.\nE.g. twitch's description is the stream JSON.").grid(column=0, row=5)
    def update_theme(self, theme):
        self.set_theme(theme, self.backgrounds[theme], self.backgrounds[theme])
        self.config(bg=self.backgrounds[self.appConfig['prefs']['theme']])
        try: 
            self.oDownloadWin.config(bg=self.backgrounds[theme])
            self.oDownloadWin.outText.config(bg=self.backgrounds[theme])
        except:
            pass
        try: 
            self.ytDownloadWin.config(bg=self.backgrounds[theme])
        except:
            pass
        try: 
            self.oWin.config(bg=self.backgrounds[theme])
        except:
            pass
        try: 
            self.timeWindow.config(bg=self.backgrounds[theme])
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
        self.pWin.iconbitmap(self.relative_path("Resources\\TransparentBox_1-1.ico"))
        def warn_para(arg=None):
            update_prefs()
            if para.get(): messagebox.showwarning("Parallel Download Warning", "Downloading in parallel will mess up the output window", parent=self.pWin)
        def update_prefs(arg=None):
            self.appConfig['prefs']['parallel'] = para.get()
            self.appConfig['prefs']['print_log'] = log.get()
            self.appConfig['prefs']['theme'] = theme.get()
            self.appConfig['prefs']['verbosity'] = verb.get()
            self.appConfig['prefs']['rerun'] = rerun.get()
            self.appConfig['prefs']['outwin_mode'] = closeOut.get()
            if hasattr(self, "ytDownloadWin"): self.ytDownloadWin.delClose=closeOut.get()
            if hasattr(self, "timeWindow"): self.timeWindow.delClose=closeOut.get()
            # self.appConfig['prefs']['remove_success'] = rem.get()
            self.update_theme(theme.get())
            self.writeConfig()
            if self.debug: print(self.appConfig)
        def reset_prefs(arg=None):
            self.appConfig['prefs'] = {"font": self.appConfig['prefs']['font'], "parallel": False, "print_log": True, "theme": "vista", "verbosity": False, "remove_success": False, "rerun": False, "outwin_mode": 0}
            self.writeConfig()
            para.set(self.appConfig['prefs']['parallel'])
            theme.set(self.appConfig['prefs']['theme'])
            log.set(self.appConfig['prefs']['print_log'])
            verb.set(self.appConfig['prefs']['verbosity'])
            rerun.set(self.appConfig['prefs']['rerun'])
            closeOut.set(self.appConfig['prefs']['outwin_mode'])
            # rem.set(self.appConfig['prefs']['remove_success'])
            self.update_theme(theme.get())
            theme_changed()
        def theme_changed(arg=None):
            update_prefs()
            ans = messagebox.askyesno("Restart Required", "Changing theme requires the app to be relaunched for all changes to be visible.\nRestart Now?", parent=self.pWin)
            if ans and self.exe:
                print("EXE restart")
                os.system("cls")
                os.execl(sys.executable, f'"{self.path}"')
            elif ans:
                print("PYTHON RESTART")
                os.system("cls")
                os.execl(sys.executable, __file__, f'"{self.path}"')
            else:
                print("[WARNING]: Some Elements may have visual glitches without a restart.")
        resetBtn = ttk.Button(self.pWin, text="Reset Prefs", command=reset_prefs)
        resetBtn.pack(side=BOTTOM)
        prefBook = ttk.Notebook(self.pWin)
        prefBook.enable_traversal()
        prefBook.pack(side=TOP, expand=True, fill=BOTH)
        pFrm = ttk.Frame(prefBook, relief=FLAT)
        pFrm.pack(expand=True, fill=BOTH, side=TOP)
        para = BooleanVar(self.pWin, value=self.appConfig['prefs']['parallel'])
        paraBox = ttk.Checkbutton(pFrm, variable=para, command=warn_para, text=" - Download in parallel (Will mess up output window)")
        log = BooleanVar(self.pWin, value=self.appConfig['prefs']['print_log'])
        logBox = ttk.Checkbutton(pFrm, variable=log, command=update_prefs, text=" - Print download log to output (defaults to console window)")
        themeFrm = ttk.Frame(pFrm)
        theme = StringVar(self.pWin, value=self.appConfig['prefs']['theme'])
        themeBox = ttk.OptionMenu(themeFrm, theme, theme.get(), 'adapta', 'alt', 'aquativo', 'arc', 'awarc', 'awblack', 'awbreeze', 'awbreezedark', 'awclearlooks', 'awdark', 'awlight', 'awtemplate', 'awwinxpblue', 'black', 'blue', 'breeze', 'clam', 'classic', 'clearlooks', 'default', 'elegance', 'equilux', 'itft1', 'keramik', 'kroc', 'plastik', 'radiance', 'scidblue', 'scidgreen', 'scidgrey', 'scidmint', 'scidpink', 'scidpurple', 'scidsand', 'smog', 'ubuntu', 'vista', 'winnative', 'winxpblue', 'xpnative', 'yaru', command=theme_changed)
        themeLbl = ttk.Label(themeFrm, text=" - Theme")
        paraBox.grid(column=0, row=0, sticky=NW)
        logBox.grid(column=0, row=1, sticky=NW)
        themeFrm.grid(column=0, row=2, sticky=NW)
        themeBox.grid(column=0, row=0, sticky=NW)
        themeLbl.grid(column=1, row=0, sticky=NW)
        prefBook.add(pFrm, text="General", underline=0)

        advFrm = ttk.Frame(prefBook, relief=FLAT)
        advFrm.pack(expand=True, fill=BOTH, side=TOP)
        verb = BooleanVar(self.pWin, value=self.appConfig['prefs']['verbosity'])
        verbBox = ttk.Checkbutton(advFrm, variable=verb, command=update_prefs, text=" - Add download verbosity (Shows extra info in output window)")
        rerun = BooleanVar(self.pWin, value=self.appConfig['prefs']['rerun'])
        rerunBox = ttk.Checkbutton(advFrm, variable=rerun, command=update_prefs, text=" - Runs downloader twice as sometimes errors can occur in post processing")
        closeOut = IntVar(self.pWin, value=self.appConfig['prefs']['outwin_mode'])
        withOutBox = ttk.Radiobutton(advFrm, command=update_prefs, text=" - Withdraw (hide) output window on close", value=0, variable=closeOut)
        delOutBox = ttk.Radiobutton(advFrm, command=update_prefs, text=" - Delete output windows on close", value=1, variable=closeOut)
        # rem = BooleanVar(self.pWin, value=self.appConfig['prefs']['remove_success'])
        # remBox = ttk.Checkbutton(advFrm, variable=rem, command=update_prefs, text=" - Remove successful downloads from list")
        verbBox.grid(column=0, row=0, sticky=NW)
        rerunBox.grid(column=0, row=1, sticky=NW)
        # withOutBox.grid(column=1, row=2, sticky=NW)
        # delOutBox.grid(column=1, row=4, sticky=NW)

        # remBox.grid(column=0, row=2, sticky=NW)
        prefBook.add(advFrm, text="Advanced", underline=0)
    def about(self):
        def link(url):
            os.system(f"start {url}")
        self.aWin=Toplevel(self, background=self.backgrounds[self.appConfig['prefs']['theme']])
        self.aWin.title("Youtube-dl GUI - About")
        # self.aWin.geometry("300x175")
        self.aWin.iconbitmap(self.relative_path("Resources\\TransparentBox_1-1.ico"))
        self.aWin.mainFrm=ttk.Frame(self.aWin)
        self.aWin.mainFrm.pack(side=TOP, expand=YES, fill=BOTH)

        verLbl=ttk.Label(self.aWin.mainFrm, text=f"Youtube-dl GUI v{appVersion}", justify=LEFT, anchor=NW)
        verLbl.grid(column=0,row=0,sticky=NW,padx=10,pady=2, columnspan=2)
        undFnt = font.Font(verLbl, font=verLbl.cget("font"), underline=True, size=9)

        autLbl=ttk.Label(self.aWin.mainFrm, text="Author: ", justify=LEFT, anchor=NW)
        autLbl.grid(column=0,row=1,sticky=NW,padx=10,pady=2)
        aut2Lbl=ttk.Label(self.aWin.mainFrm, text="Alex Johnson", justify=LEFT, anchor=NW)
        aut2Lbl.grid(column=1,row=1,sticky=NW,padx=10,pady=2)
        conLbl=ttk.Label(self.aWin.mainFrm, text="Contact: ", justify=LEFT, anchor=NW)
        conLbl.grid(column=0,row=2,sticky=NW,padx=10,pady=2)
        con2Lbl=ttk.Label(self.aWin.mainFrm, text="16JohnA28@gmail.com", foreground="#00A7FF", font=undFnt, cursor="hand2", justify=LEFT, anchor=NW)
        con2Lbl.bind("<Button-1>", lambda e: link("mailto:16JohnA28@gmail.com"))
        con2Lbl.grid(column=1,row=2,sticky=NW,padx=10,pady=2)
        gitLbl=ttk.Label(self.aWin.mainFrm, text="Github: ", justify=LEFT, anchor=NW)
        gitLbl.grid(column=0,row=3,sticky=NW,padx=10,pady=2)
        git2Lbl=ttk.Label(self.aWin.mainFrm, text="https://github.com/MrTransparentBox/ytdl-gui", foreground="#00A7FF", font=undFnt, cursor="hand2", justify=LEFT, anchor=NW)
        git2Lbl.bind("<Button-1>", lambda e: link("https://github.com/MrTransparentBox/ytdl-gui"))
        git2Lbl.grid(column=1,row=3,sticky=NW,padx=10,pady=2)

    def bug(self):
        ans=messagebox.askyesnocancel("Report via email?", "Would you like to report a bug by email.\nYes: report by email\nNo: report on github")
        if ans==True:
            os.system("start mailto:16JohnA28@gmail.com")
            if self.debug: print("Email report.")
        elif ans==False:
            os.system("start https://github.com/MrTransparentBox/ytdl-gui/issues/new")
            if self.debug: print("Github report.")
        else:
            if self.debug: print("Cancelled report.")
    def font(self):
        Font_wm(Font=self.currFont)
        self.fontToList()
    def writeConfig(self):
        with open(self.relative_path("appConfig.json"), "w") as f:
            json.dump(self.appConfig, f)
            f.close()

    def on_closing(self, event=None):
        try:
            self.fontToList()
        except Exception as ex:
            if self.debug: print(ex)
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
    def fontToList(self):
        self.appConfig['prefs']['font'] = [self.currFont.actual("family"), self.currFont.actual("size"), self.currFont.actual("weight"), self.currFont.actual("slant"), self.currFont.actual("underline"), self.currFont.actual("overstrike")]
        self.writeConfig()
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
            except TclError as e:
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
        except TclError as e:
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
        self.outText = Text(self.textFrm, font=self.master.currFont, yscrollcommand=self.yScroll.set, relief=FLAT, state=DISABLED)
        self.yScroll.config(command=self.outText.yview)
        if self.master.appConfig['prefs']['print_log']: 
            self.outRedir = StdoutRedirect(self.outText)
            self.errRedir = StderrRedirect(self.outText, master=self)
        if self.mode == "yt":
            self.btnStart = ttk.Button(self, text="Start Download", command=self.task)
            self.progress = ttk.Progressbar(self, length=800, mode='determinate', maximum=1, value=0)
            self.progress.pack(side=TOP)
        elif self.mode == "time":
            self.btnStart = ttk.Button(self, text="Start Duration Scan", command=self.task)
        else:
            print(f"mode '{self.mode}' incorrect")
        self.btnStart.pack(side=BOTTOM)
        self.textFrm.pack(side=TOP, expand=True, fill=BOTH)
        self.yScroll.pack(fill=Y, side=RIGHT)
        self.outText.pack(expand=True, fill=BOTH)
        self.iconbitmap(self.master.relative_path("Resources\\TransparentBox_1-1.ico"))
        self.protocol("WM_DELETE_WINDOW", self.outWin_close)
        self.focus_set()
        if self.setGrab: self.grab_set()
    def outWin_close(self, event=None):
        if self.master.running and self.block:
            messagebox.showerror("Cannot close", "Unable to close window while download is in progress.", parent=self)
            return
        elif self.master.running and self.delClose == 1:
            messagebox.showwarning("Download not stopped...", "Download logs continue in the console.", parent=self)
        self.grab_release()
        if self.delClose == 1:
            self.destroy()
            self.outRedir.close()
            self.errRedir.close()
            if self.mode == "yt" and hasattr(self.master, "ytDownloadWin"): 
                del self.master.ytDownloadWin
                if self.master.debug: print("Deleted yt win")
            elif self.mode == "time" and hasattr(self.master, "timeWindow"):
                del self.master.timeWindow
                if self.master.debug: print("Deleted time win")
        elif self.delClose == 0:
            self.withdraw()
            if self.master.debug: print("Withdrawn")        
    def task(self):
        if self.mode == "yt" and self.master.appConfig['prefs']['rerun']:
            self.t = threading.Thread(target=self.master.ytDownload, args=[self.btnStart, 2])
        elif self.mode == "yt":
            self.t = threading.Thread(target=self.master.ytDownload, args=[self.btnStart])
        elif self.mode == "time":
            self.t = threading.Thread(target=self.master.startTime)
        else:
            print(f"mode '{self.mode}' incorrect")
            return
        self.t.start()
appVersion = "2021.07.03.f1"
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", "--verbose", action="store_true", help="set program to debug mode for more info printed", dest="debug", default=False)
    parser.add_argument("-n", "--notes", action="store_true", help="show update notes and exit", default=False)
    parser.add_argument("-v", "--version", action="version", help="show version message and exit", version="%(prog)s v" + appVersion)
    parser.add_argument("path" , nargs="?", help="path to a .ytdl file containing a list of URLs for the editor", default=None)
    args = parser.parse_args()
    if args.notes:
        notes = f"""Youtube-dl GUI v{appVersion}
-- Added about section
-- Changed .vdl association to .ytdl
-- SaveAs when attempting to save new file
-- Resets opened file when clicking new
-- Uses mainText lines when no .ytdl file is open
-- Only one instance of the program can run at once
-- Time and download output windows are now persistant
-- Generally better input validation
-- Other general optimisations"""
        print(notes)
        sys.exit(0)
    if args.path == None:
        p = None
    elif not os.path.exists(os.path.abspath(args.path)):
        sys.exit(f"File {args.path} doesn't exist")
    else:
        p = os.path.abspath(args.path)
    if args.debug: print(sys.argv)
    if args.debug:
        app = Application("Youtube-dl GUI", "1080x600", True, p)
    else:
        app = Application("Youtube-dl GUI", "1080x600", False, p)
    app.focus_set()
    app.mainloop()

#VERSION VAR
if __name__ == "__main__":
    processes=[p.name() for p in psutil.process_iter()]
    if processes.count("DownloaderGUI.exe") < 2:
        main()
    else:
        messagebox.showwarning("Program Running", "The program is already running...")
        sys.exit("Already Running...")