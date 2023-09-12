import os, sys, threading
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
        # self.takeTime = False
        self.totTime = 0
        self.__dots__ = 0
    def write(self, text: str, importance=0, long=0):
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
                
    def get_length(self, filename, video=True):
        if not os.path.exists(filename): return None
        from moviepy.editor import VideoFileClip, AudioFileClip
        try:
            if video:
                with VideoFileClip(filename) as clip:
                    return clip.duration    
            else:
                with AudioFileClip(filename) as clip:
                    return clip.duration
        except Exception as ex:
            sys.exit(f"vv Error occurred getting file duration vv.\n\n{str(ex)}\n")

    def file_time(self, i):
        if i.count(".temp") == 0:
                isvideo = None
                if i.endswith(".mp4") or i.endswith(".mov") or i.endswith(".mkv") or i.endswith(".webm") or i.endswith(".avi") or i.endswith(".mpeg"): isvideo = True
                elif i.endswith(".mp3") or i.endswith(".opus") or i.endswith(".m4a") or i.endswith(".aac") or i.endswith(".wav"): isvideo = False
                else: return
                t = self.get_length(os.path.join(self.pathname, i), isvideo)
                if t == None: return
                iname=str(i).strip().strip('\r\n')
                self.write(f"{iname}: {t}s\n--------------------\n", 2)
                self.totTime += t
    def folder_length(self) -> dict:
        sDir = self.pathname
        tlis: list[str] = os.listdir(sDir)
        self.write("Gathered folder contents.")
        self.totTime=0
        self.write("<Video name>: <seconds>\n\n--------------------", 1)
        threads: list[threading.Thread] = []
        completed = 0
        for i in tlis:
            fn = i
            t = threading.Thread(target=lambda: self.file_time(fn))
            t.start()
            threads.append(t)
        for x in threads:
            x.join()
            completed += 1
        self.write(f"{completed} done out of {len(tlis)}")
        seconds=self.totTime%60
        minutes=int((self.totTime/60)%60)
        hours=int(self.totTime/3600)
        self.write(f"Total video time: {hours}h:{minutes}m:{seconds}s\n\n", importance=1)
        return {"hours": hours, "minutes": minutes, "seconds": seconds}