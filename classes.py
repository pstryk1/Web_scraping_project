import tkinter as tk
import ttkbootstrap as ttk
from bs4 import BeautifulSoup as bs
from lxml import html
import requests
import sys

class Fullscreen_Window:

    def __init__(self):
        self.ttk = ttk.Window(themename="darkly")
        self.ttk.attributes("-topmost", True)
        #self.tk.geometry("{0}x{1}+0+0".format(self.tk.winfo_screenwidth(), self.tk.winfo_screenheight()))
        self.ttk.state('zoomed')
        self.frame = ttk.Frame(self.ttk)
        self.frame.pack()
        self.state = False
        self.ttk.bind("<F11>", self.toggle_fullscreen)
        self.ttk.bind("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.ttk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.ttk.attributes("-fullscreen", False)
        return "break"
    
    def colors(self, color, fontcolor):
        self.ttk.configure(bg=color, fg = fontcolor)

    def edit_text(self,  height, width):
        edit_text = tk.Text(height=height, width=width, font=("Arial", 12), bd=2, relief="groove")
        edit_text.pack() #expand=False, fill="both"
        return edit_text.get("1.0", "end-1c")


