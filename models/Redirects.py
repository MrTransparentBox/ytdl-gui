import sys
from tkinter import Text, messagebox, NORMAL, END, DISABLED, TclError
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
            self.old_stderr.write(s)
        elif self.msgbox:
            messagebox.showinfo("Issue", s, parent=self.master)
        else:
            try:
                self.text_box.config(state=NORMAL)
                # s2 = s.encode("ascii", 'ignore')
                self.old_stderr.write(s)  
                if s.startswith("\r"):
                    self.text_box.delete("end-1c linestart", "end")
                    self.text_box.insert(END, f"\n{s}")
                else:
                    self.text_box.insert(END, s)
                self.text_box.see(END)
                self.text_box.config(state=DISABLED)
            except (TclError, RuntimeError) as e:
                if "main thread is not in main loop" in str(e):
                    sys.exit(e)
                self.old_stderr.write(s)
                if self.open: self.close()
    def flush(self):
        pass
    def writelines(self, lines):
        self.text_box.config(state=NORMAL)
        # for i in range(len(lines)):
        #     lines[i] = str(lines[i]).encode('ascii', 'ignore')
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
            # s2 = s.encode('ascii', 'ignore')
            if "error" in s.lower():
                messagebox.showerror("Error", s)
            if s.startswith("\r"):
                self.text_box.delete("end-1c linestart", "end")
                self.text_box.insert(END, f"\n{s}")
            else:
                self.text_box.insert(END, s)
            self.text_box.see(END)
            self.text_box.config(state=DISABLED)
        except TclError:
            self.old_stdout.write(s)
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