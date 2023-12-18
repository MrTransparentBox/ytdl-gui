"""Provides classes & functionality for the programs auto updater"""
import os
import threading
from tkinter import Misc, StringVar, TclError, Toplevel, messagebox, ttk
from tkinter.constants import BOTTOM, CENTER, DISABLED, LEFT, NORMAL, X
from typing import TYPE_CHECKING, Callable

import requests

from modules.constants import BACKGROUNDS
from modules.utils import relative_path, version_compare

if TYPE_CHECKING:
    from modules.application import Application


class Updater:
    """Logic and networking to download and install the new update"""

    def __init__(self, my_version, master: Misc | None = None) -> None:
        self.app_version = my_version
        self.master: Application = master
        self.open_window: UpdateWindow | None = None

    def check_update(self, quiet: bool = False):
        try:
            latest = requests.get(
                "https://api.github.com/repos/MrTransparentBox/ytdl-gui/releases/latest",
                headers={
                    "accept": "application/vnd.github.v3+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
                timeout=60,
            )
            if latest.status_code == 404:
                messagebox.showinfo(
                    "No releases found",
                    "There are no releases for this program.\nIf you think this is an error please report it on",
                    parent=self,
                )
                return None
            latest.raise_for_status()
            latest = latest.json()
            tag = latest["tag_name"]
        except (TimeoutError, requests.HTTPError) as ex:
            messagebox.showerror(
                "Unable to check for update",
                f"{ex}\n\nTry checking your internet connection, and try again.",
                parent=self,
            )
            return None
        comp = version_compare(tag, f"v{self.app_version}")
        if comp == "=":
            if not quiet:
                messagebox.showinfo("Up-to-date", "No updates found", parent=self)
            return False
        elif comp == ">":
            messagebox.showinfo("Update available!", f"New version found: {tag}", parent=self.open_window)
            self.open_update_window(tag)
            return True
        elif comp == "<" and not quiet:
            ans = messagebox.askyesno(
                "Preview",
                "Looks like you have a special preview or pre-release version! Do you want to install the last full release?",
            )
            if ans:
                self.open_update_window(tag)
                return True
            return False

    def open_update_window(self, version_tag):
        self.open_window = UpdateWindow(
            version_tag,
            self.start_update,
            self.master,
            background=BACKGROUNDS[self.master.app_config["prefs"]["theme"]],
        )

    def start_update(self):
        filename = self.download_setup()
        if filename is not None:
            self.open_window.destroy()
            self.open_window = None
            os.execv(
                filename,
                ["""/NOCANCEL /RESTARTAPPLICATIONS /SP- /SILENT /NOICONS \"/DIR=expand:{autopf}\\Youtube-dl GUI\""""],
            )
            os._exit(0)

    def download_setup(self):
        filename = ""

        with requests.Session() as s:
            response = s.get(
                "https://github.com/MrTransparentBox/ytdl-gui/releases/latest/download/Youtube-dl_GUI_Setup.exe",
                headers={
                    "Accept": "application/octet-stream",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
                stream=True,
            )
            try:
                response.raise_for_status()
            except requests.HTTPError as e:
                messagebox.showerror("HTTP Error occurred", e)
                return None
            cd = response.headers.get("content-disposition")
            try:
                filename = os.path.join(os.environ["temp"], cd[cd.index("filename=") + 9 :])
            except KeyError:
                filename = os.path.join(os.path.expandvars("%tmp%"), cd[cd.index("filename=") + 9 :])
            length = int(response.headers.get("content-length"))
            downloaded = 0
            try:
                with open(filename, "wb") as f:
                    for data in response.iter_content(chunk_size=524288):
                        downloaded += len(data)
                        f.write(data)
                        self.open_window.progress["value"] = downloaded / length
                        self.open_window.progress_text.set(f"Downloaded: {round(downloaded/length*100, 1)}%")
                    f.close()
            except (TclError, AttributeError):
                return None
        return filename


class UpdateWindow(Toplevel):
    """Basic window to display new version info"""

    def __init__(
        self, version_tag, update_function: Callable, master: Misc | None = None, *, background: str = ...
    ) -> None:
        super().__init__(master, background=background)
        self.update_function = update_function
        self.master: Application
        self.iconbitmap(relative_path("Resources\\YTDLv2_256.ico"))
        self.title("Youtube-dl GUI - Update")
        ttk.Label(
            self,
            text="A new version of Youtube-dl GUI is available!\nAn update is recommended.",
            justify=LEFT,
        ).pack(padx=5, pady=5)
        ttk.Label(
            self,
            text=f"\tNew version: {version_tag}\n\tYour Version: v{self.master.app_version}",
            justify=LEFT,
        ).pack(pady=10)
        ttk.Label(
            self,
            text="Click update to download the new version.",
            justify=LEFT,
        ).pack()
        update_thread = threading.Thread(target=self.start_update)
        self.update_btn = ttk.Button(self, text="Update", command=update_thread.start)
        self.update_btn.pack(side=BOTTOM, pady=15)
        self.progress = ttk.Progressbar(self, maximum=1, mode="determinate", length=200)
        self.progress.pack(side=BOTTOM, fill=X, expand=True)
        self.progress_text = StringVar(self.progress, value="Downloaded: 0%")
        ttk.Label(self, textvariable=self.progress_text, justify=CENTER).pack(side=BOTTOM)
        self.focus_set()

    def start_update(self):
        if self.master.ask_save() is None:
            return
        self.focus_set()
        self.update_btn.config(state=DISABLED)
        self.update_function()
        self.update_btn.config(state=NORMAL)
