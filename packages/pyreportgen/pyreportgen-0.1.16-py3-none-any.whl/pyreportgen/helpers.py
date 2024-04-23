import uuid
from pyreportgen.base import _DATA_DIR
import os
import sys



class ProgressBar:
    if sys.stdout.encoding == "utf-8":
        empty = " "
        half = "▌"
        full = "█"
    else:
        empty = " "
        half = " "
        full = "#"
    
    bar_length = 60
    def __init__(self, length:int, title:str = "Progress") -> None:
        self.length:int = length
        self.title:str = title
    
    def print(self, progress):
        percentage:float = float(progress)/float(self.length)
        bar = ""

        chars_to_fill = self.bar_length*percentage
        full_chars = int(chars_to_fill)
        half_char = (chars_to_fill-full_chars) > 0.5

        bar += self.full*full_chars
        if half_char:
            bar += self.half

        bar = bar.ljust(self.bar_length, self.empty)
        print(f"\r{self.title} - |{bar}| {str(int(percentage*100)).rjust(3)}% ({progress}/{self.length})", end="")
        if progress == self.length:
            print()

def clamp(num, min, max):
    if num < min:
        return min
    if num > max:
        return max
    return num

def random_path(filetype):
    return os.path.join(_DATA_DIR, random_filename(filetype))
def random_filename(filetype):
    return f"{str(uuid.uuid4())}."+filetype

#def to_html_path(path):
 #   return "file://"+str(os.path.abspath('index.html'))

def tagwrap(content:str, tag:str, classList="", props="", close=True) -> str:
    if close:
        return f"<{tag} class='{classList}' {props}>{content}</{tag}>"
    else:
        return f"<{tag} class='{classList}' {props} />"