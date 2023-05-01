#!/usr/bin/env
import argparse
import DownloaderGUI, sys
from tkinter import messagebox
if __name__ == "__main__":
    import psutil
    processes=[p.name() for p in psutil.process_iter()]
    if processes.count("YTDL_GUI.exe") < 2:
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--debug", "--verbose", action="store_true", help="set program to debug mode for more info printed", dest="debug", default=False)
        parser.add_argument("-n", "--notes", action="store_true", help="show update notes and exit", default=False)
        parser.add_argument("-v", "--version", action="version", help="show version message and exit", version="%(prog)s v" + DownloaderGUI.appVersion)
        parser.add_argument("path" , nargs="?", help="path to a .ytdl file containing a list of URLs for the editor", default=None)
        args = parser.parse_args()
        DownloaderGUI.main(args)
    else:
        messagebox.showwarning("Program Running", "The program is already running...")
        sys.exit("Already Running...")