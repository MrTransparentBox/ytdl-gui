import os, sys
class GetStats():
    """Gets basic stats about a file or folder. Only folder video contents lenth currently.
    
    Ar
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
            with VideoFileClip(filename) as clip:
                return clip.duration    
        except Exception as ex:
            sys.exit(f"vv Error occurred getting video duration vv.\n\n{str(ex)}\n")

    def folder_length(self) -> dict:
        sDir = self.pathname
        tlis = os.listdir(sDir)
        self.write("Gathered folder contents.")
        totTime=0
        self.write("<Video name>: <seconds.microseconds>\n\n--------------------", 1)
        for i in tlis:
            if (i.endswith(".mp4") or i.endswith(".mov") or i.endswith(".mkv") or i.endswith(".webm") or i.endswith(".avi")) and i.count(".temp") == 0:
                t = self.get_length(os.path.join(self.pathname, i))
                if t == None: continue
                self.write(f"{i}: {t}s\n--------------------\n", 2)
                totTime += t
        seconds=totTime%60
        minutes=int((totTime/60)%60)
        hours=int(totTime/3600)
        self.write(f"Total video time: {hours}h:{minutes}m:{seconds}s\n\n", importance=1)
        return {"hours": hours, "minutes": minutes, "seconds": seconds}